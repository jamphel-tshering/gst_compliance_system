"""
PostgreSQL LAN Configuration for GST Compliance System
Copy this configuration to settings.py and modify the database settings
"""

# Database Configuration for PostgreSQL LAN Deployment
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gst_compliance_db',          # Database name
        'USER': 'gst_admin',                   # Database user
        'PASSWORD': 'YourStrongPassword123!',  # STRONG PASSWORD - CHANGE THIS!
        'HOST': '192.168.1.100',              # Database server IP address
        'PORT': '5432',                       # PostgreSQL port
        'OPTIONS': {
            'connect_timeout': 10,             # Connection timeout in seconds
        },
    }
}

# Security settings for LAN deployment
DEBUG = False  # Always False in production
ALLOWED_HOSTS = ['*']  # Allow all LAN access
# Or specify your LAN range: ['192.168.1.*', '10.0.0.*', 'gst-compliance.local']

# Session settings for multi-user environment
SESSION_COOKIE_SECURE = False  # Set to True if using HTTPS
CSRF_COOKIE_SECURE = False     # Set to True if using HTTPS
SESSION_COOKIE_AGE = 7200     # 2 hours session timeout
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Email configuration for LAN (file-based or local SMTP)
EMAIL_BACKEND = 'django.core.mail.backends.file.EmailBackend'
EMAIL_FILE_PATH = '/tmp/gst_emails'  # Local file storage for emails
# OR use local SMTP server if available:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'localhost'
# EMAIL_PORT = 25
# EMAIL_USE_TLS = False

# Security headers (keep even without HTTPS)
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 0  # Disable HSTS for HTTP-only LAN
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

# CORS settings for LAN access
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.1.*",    # Your LAN range
    "http://10.0.0.*",       # Alternative LAN range
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = False  # Security: Keep this False

# Media and static files for LAN
MEDIA_URL = '/media/'
MEDIA_ROOT = '/opt/gst_system/media'  # Change to your media directory
STATIC_URL = '/static/'
STATIC_ROOT = '/opt/gst_system/staticfiles'  # Change to your static files directory
STATICFILES_DIRS = ['/opt/gst_system/static']  # Change to your static directory

# Logging configuration for LAN
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/opt/gst_system/logs/gst-compliance.log',  # Change to your log directory
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'gst_compliance_system': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Performance settings for multi-user
DATABASES['default']['OPTIONS'] = {
    'connect_timeout': 10,
    'options': '-c statement_timeout=30000',  # 30 second query timeout
}

# Additional security settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True