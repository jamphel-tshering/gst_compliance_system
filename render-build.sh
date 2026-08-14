#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from django.core.management import call_command

print("Running migrations...")
call_command('migrate', '--noinput')

print("Creating superuser if not exists...")
from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@gst-system.local',
        password='admin123'
    )
    print("Superuser created: admin/admin123")
else:
    print("Superuser already exists")

print("Build complete!")
