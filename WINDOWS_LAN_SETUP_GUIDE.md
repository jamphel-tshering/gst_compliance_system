# GST Compliance System - Windows LAN SQL Setup Guide

## 🎯 Overview
Setup the GST Compliance System on Windows for internal LAN deployment with PostgreSQL database.

## 🏗️ Windows Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              Windows Internal Network (LAN)                  │
│                                                              │
│  ┌──────────────┐         ┌──────────────┐                │
│  │   Database   │◄────────┤ Application  │                │
│  │   Server     │         │   Server     │                │
│  │ PostgreSQL   │         │   Django     │                │
│  │   :5432      │         │   :8000      │                │
│  │  (Windows)   │         │  (Windows)   │                │
│  └──────────────┘         └──────────────┘                │
│         │                         │                         │
│         │                         │                         │
│         └──────────┬──────────────┘                         │
│                    │                                       │
│                    ▼                                       │
│         ┌──────────────────────┐                          │
│         │   Client Computers  │                          │
│         │   (Windows)          │                          │
│         │   HTTP://SERVER:8000 │                          │
│         └──────────────────────┘                          │
└─────────────────────────────────────────────────────────────┘
```

## 📦 Software Requirements

### Database Server (Windows)
- **PostgreSQL**: 14+ or 15+ for Windows
- **pgAdmin**: Database management tool
- **Windows Server**: 2019+ or Windows 10/11 Pro

### Application Server (Windows)
- **Python**: 3.10+ for Windows
- **PostgreSQL client library**: psycopg2-binary
- **Django**: 6.1
- ** waitress**: Production WSGI server for Windows

### Client Computers
- **Windows**: 10/11
- **Browser**: Chrome, Firefox, Edge
- **Network**: LAN connectivity

## 🚀 Step-by-Step Windows Setup

### Phase 1: Database Server Setup

#### Step 1.1: Install PostgreSQL on Windows

1. **Download PostgreSQL Installer**
   - Visit: https://www.postgresql.org/download/windows/
   - Download the latest version (14+ or 15+)

2. **Run PostgreSQL Installer**
   - Select installation directory (default: `C:\Program Files\PostgreSQL\15`)
   - Set strong password for `postgres` user
   - Select port `5432` (default)
   - Select components: PostgreSQL Server, pgAdmin 4, Command Line Tools
   - Complete installation

3. **Configure PostgreSQL for Network Access**

   **Edit postgresql.conf:**
   ```
   Location: C:\Program Files\PostgreSQL\15\data\postgresql.conf
   
   Find and modify:
   listen_addresses = '*'          # Listen on all interfaces
   port = 5432
   max_connections = 100
   ```

   **Edit pg_hba.conf:**
   ```
   Location: C:\Program Files\PostgreSQL\15\data\pg_hba.conf
   
   Add these lines at the end:
   # TYPE  DATABASE        USER            ADDRESS                 METHOD
   host    all             all             192.168.1.0/24          md5
   host    all             all             10.0.0.0/8              md5
   host    all             all             172.16.0.0/12           md5
   ```

4. **Restart PostgreSQL Service**
   - Open Services (`services.msc`)
   - Find `postgresql-x64-15` service
   - Restart the service

#### Step 1.2: Create Database and User

1. **Open pgAdmin 4**
   - Launch pgAdmin from Start Menu
   - Connect to your PostgreSQL server with postgres user

2. **Create Database**
   - Right-click on Databases → Create → Database
   - Name: `gst_compliance_db`
   - Click Save

3. **Create User**
   - Right-click on Login/Group Roles → Create → Login/Group Role
   - Name: `gst_admin`
   - Password: `YourStrongPassword123!`
   - Privileges: Can login
   - Click Save

4. **Grant Privileges**
   - Right-click on `gst_compliance_db` database
   - Properties → Privileges
   - Add `gst_admin` user
   - Grant ALL privileges
   - Click Save

### Phase 2: Application Server Setup

#### Step 2.1: Install Python on Windows

1. **Download Python**
   - Visit: https://www.python.org/downloads/
   - Download Python 3.10+ for Windows

2. **Install Python**
   - Run installer
   - **IMPORTANT**: Check "Add Python to PATH"
   - Complete installation

3. **Verify Installation**
   ```cmd
   python --version
   pip --version
   ```

#### Step 2.2: Create Project Directory

```cmd
# Create directory
mkdir C:\gst_system
cd C:\gst_system

# Copy your project files to this directory
# Or clone from repository if applicable
```

#### Step 2.3: Create Virtual Environment

```cmd
# Navigate to project directory
cd C:\gst_system\gst_compliance_system

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

#### Step 2.4: Install Dependencies

