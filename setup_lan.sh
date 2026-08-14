#!/bin/bash
# GST Compliance System - LAN SQL Setup Script
# This script helps set up the system for internal LAN deployment

set -e

echo "🚀 GST Compliance System - LAN SQL Setup"
echo "=========================================="

# Configuration variables
DB_NAME="gst_compliance_db"
DB_USER="gst_admin"
DB_HOST="192.168.1.100"  # Change to your database server IP
DB_PORT="5432"
APP_DIR="/opt/gst_system"
VENV_DIR="$APP_DIR/venv"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    print_warning "This script should be run as root or with sudo"
    exit 1
fi

# Step 1: System dependencies
print_status "Installing system dependencies..."
apt update
apt install -y python3 python3-pip python3-venv postgresql-client nginx

# Step 2: Create application directory
print_status "Creating application directory..."
mkdir -p $APP_DIR
mkdir -p $APP_DIR/logs
mkdir -p $APP_DIR/media
mkdir -p $APP_DIR/static
mkdir -p $APP_DIR/backups

# Step 3: Create virtual environment
print_status "Creating Python virtual environment..."
python3 -m venv $VENV_DIR
source $VENV_DIR/bin/activate

# Step 4: Install Python dependencies
print_status "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Step 5: Test database connection
print_status "Testing database connection..."
read -p "Enter PostgreSQL password for user $DB_USER: " -s DB_PASSWORD
echo

PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d postgres -c "SELECT 1;" > /dev/null 2>&1

if [ $? -eq 0 ]; then
    print_status "Database connection successful!"
else
    print_error "Database connection failed. Please check your credentials and network."
    exit 1
fi

# Step 6: Update settings.py
print_status "Configuring Django settings for PostgreSQL..."
if [ -f "gst_compliance_system/settings_postgresql_lan.py" ]; then
    print_warning "Please manually update settings.py with PostgreSQL configuration from settings_postgresql_lan.py"
    print_warning "Update the following values:"
    print_warning "  - DATABASE settings"
    print_warning "  - ALLOWED_HOSTS"
    print_warning "  - DB_PASSWORD (use the password you entered above)"
else
    print_error "settings_postgresql_lan.py not found. Please create it first."
    exit 1
fi

# Step 7: Run migrations
print_status "Running database migrations..."
python manage.py migrate

# Step 8: Collect static files
print_status "Collecting static files..."
python manage.py collectstatic --noinput

# Step 9: Create superuser
print_status "Creating Django superuser..."
read -p "Do you want to create a superuser now? (y/n): " create_superuser
if [ "$create_superuser" = "y" ] || [ "$create_superuser" = "Y" ]; then
    python manage.py createsuperuser
fi

# Step 10: Configure systemd service
print_status "Configuring systemd service..."
cat > /etc/systemd/system/gst-compliance.service <<EOF
[Unit]
Description=GST Compliance System Django Application
After=network.target postgresql.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=$APP_DIR/gst_compliance_system
Environment="PATH=$VENV_DIR/bin"
ExecStart=$VENV_DIR/bin/gunicorn \
          --workers 3 \
          --bind 0.0.0.0:8000 \
          gst_compliance_system.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable gst-compliance

# Step 11: Configure Nginx
print_status "Configuring Nginx..."
cat > /etc/nginx/sites-available/gst-compliance <<EOF
server {
    listen 80;
    server_name _;

    location /static/ {
        alias $APP_DIR/staticfiles/;
    }

    location /media/ {
        alias $APP_DIR/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

ln -sf /etc/nginx/sites-available/gst-compliance /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx

# Step 12: Configure firewall
print_status "Configuring firewall..."
ufw allow 8000/tcp
ufw allow from $DB_HOST to any port 5432
ufw --force enable

# Step 13: Setup backup script
print_status "Setting up backup script..."
cat > $APP_DIR/backups/gst_backup.sh <<EOF
#!/bin/bash
DATE=\$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="$APP_DIR/backups"
DB_NAME="$DB_NAME"
DB_USER="$DB_USER"
DB_HOST="$DB_HOST"
DB_PORT="$DB_PORT"

mkdir -p \$BACKUP_DIR

PGPASSWORD=$DB_PASSWORD pg_dump -h \$DB_HOST -p \$DB_PORT -U \$DB_USER \$DB_NAME > \$BACKUP_DIR/gst_db_\$DATE.sql
gzip \$BACKUP_DIR/gst_db_\$DATE.sql

find \$BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete

echo "Backup completed: gst_db_\$DATE.sql.gz"
EOF

chmod +x $APP_DIR/backups/gst_backup.sh

# Add to crontab
(crontab -l 2>/dev/null; echo "0 2 * * * $APP_DIR/backups/gst_backup.sh") | crontab -

# Step 14: Start services
print_status "Starting services..."
systemctl start gst-compliance
systemctl status gst-compliance

# Step 15: Final instructions
echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo ""
echo "Your GST Compliance System is now configured for LAN deployment."
echo ""
echo "Access the application at:"
echo "  http://$(hostname -I | awk '{print $1}'):8000"
echo "  or"
echo "  http://$(hostname):8000"
echo ""
echo "Next steps:"
echo "1. Update settings.py with your database password"
echo "2. Create additional user accounts through the admin interface"
echo "3. Configure client computers to access the server"
echo "4. Test all functionality"
echo "5. Setup regular monitoring"
echo ""
echo "For detailed configuration, see LAN_SQL_SETUP_GUIDE.md"
echo ""
echo "🔒 Security Reminders:"
echo "- Change all default passwords"
echo "- Configure network firewall rules"
echo "- Set up regular backups"
echo "- Monitor system logs"
echo "- Review user access regularly"
echo ""