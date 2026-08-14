# GST Compliance System - Internal LAN SQL-Based Application Setup Guide

## 🎯 Overview
Convert the GST Compliance System to an internal LAN SQL-based application using PostgreSQL for centralized database management, multi-user access, and government network deployment.

## 🏗️ Architecture Overview

### Recommended Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    Government Internal Network               │
│                                                              │
│  ┌──────────────┐         ┌──────────────┐                │
│  │   Database   │◄────────┤ Application  │                │
│  │   Server     │         │   Server     │                │
│  │ PostgreSQL   │         │   Django     │                │
│  │   :5432      │         │   :8000      │                │
│  └──────────────┘         └──────────────┘                │
│         │                         │                         │
│         │                         │                         │
│         └──────────┬──────────────┘                         │
│                    │                                       │
│                    ▼                                       │
│         ┌──────────────────────┐                          │
│         │   Client Computers  │                          │
│         │   (LAN Users)        │                          │
│         │   HTTP://SERVER:8000 │                          │
│         └──────────────────────┘                          │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Hardware Requirements

### Database Server (Recommended)
- **CPU**: 4+ cores
- **RAM**: 8GB+ (16GB recommended for heavy usage)
- **Storage**: 200GB+ SSD with RAID for redundancy
- **OS**: Linux (Ubuntu 22.04 LTS recommended)
- **Network**: Gigabit Ethernet

### Application Server
- **CPU**: 2+ cores
- **RAM**: 4GB+
- **Storage**: 50GB+
- **OS**: Linux or Windows
- **Network**: Gigabit Ethernet

### Client Computers
- **CPU**: Dual core
- **RAM**: 4GB+
- **OS**: Windows 10+, Linux, macOS
- **Network**: Gigabit Ethernet
- **Browser**: Chrome, Firefox, Edge

## 📦 Software Requirements

### Database Server
- **PostgreSQL**: 14+ or 15+
- **pgAdmin**: For database management
- **Backup tools**: pg_dump, pg_restore

### Application Server
- **Python**: 3.10+
- **PostgreSQL client library**: psycopg2-binary
- **Django**: 6.1
- **Gunicorn**: Production WSGI server
- **Nginx**: Reverse proxy (optional but recommended)

### Client Computers
- **Modern web browser** (Chrome, Firefox, Edge)
- **Network connectivity** to application server

## 🚀 Step-by-Step Setup Guide

### Phase 1: Database Server Setup

#### Step 1.1: Install PostgreSQL on Database Server

**For Ubuntu/Debian:**
```bash
# Update system
sudo apt update
sudo apt upgrade -y

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Install pgAdmin (optional)
sudo apt install pgadmin4 -y

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**For Windows:**
1. Download PostgreSQL installer from https://www.postgresql.org/download/windows/
2. Run installer with default settings
3. Set strong password for postgres user
4. Install pgAdmin during installation

#### Step 1.2: Configure PostgreSQL for Network Access

**Edit PostgreSQL Configuration:**
```bash
# Find configuration files
sudo -u postgres psql -c "SHOW config_file;"
sudo -u postgres psql -c "SHOW hba_file;"

# Edit postgresql.conf
sudo nano /etc/postgresql/14/main/postgresql.conf

# Add/modify these lines:
listen_addresses = '*'          # Listen on all interfaces
port = 5432                    # Default port
max_connections = 100          # Adjust based on expected users
shared_buffers = 256MB          # Adjust based on RAM
effective_cache_size = 1GB     # Adjust based on RAM
```

**Edit pg_hba.conf for LAN Access:**
```bash
sudo nano /etc/postgresql/14/main/pg_hba.conf

# Add these lines for LAN access (replace with your network range)
# TYPE  DATABASE        USER            ADDRESS                 METHOD
host    all             all             192.168.1.0/24          md5
host    all             all             10.0.0.0/8              md5
host    all             all             172.16.0.0/12           md5
```

**Restart PostgreSQL:**
```bash
sudo systemctl restart postgresql
```

#### Step 1.3: Create Database and User

```bash
# Login to PostgreSQL
sudo -u postgres psql

# Create database
CREATE DATABASE gst_compliance_db;

# Create user with strong password
CREATE USER gst_admin WITH PASSWORD 'YourStrongPassword123!';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE gst_compliance_db TO gst_admin;

# Exit
\q
```

### Phase 2: Application Server Setup

#### Step 2.1: Install Python and Dependencies

**For Ubuntu/Debian:**
```bash
# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Create virtual environment
python3 -m venv /opt/gst_system/venv
source /opt/gst_system/venv/bin/activate

# Navigate to application directory
cd /opt/gst_system
```

**For Windows:**
```powershell
# Install Python from python.org
# Create virtual environment
python -m venv C:\gst_system\venv
C:\gst_system\venv\Scripts\activate
```

#### Step 2.2: Install Application Dependencies

```bash
# Navigate to your project directory
cd /path/to/gst_compliance_system

# Install requirements
pip install -r requirements.txt