```cmd
# Ensure virtual environment is activated
venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Install PostgreSQL adapter
pip install psycopg2-binary

# Install waitress for Windows production server
pip install waitress
```

#### Step 2.5: Configure Django for PostgreSQL

**Update settings.py:**
```python
# Database Configuration for PostgreSQL on Windows
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gst_compliance_db',
        'USER': 'gst_admin',
        'PASSWORD': 'YourStrongPassword123!',  # Change this!
        'HOST': '192.168.1.100',  # Database server IP
        'PORT': '5432',
        'OPTIONS': {
            'connect_timeout': 10,
        },
    }
}

# Security settings for LAN
DEBUG = False
ALLOWED_HOSTS = ['*']  # Or specify your LAN range

# Session settings
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_AGE = 7200  # 2 hours
```

#### Step 2.6: Run Database Migrations

```cmd
# Ensure virtual environment is activated
venv\Scripts\activate

# Navigate to project
cd C:\gst_system\gst_compliance_system

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic
```

### Phase 3: Windows Service Configuration

#### Step 3.1: Create Windows Service Script

**Create file: `C:\gst_system\gst_compliance_system\run_service.py`**
```python
from waitress import serve
from django.core.wsgi import get_wsgi_application
import os
import sys

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')

# Get Django application
application = get_wsgi_application()

# Serve with waitress
serve(application, host='0.0.0.0', port=8000, threads=4)
```

#### Step 3.2: Create Windows Service (Optional)

**Option A: Using NSSM (Non-Sucking Service Manager)**

1. **Download NSSM**
   - Visit: https://nssm.cc/download
   - Download and extract

2. **Install Service**
   ```cmd
   # Navigate to NSSM directory
   cd C:\path\to\nssm

   # Install service
   nssm install GSTCompliance C:\gst_system\venv\Scripts\python.exe C:\gst_system\gst_compliance_system\run_service.py

   # Configure service
   nssm set GSTCompliance AppDirectory C:\gst_system\gst_compliance_system
   nssm set GSTCompliance DisplayName GST Compliance System
   nssm set GSTCompliance Description GST Compliance System Django Application
   nssm set GSTCompliance Start SERVICE_AUTO_START

   # Start service
   nssm start GSTCompliance
   ```

**Option B: Using Task Scheduler**

1. **Open Task Scheduler**
   - Press Win+R, type `taskschd.msc`

2. **Create Basic Task**
   - Name: "GST Compliance System"
   - Trigger: "At startup"
   - Action: "Start a program"
   - Program: `C:\gst_system\venv\Scripts\python.exe`
   - Arguments: `C:\gst_system\gst_compliance_system\run_service.py`
   - Start in: `C:\gst_system\gst_compliance_system`

#### Step 3.3: Manual Startup (For Testing)

```cmd
# Activate virtual environment
C:\gst_system\venv\Scripts\activate

# Navigate to project
cd C:\gst_system\gst_compliance_system

# Run Django development server
python manage.py runserver 0.0.0.0:8000

# OR run with waitress for production
python run_service.py
```

### Phase 4: Windows Firewall Configuration

#### Step 4.1: Configure Windows Firewall

1. **Open Windows Firewall**
   - Press Win+R, type `wf.msc`

2. **Add Inbound Rule for Django**
   - Inbound Rules → New Rule
   - Port → TCP → Specific local ports: 8000
   - Allow the connection
   - Profile: Domain, Private
   - Name: "GST Compliance System"

3. **Add Inbound Rule for PostgreSQL** (if on same server)
   - Inbound Rules → New Rule
   - Port → TCP → Specific local ports: 5432
   - Allow the connection
   - Profile: Domain, Private
   - Name: "PostgreSQL"

### Phase 5: Client Access Configuration

#### Step 5.1: Configure Client Computers

**Option A: Using Hosts File**
```
# Edit C:\Windows\System32\drivers\etc\hosts
# Add line:
192.168.1.50    gst-compliance.local
```

**Option B: Direct IP Access**
```
http://192.168.1.50:8000
```

#### Step 5.2: Test Client Access

1. Open web browser on client computer
2. Navigate to `http://gst-compliance.local:8000` or `http://192.168.1.50:8000`
3. Login with superuser credentials
4. Test all functionality

## 🔒 Windows Security Configuration

### Database Security
```sql
-- Open pgAdmin and run in Query Tool
-- Create read-only user for reporting
CREATE USER gst_report WITH PASSWORD 'ReportPassword123!';
GRANT CONNECT ON DATABASE gst_compliance_db TO gst_report;
GRANT USAGE ON SCHEMA public TO gst_report;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO gst_report;

-- Create backup user
CREATE USER gst_backup WITH PASSWORD 'BackupPassword123!';
GRANT CONNECT ON DATABASE gst_compliance_db TO gst_backup;
```

