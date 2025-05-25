#!/bin/bash

# SmartBetGPT Production Deployment Script
# This script sets up the application on a DigitalOcean droplet

set -e  # Exit on any error

echo "🚀 Starting SmartBetGPT Production Deployment..."

# Variables
PROJECT_DIR="/var/www/smartbetgpt"
DOMAIN="smartbetgpt.me"
USER="www-data"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Update system packages
print_status "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required packages
print_status "Installing required packages..."
sudo apt install -y python3 python3-pip python3-venv nginx supervisor git ufw certbot python3-certbot-nginx

# Create project directory
print_status "Setting up project directory..."
sudo mkdir -p $PROJECT_DIR
sudo chown $USER:$USER $PROJECT_DIR

# Copy application files (assuming they're in current directory)
print_status "Copying application files..."
sudo cp -r . $PROJECT_DIR/
sudo chown -R $USER:$USER $PROJECT_DIR

# Set up Python virtual environment
print_status "Setting up Python virtual environment..."
cd $PROJECT_DIR
sudo -u $USER python3 -m venv venv
sudo -u $USER ./venv/bin/pip install --upgrade pip
sudo -u $USER ./venv/bin/pip install -r requirements.txt

# Set up environment variables for production
print_status "Setting up production environment..."
sudo -u $USER cp .env.production .env

# Initialize database
print_status "Initializing database..."
sudo -u $USER ./venv/bin/python create_db.py

# Create Gunicorn configuration
print_status "Creating Gunicorn configuration..."
sudo tee $PROJECT_DIR/gunicorn.conf.py > /dev/null <<EOF
# Gunicorn configuration file for SmartBetGPT

# Server socket
bind = "127.0.0.1:8000"
backlog = 2048

# Worker processes
workers = 3
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Restart workers after this many requests, to prevent memory leaks
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"

# Process naming
proc_name = 'smartbetgpt'

# Server mechanics
daemon = False
pidfile = '/var/run/gunicorn/smartbetgpt.pid'
user = 'www-data'
group = 'www-data'
tmp_upload_dir = None

# SSL (will be handled by Nginx)
keyfile = None
certfile = None
EOF

# Create log directories for Gunicorn
sudo mkdir -p /var/log/gunicorn
sudo mkdir -p /var/run/gunicorn
sudo chown -R $USER:$USER /var/log/gunicorn
sudo chown -R $USER:$USER /var/run/gunicorn

# Create Supervisor configuration for Gunicorn
print_status "Setting up Supervisor for process management..."
sudo tee /etc/supervisor/conf.d/smartbetgpt.conf > /dev/null <<EOF
[program:smartbetgpt]
command=$PROJECT_DIR/venv/bin/gunicorn --config $PROJECT_DIR/gunicorn.conf.py wsgi:application
directory=$PROJECT_DIR
user=$USER
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/supervisor/smartbetgpt.log
EOF

# Configure Nginx
print_status "Configuring Nginx..."
sudo tee /etc/nginx/sites-available/smartbetgpt > /dev/null <<EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

    # Serve static files directly
    location /static {
        alias $PROJECT_DIR/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Proxy all other requests to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_redirect off;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 10240;
    gzip_proxied expired no-cache no-store private must-revalidate no_last_modified no_etag auth;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss;

    # File upload size limit
    client_max_body_size 10M;
}
EOF

# Enable the site
sudo ln -sf /etc/nginx/sites-available/smartbetgpt /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# Configure firewall
print_status "Configuring firewall..."
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw --force enable

# Start services
print_status "Starting services..."
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start smartbetgpt
sudo systemctl restart nginx
sudo systemctl enable supervisor
sudo systemctl enable nginx

print_success "Base deployment completed!"
print_warning "Next steps:"
echo "1. Update DNS records to point $DOMAIN to this server's IP"
echo "2. Wait for DNS propagation (up to 24 hours)"
echo "3. Run SSL setup script: sudo ./setup_ssl.sh"
echo "4. Update .env file with production values"

print_status "Deployment completed! Your application should be accessible at http://$DOMAIN"