# Install PostgreSQL adapter
pip install psycopg2-binary
```

#### Step 2.3: Configure Django for PostgreSQL

**Update settings.py:**
```python
# Database Configuration for PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gst_compliance_db',
        'USER': 'gst_admin',
        'PASSWORD': 'YourStrongPassword123!',
        'HOST': '192.168.1.100',  # Database server IP
        'PORT': '5432',
        'OPTIONS': {
            'connect_timeout': 10,
        },
    }
}

# Security settings for LAN deployment
DEBUG = False
ALLOWED_HOSTS = ['*']  # Allow all LAN access
# Or specify your LAN range: ['192.168.1.*', '10.0.0.*']

# Session settings for multi-user
SESSION_COOKIE_SECURE = False  # False if no HTTPS
CSRF_COOKIE_SECURE = False     # False if no HTTPS
SESSION_COOKIE_AGE = 7200     # 2 hours session timeout
```

#### Step 2.4: Remove External Dependencies

**Update settings.py:**
```python
# Remove Google Sheets integration
# SHEET_NAME = None
# WORKSHEET_RETURNS = None
# WORKSHEET_RISK_SCORES = None
# WORKSHEET_NOT_FILED = None

# Email configuration for LAN
EMAIL_BACKEND = 'django.core.mail.backends.file.EmailBackend'
EMAIL_FILE_PATH = '/tmp/gst_emails'
# OR configure local SMTP if available
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'localhost'
# EMAIL_PORT = 25
```

#### Step 2.5: Run Database Migrations

```bash
# Activate virtual environment
source /opt/gst_system/venv/bin/activate

# Navigate to project
cd /opt/gst_system/gst_compliance_system

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

### Phase 3: Network Configuration

#### Step 3.1: Configure Firewall

**For Ubuntu (UFW):**
```bash
# Allow PostgreSQL from application server
sudo ufw allow from 192.168.1.50 to any port 5432

# Allow Django application port
sudo ufw allow 8000/tcp

# Enable firewall
sudo ufw enable
```

**For Windows Firewall:**
1. Open Windows Defender Firewall
2. Add inbound rule for PostgreSQL (port 5432)
3. Add inbound rule for Django application (port 8000)
4. Restrict to local network IPs

#### Step 3.2: Test Database Connection

```bash
# From application server, test connection to database
psql -h 192.168.1.100 -U gst_admin -d gst_compliance_db

# If successful, you'll see PostgreSQL prompt
```

### Phase 4: Production Deployment

#### Step 4.1: Install Gunicorn

```bash
pip install gunicorn
```

#### Step 4.2: Create Gunicorn Systemd Service

**Create service file:**
```bash
sudo nano /etc/systemd/system/gst-compliance.service
```

**Service configuration:**
```ini
[Unit]
Description=GST Compliance System Django Application
After=network.target postgresql.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/gst_system/gst_compliance_system
Environment="PATH=/opt/gst_system/venv/bin"
ExecStart=/opt/gst_system/venv/bin/gunicorn \
          --workers 3 \
          --bind 0.0.0.0:8000 \
          gst_compliance_system.wsgi:application

[Install]
WantedBy=multi-user.target
```

