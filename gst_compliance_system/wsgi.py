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

# Create admin user if not exists
from django.contrib.auth import get_user_model
User = get_user_model()

try:
    if not User.objects.filter(username='jamphel.tshering').exists():
        User.objects.create_superuser(
            username='jamphel.tshering',
            email='jimmes2008@gmail.com',
            password='Admin@123'
        )
        print("Superuser created: jamphel.tshering / Admin@123")
    else:
        print("Superuser already exists")
except Exception as e:
    print(f"User creation error: {e}")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
