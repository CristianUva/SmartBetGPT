# SmartBetGPT Deployment Guide

## Prerequisites
- DigitalOcean Droplet (Ubuntu 20.04/22.04 LTS)
- Domain: smartbetgpt.me (purchased from Namecheap)
- SSL Certificate (from Namecheap or Let's Encrypt)

## Server Requirements
- **OS**: Ubuntu 20.04/22.04 LTS
- **RAM**: Minimum 1GB (recommended 2GB)
- **Storage**: Minimum 25GB SSD
- **CPU**: 1 vCPU (recommended 2 vCPU)

## Deployment Steps

### 1. Create DigitalOcean Droplet
1. Log into DigitalOcean
2. Create new Droplet:
   - **Image**: Ubuntu 22.04 LTS
   - **Size**: Basic $12/month (2GB RAM, 1 vCPU, 50GB SSD)
   - **Region**: Choose closest to your users
   - **SSH Key**: Add your SSH key
   - **Hostname**: smartbetgpt

### 2. Configure DNS (Namecheap)
1. Log into Namecheap
2. Go to Domain List → smartbetgpt.me → Manage
3. Advanced DNS tab
4. Add these records:
   ```
   Type: A Record
   Host: @
   Value: [Your Droplet IP]
   TTL: 1 min
   
   Type: A Record  
   Host: www
   Value: [Your Droplet IP]
   TTL: 1 min
   ```

### 3. Upload Files to Server
```bash
# On your local machine
cd /home/crisexy/NewTest/SmartBetGPT
rsync -avz --exclude='.git' --exclude='__pycache__' --exclude='*.pyc' . root@YOUR_DROPLET_IP:/tmp/smartbetgpt/
```

### 4. Run Deployment Script
```bash
# SSH into your droplet
ssh root@YOUR_DROPLET_IP

# Move files and run deployment
mv /tmp/smartbetgpt /root/
cd /root/smartbetgpt
chmod +x deploy.sh setup_ssl.sh
./deploy.sh
```

### 5. Configure Environment Variables
```bash
# The production environment file is already configured with your credentials
# You can verify the configuration with:
sudo cat /var/www/smartbetgpt/.env

# The file should contain your actual API keys and email credentials
# If you need to make changes, edit with:
sudo nano /var/www/smartbetgpt/.env
```

### 6. Wait for DNS Propagation
Wait 1-24 hours for DNS to propagate globally.
Check with: `nslookup smartbetgpt.me`

### 7. Setup SSL Certificate
```bash
# After DNS propagation
cd /var/www/smartbetgpt
sudo ./setup_ssl.sh
```

### 8. Final Verification
```bash
# Check services are running
sudo supervisorctl status
sudo systemctl status nginx
sudo systemctl status certbot.timer

# Test the application
curl -I https://smartbetgpt.me
```

## Post-Deployment Tasks

### Update Production Environment
```bash
sudo nano /var/www/smartbetgpt/.env
```

### Monitor Logs
```bash
# Application logs
sudo tail -f /var/log/supervisor/smartbetgpt.log

# Nginx logs  
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Gunicorn logs
sudo tail -f /var/log/gunicorn/access.log
sudo tail -f /var/log/gunicorn/error.log
```

### Restart Services
```bash
# Restart application
sudo supervisorctl restart smartbetgpt

# Restart nginx
sudo systemctl restart nginx

# View status
sudo supervisorctl status
```

### Update Application
```bash
cd /var/www/smartbetgpt
git pull origin main  # if using git
sudo supervisorctl restart smartbetgpt
```

## Namecheap SSL Certificate (Alternative)

If you want to use your Namecheap SSL certificate instead of Let's Encrypt:

1. Download certificate files from Namecheap
2. Upload to server: `/etc/ssl/certs/smartbetgpt/`
3. Update Nginx configuration to use these files
4. Restart Nginx

## Troubleshooting

### Common Issues
- **502 Bad Gateway**: Check if Gunicorn is running
- **DNS not resolving**: Wait for propagation or check DNS settings
- **SSL errors**: Verify certificate files and Nginx config

### Debug Commands
```bash
# Check ports
sudo netstat -tlnp | grep :80
sudo netstat -tlnp | grep :8000

# Test Nginx config
sudo nginx -t

# Check supervisor
sudo supervisorctl status

# Check logs
journalctl -u nginx
journalctl -u supervisor
```

## Security Checklist
- [x] UFW firewall enabled
- [x] SSH key authentication
- [x] SSL/TLS certificate
- [x] Security headers configured
- [x] Regular backups scheduled
- [ ] Fail2ban installed (optional)
- [ ] Regular security updates

## Backup Strategy
```bash
# Database backup
cp /var/www/smartbetgpt/database.db /backup/database_$(date +%Y%m%d_%H%M%S).db

# Full application backup
tar -czf /backup/smartbetgpt_$(date +%Y%m%d_%H%M%S).tar.gz /var/www/smartbetgpt
```
