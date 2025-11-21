#!/bin/bash

# Buffet School Management System - Deployment Script
# This script helps deploy the application on a server

set -e

echo "🍎 Buffet School Management System - Deployment Setup"
echo "======================================================"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create a .env file based on .env.example"
    echo "cp .env.example .env"
    echo "Then edit .env with your configuration."
    exit 1
fi

echo "✅ Found .env configuration file"

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Check Django configuration
echo "🔍 Checking Django configuration..."
python manage.py check --settings=buffet_app.settings_production

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate --settings=buffet_app.settings_production

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --settings=buffet_app.settings_production

# Check if superuser exists
echo "👤 Checking for superuser..."
python manage.py shell --settings=buffet_app.settings_production -c "
from django.contrib.auth.models import User
if not User.objects.filter(is_superuser=True).exists():
    print('No superuser found. Please create one manually:')
    print('python manage.py createsuperuser --settings=buffet_app.settings_production')
else:
    print('✅ Superuser already exists')
"

echo ""
echo "🎉 Deployment setup completed successfully!"
echo ""
echo "To start the application:"
echo "  Development: python manage.py runserver"
echo "  Production:  gunicorn buffet_app.wsgi:application --bind 0.0.0.0:8000"
echo ""
echo "Or use Docker:"
echo "  docker-compose up -d"
echo ""
echo "Don't forget to:"
echo "  1. Configure your web server (Nginx/Apache)"
echo "  2. Set up SSL certificates"
echo "  3. Configure firewall rules"
echo "  4. Set up automated backups"