import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from core.models import User
from django.db import connection

def setup_admin_permissions():
    """Set up comprehensive permissions for the admin user"""
    
    print("Setting up comprehensive access control for admin user")
    print("=" * 70)
    
    # Get the admin user
    try:
        admin_user = User.objects.get(username='admin')
        print(f"Found admin user: {admin_user.email}")
    except User.DoesNotExist:
        print("Admin user not found. Please create an admin user first.")
        return
    
    # Grant all permissions to admin user
    permissions_to_grant = [
        # Taxpayer Module
        'can_view_taxpayers', 'can_add_taxpayers', 'can_edit_taxpayers', 'can_delete_taxpayers',
        # GST Returns Module
        'can_view_returns', 'can_add_returns', 'can_edit_returns', 'can_delete_returns',
        # Refunds Module
        'can_view_refunds', 'can_add_refunds', 'can_edit_refunds', 'can_delete_refunds',
        # Compliance Module
        'can_view_compliance', 'can_add_compliance', 'can_edit_compliance', 'can_delete_compliance',
        # Risk Assessment Module
        'can_view_risk_assessment', 'can_run_risk_assessment', 'can_edit_risk_assessment', 'can_approve_risk_assessment',
        # Enforcement & Recovery Module
        'can_view_enforcement', 'can_add_enforcement', 'can_edit_enforcement', 'can_delete_enforcement',
        # Audit Module
        'can_view_audit', 'can_create_audit', 'can_edit_audit', 'can_approve_audit',
        # Reports Module
        'can_view_reports', 'can_generate_reports', 'can_export_reports',
        # User Management
        'can_view_users', 'can_add_users', 'can_edit_users', 'can_delete_users', 'can_manage_permissions',
        # System Settings
        'can_view_settings', 'can_edit_settings',
        # Data Import/Export
        'can_import_data', 'can_export_data',
    ]
    
    # Update admin user with all permissions
    for permission in permissions_to_grant:
        setattr(admin_user, permission, True)
    
    admin_user.save()
    
    print(f"[OK] Granted {len(permissions_to_grant)} permissions to admin user")
    print()
    print("Admin user now has full access to all modules")
    print()
    print("Permission Summary:")
    print("- Taxpayer Module: Full Access")
    print("- GST Returns Module: Full Access")
    print("- Refunds Module: Full Access")
    print("- Compliance Module: Full Access")
    print("- Risk Assessment Module: Full Access")
    print("- Enforcement & Recovery Module: Full Access")
    print("- Audit Module: Full Access")
    print("- Reports Module: Full Access")
    print("- User Management: Full Access")
    print("- System Settings: Full Access")
    print("- Data Import/Export: Full Access")
    print()
    print("You can now:")
    print("1. Go to the User admin page")
    print("2. Edit any user to see the granular permission checkboxes")
    print("3. Grant/revoke specific permissions for each module")
    print("4. Create custom access profiles for different user roles")

if __name__ == "__main__":
    setup_admin_permissions()