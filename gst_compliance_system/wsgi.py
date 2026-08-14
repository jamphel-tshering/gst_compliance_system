"""
WSGI config for gst_compliance_system project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/wsgi/
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

# Run migrations on startup
from django.core.management import call_command
try:
    call_command('migrate', '--noinput', verbosity=0)
    print("Migrations completed successfully")
except Exception as e:
    print(f"Migration error: {e}")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
