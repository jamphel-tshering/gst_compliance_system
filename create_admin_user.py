import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from core.models import User

# Check if admin user exists
try:
    admin = User.objects.get(username='admin')
    print(f"Admin user exists: {admin.email}")
    print(f"Is active: {admin.is_active}")
    print(f"Is staff: {admin.is_staff}")
    print(f"Is superuser: {admin.is_superuser}")
except User.DoesNotExist:
    print("Admin user does not exist. Creating...")
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@gst-system.local',
        password='admin123'
    )
    print(f"Admin user created: {admin.email}")
    print("Username: admin")
    print("Password: admin123")

# List all users
print("\nAll users in system:")
for user in User.objects.all():
    print(f"- {user.username} ({user.email}) - Active: {user.is_active}")
