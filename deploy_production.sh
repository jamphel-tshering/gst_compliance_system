#!/bin/bash
# GST COMPLIANCE SYSTEM - PRODUCTION DEPLOYMENT SCRIPT
# Domain: mongargst.drc.gov.bt

echo "🚀 GST Compliance System - Production Deployment"
echo "Domain: mongargst.drc.gov.bt"
echo "=========================================="

# Check if .env.production exists
if [ ! -f .env.production ]; then
    echo "❌ Error: .env.production file not found!"
    exit 1
fi

# Copy production environment
echo "📋 Copying production environment..."
cp .env.production .env

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "🗄️  Running database migrations..."
python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if not exists
echo "👤 Creating superuser account..."
python manage.py shell << EOF
from core.models import User
if not User.objects.filter(email='admin@drc.gov.bt').exists():
    User.objects.create_superuser(
        email='admin@drc.gov.bt',
        username='admin',
        password='change-me-immediately'
    )
    print("✅ Superuser created: admin@drc.gov.bt / admin / change-me-immediately")
else:
    print("ℹ️  Superuser already exists")
EOF

echo "✅ Deployment setup complete!"
echo "=========================================="
echo "📋 Next Steps:"
echo "1. Start production server: gunicorn gst_compliance_system.wsgi:application"
echo "2. Configure web server (Nginx/Apache)"
echo "3. Set up SSL certificate"
echo "4. Change superuser password immediately!"
echo "=========================================="
echo "🎉 System ready for production launch!"