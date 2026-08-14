import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from core.models import User

def create_test_users():
    """Create test users with different permission profiles"""
    
    print("Creating test users with different permission profiles")
    print("=" * 70)
    
    # Generate unique employee IDs based on username
    def get_employee_id(username):
        return f"EMP{username[-2:].upper()}Z{username[:2].upper()}"
    
    # 1. Compliance Officer Profile
    compliance_officer = User.objects.create_user(
        username='compliance_officer',
        email='compliance.officer@gst.gov.bt',
        password='testpass123',
        first_name='Tashi',
        last_name='Wangmo',
        role='compliance',
        department='Compliance Division',
        employee_id=get_employee_id('compliance_officer')
    )
    # Grant compliance-specific permissions
    compliance_officer.can_view_taxpayers = True
    compliance_officer.can_view_returns = True
    compliance_officer.can_view_compliance = True
    compliance_officer.can_add_compliance = True
    compliance_officer.can_edit_compliance = True
    compliance_officer.can_view_risk_assessment = True
    compliance_officer.can_run_risk_assessment = True
    compliance_officer.can_edit_risk_assessment = True
    compliance_officer.can_view_enforcement = True
    compliance_officer.can_add_enforcement = True
    compliance_officer.can_edit_enforcement = True
    compliance_officer.can_view_reports = True
    compliance_officer.can_generate_reports = True
    compliance_officer.can_export_reports = True
    compliance_officer.is_staff = True
    compliance_officer.save()
    print(f"[OK] Created Compliance Officer: {compliance_officer.email}")
    
    # 2. Audit Officer Profile
    audit_officer = User.objects.create_user(
        username='audit_officer',
        email='audit.officer@gst.gov.bt',
        password='testpass123',
        first_name='Karma',
        last_name='Dorji',
        role='audit_refund',
        department='Audit Division',
        employee_id=get_employee_id('audit_officer')
    )
    # Grant audit-specific permissions
    audit_officer.can_view_taxpayers = True
    audit_officer.can_view_returns = True
    audit_officer.can_view_refunds = True
    audit_officer.can_add_refunds = True
    audit_officer.can_edit_refunds = True
    audit_officer.can_view_audit = True
    audit_officer.can_create_audit = True
    audit_officer.can_edit_audit = True
    audit_officer.can_view_risk_assessment = True
    audit_officer.can_view_enforcement = True
    audit_officer.can_view_reports = True
    audit_officer.can_generate_reports = True
    audit_officer.can_export_reports = True
    audit_officer.is_staff = True
    audit_officer.save()
    print(f"[OK] Created Audit Officer: {audit_officer.email}")
    
    # 3. Section Head Profile
    section_head = User.objects.create_user(
        username='section_head',
        email='section.head@gst.gov.bt',
        password='testpass123',
        first_name='Sonam',
        last_name='Tshering',
        role='section_head',
        department='Compliance Division',
        employee_id=get_employee_id('section_head')
    )
    # Grant section head permissions
    section_head.can_view_taxpayers = True
    section_head.can_view_returns = True
    section_head.can_view_refunds = True
    section_head.can_view_compliance = True
    section_head.can_edit_compliance = True
    section_head.can_view_risk_assessment = True
    section_head.can_edit_risk_assessment = True
    section_head.can_approve_risk_assessment = True
    section_head.can_view_enforcement = True
    section_head.can_edit_enforcement = True
    section_head.can_view_audit = True
    section_head.can_edit_audit = True
    section_head.can_approve_audit = True
    section_head.can_view_reports = True
    section_head.can_generate_reports = True
    section_head.can_export_reports = True
    section_head.can_view_users = True
    section_head.can_edit_users = True
    section_head.can_manage_permissions = True
    section_head.can_view_settings = True
    section_head.can_import_data = True
    section_head.can_export_data = True
    section_head.is_staff = True
    section_head.save()
    print(f"[OK] Created Section Head: {section_head.email}")
    
    # 4. Registration Officer Profile
    registration_officer = User.objects.create_user(
        username='registration_officer',
        email='registration.officer@gst.gov.bt',
        password='testpass123',
        first_name='Deki',
        last_name='Pema',
        role='registration_enquiry',
        department='Registration Division',
        employee_id=get_employee_id('registration_officer')
    )
    # Grant registration-specific permissions
    registration_officer.can_view_taxpayers = True
    registration_officer.can_add_taxpayers = True
    registration_officer.can_edit_taxpayers = True
    registration_officer.can_view_returns = True
    registration_officer.can_add_returns = True
    registration_officer.can_edit_returns = True
    registration_officer.can_view_reports = True
    registration_officer.can_generate_reports = True
    registration_officer.can_export_reports = True
    registration_officer.is_staff = True
    registration_officer.save()
    print(f"[OK] Created Registration Officer: {registration_officer.email}")
    
    # 5. Read-Only Viewer Profile
    viewer = User.objects.create_user(
        username='viewer',
        email='viewer@gst.gov.bt',
        password='testpass123',
        first_name='Thinley',
        last_name='Namgyel',
        role='compliance',
        department='Management',
        employee_id=get_employee_id('viewer')
    )
    # Grant view-only permissions
    viewer.can_view_taxpayers = True
    viewer.can_view_returns = True
    viewer.can_view_refunds = True
    viewer.can_view_compliance = True
    viewer.can_view_risk_assessment = True
    viewer.can_view_enforcement = True
    viewer.can_view_audit = True
    viewer.can_view_reports = True
    viewer.is_staff = True
    viewer.save()
    print(f"[OK] Created Read-Only Viewer: {viewer.email}")
    
    print()
    print("=" * 70)
    print("Successfully created 5 test users with different permission profiles")
    print()
    print("User Profiles Created:")
    print("1. Compliance Officer - Full compliance and enforcement access")
    print("2. Audit Officer - Audit and refund specific access")
    print("3. Section Head - Management and approval access")
    print("4. Registration Officer - Taxpayer and returns management")
    print("5. Read-Only Viewer - View-only access to all modules")
    print()
    print("You can now:")
    print("1. Go to the User admin page")
    print("2. Edit any user to see their permission checkboxes")
    print("3. Modify permissions as needed")
    print("4. Create custom permission profiles for specific roles")

if __name__ == "__main__":
    create_test_users()