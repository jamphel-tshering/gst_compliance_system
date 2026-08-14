import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from compliance.models import ComplianceRiskReferral
from audit_refund.models import AuditCase
from django.utils import timezone

def auto_create_audit_cases():
    """Automatically create audit cases from Compliance Risk where Final = AUDIT"""
    
    print("Auto-creating Audit Cases from Compliance Risk Selection")
    print("=" * 70)
    
    # Get all risk referrals with Final = AUDIT that don't have audit cases yet
    audit_risks = ComplianceRiskReferral.objects.filter(final_selection='AUDIT')
    
    print(f"Found {audit_risks.count()} risk referrals with Final = AUDIT")
    
    created_count = 0
    skipped_count = 0
    
    for risk in audit_risks:
        # Check if audit case already exists
        if AuditCase.objects.filter(risk_referral=risk).exists():
            print(f"Skipping {risk.risk_id} - audit case already exists")
            skipped_count += 1
            continue
        
        # Create audit case
        audit_case = AuditCase.objects.create(
            risk_referral=risk,
            assessment_date=risk.assessment_date,
            from_tax_period=risk.assessment_from_period,
            to_tax_period=risk.assessment_to_period,
            gstin=risk.gstin,
            taxpayer_name=risk.taxpayer_name,
            assessment_type='field_audit',  # Default to field audit
            audit_priority='high' if risk.risk_level in ['Critical', 'High'] else 'medium',
            status='referred',
            assessor=risk.assessor,
        )
        
        print(f"Created audit case {audit_case.audit_case_id} for {risk.risk_id} - {risk.taxpayer_name}")
        created_count += 1
    
    print()
    print("=" * 70)
    print(f"Summary:")
    print(f"- Created: {created_count} audit cases")
    print(f"- Skipped: {skipped_count} (already have audit cases)")
    print(f"- Total processed: {audit_risks.count()}")
    print()
    print("You can now:")
    print("1. Go to the Audit & Refund landing page: /audit_refund/")
    print("2. Access the Audit Dashboard: /audit_refund/audit/")
    print("3. View and manage audit cases in the admin")

if __name__ == "__main__":
    auto_create_audit_cases()