import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from core.models import User

# Create admin user
admin = User.objects.create_superuser(
    username='admin',
    email='admin@gst-system.local',
    password='admin123'
)

print("Admin user created successfully!")
print("Username: admin")
print("Password: admin123")
print("Email: admin@gst-system.local")
