"""
Script to reset admin password
"""
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from core.models import User

print("=== Reset Admin Password ===")
print()

try:
    admin_user = User.objects.get(username='admin')
    new_password = 'admin123'  # Simple default password
    
    admin_user.set_password(new_password)
    admin_user.save()
    
    print(f"Password reset successfully!")
    print(f"Username: {admin_user.username}")
    print(f"New Password: {new_password}")
    print(f"Email: {admin_user.email}")
    print()
    print("You can now login at: http://127.0.0.1:8001/login/")
    print("Please change this password after your first login for security.")
    
except User.DoesNotExist:
    print("Admin user not found. Creating a new admin user...")
    User.objects.create_superuser(
        username='admin',
        email='admin@gst-system.local',
        password='admin123',
        role='admin'
    )
    print("Admin user created successfully!")
    print(f"Username: admin")
    print(f"Password: admin123")
    print(f"Email: admin@gst-system.local")