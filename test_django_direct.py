import os
import sys
import django

# Add project to path
sys.path.insert(0, 'C:/Users/jamphelt_mongar/gst_compliance_system')

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')

# Setup Django
django.setup()

# Test Django configuration
from django.conf import settings

print("Django Configuration Test")
print("=" * 50)
print(f"DEBUG: {settings.DEBUG}")
print(f"SECRET_KEY: {settings.SECRET_KEY[:20]}...")
print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
print(f"DATABASE: {settings.DATABASES}")
print("=" * 50)

# Test database connection
from django.db import connection
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Database tables: {len(tables)}")
        print("First 5 tables:", [t[0] for t in tables[:5]])
except Exception as e:
    print(f"Database error: {e}")

print("=" * 50)
print("Django configuration test completed successfully!")
