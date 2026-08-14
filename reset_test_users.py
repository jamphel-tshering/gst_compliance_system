import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from core.models import User

# Delete existing test users
test_usernames = ['compliance_officer', 'audit_officer', 'section_head', 'registration_officer', 'viewer']
deleted_count = User.objects.filter(username__in=test_usernames).delete()[0]
print(f"Deleted {deleted_count} existing test users")