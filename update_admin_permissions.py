"""
Script to update existing admin user with all permissions
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from core.models import User

# Get the admin user by role or by username
admin_user = User.objects.filter(role='administrator').first()

if not admin_user:
    # Try to find user with admin username
    admin_user = User.objects.filter(username='admin').first()
    if admin_user:
        print(f"Found existing user 'admin', updating to administrator role...")
        admin_user.role = 'administrator'
        admin_user.save()

if admin_user:
    print(f"Found admin user: {admin_user.email}")
    print(f"Current role: {admin_user.role}")
    
    # Grant all permissions
    admin_user.grant_all_permissions()
    admin_user.is_superuser = True
    admin_user.is_staff = True
    admin_user.save()
    
    print("[OK] All permissions granted to admin user")
    print(f"[OK] User is now superuser: {admin_user.is_superuser}")
    print(f"[OK] User is now staff: {admin_user.is_staff}")
    
    # Show access summary
    access_summary = admin_user.get_access_summary()
    print("\nAccess Summary:")
    for module, permissions in access_summary.items():
        if all(permissions.values()):
            print(f"  {module}: [OK] FULL ACCESS")
        else:
            print(f"  {module}: {permissions}")
else:
    print("No admin user found. Creating a new admin user...")
    admin_user = User.objects.create_user(
        username='admin',
        email='admin@gst.gov.bt',
        password='admin123',
        first_name='Admin',
        last_name='User',
        role='administrator'
    )
    admin_user.is_superuser = True
    admin_user.is_staff = True
    admin_user.save()
    print(f"[OK] Created admin user: {admin_user.email}")
    print(f"[OK] Default password: admin123")
