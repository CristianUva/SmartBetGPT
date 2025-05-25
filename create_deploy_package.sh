#!/bin/bash

# SmartBetGPT - Create deployment package
# This script creates a clean deployment package

set -e

PROJECT_NAME="smartbetgpt-deploy"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
PACKAGE_NAME="${PROJECT_NAME}_${TIMESTAMP}.tar.gz"

echo "🚀 Creating deployment package for SmartBetGPT..."

# Create temporary directory
TEMP_DIR="/tmp/smartbetgpt_deploy"
rm -rf $TEMP_DIR
mkdir -p $TEMP_DIR

# Copy project files (excluding development files)
echo "📦 Copying project files..."
rsync -av \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='*.pyo' \
    --exclude='.pytest_cache' \
    --exclude='venv' \
    --exclude='env' \
    --exclude='database.db' \
    --exclude='instance/' \
    --exclude='.env.local' \
    --exclude='*.log' \
    . $TEMP_DIR/

# Create deployment package
cd /tmp
echo "📦 Creating deployment package: $PACKAGE_NAME"
tar -czf $PACKAGE_NAME smartbetgpt_deploy/

# Move package to current directory
mv $PACKAGE_NAME /home/crisexy/NewTest/SmartBetGPT/

# Cleanup
rm -rf $TEMP_DIR

echo "✅ Deployment package created: $PACKAGE_NAME"
echo "📤 Ready to upload to your DigitalOcean droplet!"
echo ""
echo "Next steps:"
echo "1. Upload this package to your server"
echo "2. Extract and run the deployment script"
echo "3. Configure DNS settings"
echo "4. Set up SSL certificate"