### Windows Security
- **User Account Control**: Keep enabled
- **Windows Defender**: Add exclusions for application directory
- **Network Profile**: Set to Private for LAN
- **Windows Updates**: Keep system updated

### Application Security
```python
# In settings.py - Enhanced security
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Rate limiting for login
LOGIN_RATE_LIMIT = '5/m'
```

## 📊 Backup Strategy for Windows

### Automated Database Backups

**Create batch file: `C:\gst_system\backups\gst_backup.bat`**
```batch
@echo off
set DATE=%date:~10,4%%date:~4,2%%date:~7,2%
set TIME=%time:~0,2%%time:~3,2%
set BACKUP_DIR=C:\gst_system\backups
set DB_NAME=gst_compliance_db
set DB_USER=gst_admin
set DB_HOST=192.168.1.100
set DB_PORT=5432

set PGPASSWORD=YourStrongPassword123!

mkdir %BACKUP_DIR% 2>nul

pg_dump -h %DB_HOST% -p %DB_PORT% -U %DB_USER% %DB_NAME% > %BACKUP_DIR%\gst_db_%DATE%_%TIME%.sql

7z a -tzip %BACKUP_DIR%\gst_db_%DATE%_%TIME%.sql.zip %BACKUP_DIR%\gst_db_%DATE%_%TIME%.sql
del %BACKUP_DIR%\gst_db_%DATE%_%TIME%.sql

forfiles /p %BACKUP_DIR% /m *.sql.zip /d -30 /c "cmd /c del @path"

echo Backup completed: gst_db_%DATE%_%TIME%.sql.zip
```

### Schedule with Windows Task Scheduler

1. **Open Task Scheduler**
   - Press Win+R, type `taskschd.msc`

2. **Create Scheduled Task**
   - Name: "GST Database Backup"
   - Trigger: Daily at 2:00 AM
   - Action: Start a program
   - Program: `C:\gst_system\backups\gst_backup.bat`
   - Start in: `C:\gst_system\backups`

## 🔧 Windows Maintenance

### Regular Maintenance Tasks
- **Daily**: Check application logs
- **Weekly**: Review database performance, check disk space
- **Monthly**: Windows updates, database maintenance
- **Quarterly**: Full backup testing, security review

### Monitoring Commands
```cmd
# Check PostgreSQL service
sc query postgresql-x64-15

# Check Django service (if using NSSM)
nssm status GSTCompliance

# Check disk space
dir C:\gst_system

# View application logs
type C:\gst_system\logs\gst-compliance.log
```

## 🚨 Windows Troubleshooting

### Common Issues

#### Database Connection Failed
```cmd
# Check PostgreSQL service
sc query postgresql-x64-15

# Test connection
psql -h 192.168.1.100 -U gst_admin -d gst_compliance_db

# Check Windows Firewall
wf.msc
```

#### Application Not Accessible
```cmd
# Check if Django is running
netstat -an | findstr :8000

# Check Windows Firewall
wf.msc

# Restart service
nssm restart GSTCompliance
```

#### Performance Issues
```cmd
# Check system resources
taskmgr

# Check PostgreSQL connections
psql -U postgres -c "SELECT count(*) FROM pg_stat_activity;"

# Restart services
nssm restart GSTCompliance
```

## 📋 Windows Setup Verification Checklist

### Database Server
- [ ] PostgreSQL installed and running
- [ ] Database created (gst_compliance_db)
- [ ] User created with proper permissions
- [ ] Network access configured
- [ ] Windows Firewall configured
- [ ] Backup script scheduled

### Application Server
- [ ] Python and virtual environment installed
- [ ] Dependencies installed
- [ ] Database connection configured
- [ ] Migrations run successfully
- [ ] Static files collected
- [ ] Windows service configured
- [ ] Windows Firewall configured

### Client Access
- [ ] Client can access application via browser
- [ ] User authentication working
- [ ] All functionality tested
- [ ] Performance acceptable
- [ ] Network connectivity stable

### Security
- [ ] Strong passwords configured
- [ ] Windows Firewall active
- [ ] Windows Defender configured
- [ ] Backup system working
- [ ] Audit logging enabled
- [ ] Windows Updates enabled

## 🎉 Conclusion

Your GST Compliance System is now configured as a Windows-based internal LAN SQL application with:

- **PostgreSQL database** for reliable data management
- **Multi-user access** across your Windows network
- **Windows service integration** for automatic startup
- **Robust backup system** for data protection
- **Windows-native security** for government deployment

The system provides a secure, efficient solution for GST compliance management using familiar Windows infrastructure.

---

**Version**: 1.0
**Created**: 2026-08-14
**Status**: ✅ Ready for Windows LAN Deployment