# GST COMPLIANCE SYSTEM - PRODUCTION DEPLOYMENT SCRIPT (Windows PowerShell)
# Domain: mongargst.drc.gov.bt

Write-Host "🚀 GST Compliance System - Production Deployment" -ForegroundColor Green
Write-Host "Domain: mongargst.drc.gov.bt" -ForegroundColor Yellow
Write-Host "==========================================" -ForegroundColor Cyan

# Check if .env.production exists
if (-not (Test-Path .env.production)) {
    Write-Host "❌ Error: .env.production file not found!" -ForegroundColor Red
    exit 1
}

# Copy production environment
Write-Host "📋 Copying production environment..." -ForegroundColor Cyan
Copy-Item .env.production .env -Force

# Install dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt

# Run database migrations
Write-Host "🗄️  Running database migrations..." -ForegroundColor Cyan
python manage.py migrate

# Collect static files
Write-Host "📁 Collecting static files..." -ForegroundColor Cyan
python manage.py collectstatic --noinput

# Create superuser if not exists
Write-Host "👤 Creating superuser account..." -ForegroundColor Cyan
python manage.py shell -c "from core.models import User; User.objects.create_superuser('admin@drc.gov.bt', 'admin', 'change-me-immediately') if not User.objects.filter(email='admin@drc.gov.bt').exists() else print('Superuser already exists')"

Write-Host "✅ Deployment setup complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "📋 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Start production server: gunicorn gst_compliance_system.wsgi:application"
Write-Host "2. Configure web server (IIS/Nginx)"
Write-Host "3. Set up SSL certificate"
Write-Host "4. Change superuser password immediately!"
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "🎉 System ready for production launch!" -ForegroundColor Green