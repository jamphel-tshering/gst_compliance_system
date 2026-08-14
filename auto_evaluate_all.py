"""
Auto-Evaluate All Taxpayers
Run this script to automatically evaluate all taxpayers using the risk engine
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from compliance.risk_engine import RiskAssessmentEngine
from core.models import User

def main():
    print("Starting Auto-Evaluation of All Taxpayers...")
    print("=" * 50)
    
    # Get or create a default user
    user = User.objects.first()
    if not user:
        print("No user found. Creating default user...")
        user = User.objects.create_superuser(
            username='admin',
            email='admin@gst-system.local',
            password='admin123'
        )
        print("Default user created: admin/admin123")
    
    # Run the risk engine
    engine = RiskAssessmentEngine()
    count = engine.assess_all_returns(user)
    
    print("=" * 50)
    print(f"Auto-evaluation completed!")
    print(f"Total taxpayers evaluated: {count}")
    print("=" * 50)
    
    # Show statistics
    from compliance.models import ComplianceRiskReferral
    total = ComplianceRiskReferral.objects.count()
    audit = ComplianceRiskReferral.objects.filter(system_decision='AUDIT').count()
    review = ComplianceRiskReferral.objects.filter(system_decision='REVIEW').count()
    monitor = ComplianceRiskReferral.objects.filter(system_decision='MONITOR').count()
    not_selected = ComplianceRiskReferral.objects.filter(system_decision='NOT SELECTED').count()
    
    print(f"\nSystem Decision Breakdown:")
    print(f"   AUDIT: {audit}")
    print(f"   REVIEW: {review}")
    print(f"   MONITOR: {monitor}")
    print(f"   NOT SELECTED: {not_selected}")
    print(f"   Total: {total}")
    print("\nYou can now view the results in the admin panel at:")
    print("   http://127.0.0.1:8000/admin/compliance/complianceriskreferral/")

if __name__ == '__main__':
    main()