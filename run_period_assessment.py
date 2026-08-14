"""
Period-Based Risk Assessment Script
Run this script to assess taxpayers for a specific tax period range
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from compliance.risk_engine import RiskAssessmentEngine
from core.models import User

def main():
    print("Period-Based Risk Assessment")
    print("=" * 50)
    
    # Available tax periods
    tax_periods = [
        'Jan-2026', 'Feb-2026', 'Mar-2026', 'Apr-2026', 'May-2026', 'Jun-2026',
        'Jul-2026', 'Aug-2026', 'Sep-2026', 'Oct-2026', 'Nov-2026', 'Dec-2026',
        'Jan-2027', 'Feb-2027', 'Mar-2027', 'Apr-2027', 'May-2027', 'Jun-2027',
        'Jul-2027', 'Aug-2027', 'Sep-2027', 'Oct-2027', 'Nov-2027', 'Dec-2027'
    ]
    
    print("\nAvailable Tax Periods:")
    for i, period in enumerate(tax_periods, 1):
        print(f"{i}. {period}")
    
    try:
        from_period = input("\nEnter From Period (number or exact period): ").strip()
        to_period = input("Enter To Period (number or exact period): ").strip()
        
        # Convert numbers to periods
        if from_period.isdigit():
            from_period = tax_periods[int(from_period) - 1]
        if to_period.isdigit():
            to_period = tax_periods[int(to_period) - 1]
        
        print(f"\nSelected Period: {from_period} to {to_period}")
        
        # Get user
        user = User.objects.first()
        if not user:
            print("No user found. Creating default user...")
            user = User.objects.create_superuser(
                username='admin',
                email='admin@gst-system.local',
                password='admin123'
            )
            print("Default user created: admin/admin123")
        
        # Run assessment
        print(f"\nRunning risk assessment for {from_period} to {to_period}...")
        engine = RiskAssessmentEngine()
        count = engine.assess_period(from_period, to_period, user)
        
        print("=" * 50)
        print(f"Risk assessment completed!")
        print(f"Total taxpayers evaluated: {count}")
        print("=" * 50)
        
        # Show statistics
        from compliance.models import ComplianceRiskReferral
        total = ComplianceRiskReferral.objects.filter(
            assessment_from_period=from_period,
            assessment_to_period=to_period
        ).count()
        
        audit = ComplianceRiskReferral.objects.filter(
            assessment_from_period=from_period,
            assessment_to_period=to_period,
            system_decision='AUDIT'
        ).count()
        
        review = ComplianceRiskReferral.objects.filter(
            assessment_from_period=from_period,
            assessment_to_period=to_period,
            system_decision='REVIEW'
        ).count()
        
        monitor = ComplianceRiskReferral.objects.filter(
            assessment_from_period=from_period,
            assessment_to_period=to_period,
            system_decision='MONITOR'
        ).count()
        
        not_selected = ComplianceRiskReferral.objects.filter(
            assessment_from_period=from_period,
            assessment_to_period=to_period,
            system_decision='NOT SELECTED'
        ).count()
        
        print(f"\nSystem Decision Breakdown:")
        print(f"   AUDIT: {audit}")
        print(f"   REVIEW: {review}")
        print(f"   MONITOR: {monitor}")
        print(f"   NOT SELECTED: {not_selected}")
        print(f"   Total: {total}")
        
        print(f"\nYou can now view the results in the admin panel at:")
        print(f"   http://127.0.0.1:8000/admin/compliance/complianceriskreferral/")
        print(f"\nFilter by Assessment From Period: {from_period}")
        print(f"Filter by Assessment To Period: {to_period}")
        
    except KeyboardInterrupt:
        print("\nAssessment cancelled by user.")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()