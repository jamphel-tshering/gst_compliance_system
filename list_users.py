"""
Script to list all users in the GST Compliance System
"""
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from core.models import User

print("=== GST Compliance System Users ===")
print()

users = User.objects.all()
if users.exists():
    for user in users:
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"Role: {user.role}")
        print(f"Is Active: {user.is_active}")
        print("-" * 40)
else:
    print("No users found in the system.")
    print("You may need to create a superuser.")
    print("Run: py manage.py createsuperuser")

print("\n=== Reset Password Instructions ===")
print("To reset a password, run:")
print("py manage.py shell")
print("Then execute:")
print("from core.models import User")
print("user = User.objects.get(username='your_username')")
print("user.set_password('new_password')")
print("user.save()")