**Enable and start service:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable gst-compliance
sudo systemctl start gst-compliance
sudo systemctl status gst-compliance
```

#### Step 4.3: Configure Nginx (Optional but Recommended)

**Install Nginx:**
```bash
sudo apt install nginx -y
```

**Create Nginx configuration:**
```bash
sudo nano /etc/nginx/sites-available/gst-compliance
```

**Nginx configuration:**
```nginx
server {
    listen 80;
    server_name gst-compliance.local;  # Use your server hostname

    location /static/ {
        alias /opt/gst_system/staticfiles/;
    }

    location /media/ {
        alias /opt/gst_system/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Enable site:**
```bash
sudo ln -s /etc/nginx/sites-available/gst-compliance /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Phase 5: Client Access Configuration

#### Step 5.1: Configure Client Computers

**Add to hosts file (C:\Windows\System32\drivers\etc\hosts on Windows):**
```
192.168.1.50    gst-compliance.local
```

**Or access directly via IP:**
```
http://192.168.1.50:8000
```

#### Step 5.2: Test Client Access

1. Open web browser on client computer
2. Navigate to `http://gst-compliance.local` or `http://192.168.1.50:8000`
3. Login with superuser credentials
4. Test all functionality

## 🔒 Security Configuration for LAN

### Database Security
```sql
-- Create read-only user for reporting
CREATE USER gst_report WITH PASSWORD 'ReportPassword123!';
GRANT CONNECT ON DATABASE gst_compliance_db TO gst_report;
GRANT USAGE ON SCHEMA public TO gst_report;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO gst_report;

-- Create backup user
CREATE USER gst_backup WITH PASSWORD 'BackupPassword123!';
GRANT CONNECT ON DATABASE gst_compliance_db TO gst_backup;
```

### Application Security
```python
# In settings.py - Enhanced security for LAN
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False  # Disable if no SSL
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Keep other security measures
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Rate limiting for login
LOGIN_RATE_LIMIT = '5/m'  # 5 attempts per minute
```

### Network Security
- **Network Segmentation**: Place database server in secure VLAN
- **Firewall Rules**: Restrict access to specific IPs only
- **VPN Access**: For remote users if needed
- **Network Monitoring**: Monitor for suspicious activity

## 📊 Backup Strategy

### Automated Database Backups

**Create backup script:**
```bash
#!/bin/bash
# /opt/backups/gst_backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/backups/gst_system"
DB_NAME="gst_compliance_db"
DB_USER="gst_admin"
DB_HOST="192.168.1.100"

# Create backup directory
mkdir -p $BACKUP_DIR

# Database backup
pg_dump -h $DB_HOST -U $DB_USER $DB_NAME > $BACKUP_DIR/gst_db_$DATE.sql

# Compress backup
gzip $BACKUP_DIR/gst_db_$DATE.sql

# Keep last 30 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete

echo "Backup completed: gst_db_$DATE.sql.gz"
```

**Schedule with cron:**
```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * /opt/backups/gst_backup.sh
```

### Application Backups
```bash
# Backup application files
tar -czf /opt/backups/gst_app_$(date +%Y%m%d).tar.gz /opt/gst_system
```

## 🔧 Maintenance and Monitoring

### Regular Maintenance Tasks
- **Daily**: Monitor application logs
- **Weekly**: Check database performance, review audit logs
- **Monthly**: Database maintenance (VACUUM, ANALYZE), security updates
- **Quarterly**: Full system backup testing, security audit

### Monitoring Commands
```bash
# Check PostgreSQL connections
sudo -u postgres psql -c "SELECT count(*) FROM pg_stat_activity;"

# Check database size
sudo -u postgres psql -c "SELECT pg_size_pretty(pg_database_size('gst_compliance_db'));"

# Check Gunicorn status
sudo systemctl status gst-compliance

# Check Nginx status
sudo systemctl status nginx

# View application logs
tail -f /opt/gst_system/logs/gst-compliance.log
```

## 🚨 Troubleshooting

### Common Issues

#### Database Connection Failed
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check firewall
sudo ufw status

# Test connection
psql -h 192.168.1.100 -U gst_admin -d gst_compliance_db
```

#### Application Not Accessible
```bash
# Check Gunicorn status
sudo systemctl status gst-compliance

# Check Nginx status
sudo systemctl status nginx

# Check firewall
sudo ufw status

# View logs
sudo journalctl -u gst-compliance -f
```

#### Performance Issues
```bash
# Check database performance
sudo -u postgres psql -c "SELECT * FROM pg_stat_activity;"

# Check slow queries
sudo -u postgres psql -c "SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;"

# Restart services
sudo systemctl restart gst-compliance
sudo systemctl restart postgresql
```

## 📋 User Management

### Create User Accounts
```bash
# Activate virtual environment
source /opt/gst_system/venv/bin/activate

# Navigate to project
cd /opt/gst_system/gst_compliance_system

# Create superuser
python manage.py createsuperuser

# Or create regular users through admin interface
# Access: http://gst-compliance.local/admin/
```

### Configure User Permissions
- Use Django admin interface to assign roles
- Set granular permissions based on user responsibilities
- Regular review of user access rights

## 🎯 Performance Optimization

### Database Optimization
```sql
-- Regular vacuum and analyze
VACUUM ANALYZE;

-- Check table sizes
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Create indexes on frequently queried columns
CREATE INDEX idx_gstin ON taxpayers_taxpayermaster(gstin);
CREATE INDEX idx_tax_period ON returns_gstreturn(tax_period);
```

### Application Optimization
```python
# In settings.py - Performance settings
DATABASES['default']['OPTIONS'] = {
    'connect_timeout': 10,
    'options': '-c statement_timeout=30000',
}

# Enable connection pooling if needed
# Install: pip install django-db-geventpool
```

## ✅ Setup Verification Checklist

### Database Server
- [ ] PostgreSQL installed and running
- [ ] Database created (gst_compliance_db)
- [ ] User created with proper permissions
- [ ] Network access configured
- [ ] Firewall rules configured
- [ ] Backup script scheduled

### Application Server
- [ ] Python and virtual environment installed
- [ ] Dependencies installed
- [ ] Database connection configured
- [ ] Migrations run successfully
- [ ] Static files collected
- [ ] Gunicorn service configured
- [ ] Nginx configured (if using)
- [ ] Firewall rules configured

### Client Access
- [ ] Client can access application via browser
- [ ] User authentication working
- [ ] All functionality tested
- [ ] Performance acceptable
- [ ] Network connectivity stable

### Security
- [ ] Strong passwords configured
- [ ] Network access restricted
- [ ] Firewall rules active
- [ ] Backup system working
- [ ] Audit logging enabled
- [ ] Security monitoring configured

## 🎉 Conclusion

Your GST Compliance System is now configured as an internal LAN SQL-based application with:

- **Centralized PostgreSQL database** for reliable data management
- **Multi-user access** across your government network
- **Robust backup system** for data protection
- **Secure network configuration** for government deployment
- **Scalable architecture** for future growth

The system provides a secure, efficient solution for GST compliance management without requiring internet connectivity or external dependencies.

---

**Version**: 1.0
**Created**: 2026-08-14
**Status**: ✅ Ready for LAN Deployment