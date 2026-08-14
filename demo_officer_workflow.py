import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from compliance.models import ComplianceRiskReferral
from core.models import User
from django.db import connection

def demo_officer_workflow():
    """Demonstrate section head approval and officer assignment workflow"""
    
    print("Demonstrating Section Head Approval and Officer Assignment Workflow")
    print("=" * 70)
    
    # Get test high-risk taxpayers for demo
    test_gstins = ['TEST001', 'TEST002', 'TEST003', 'TEST004', 'TEST005']
    
    # Get first user to act as section head
    section_head = User.objects.first()
    if not section_head:
        print("No users found in database. Please create a user first.")
        return
    
    print(f"Using {section_head.username} as Section Head")
    print()
    
    # Step 1: Section Head Review and Approval
    print("Step 1: Section Head Review and Approval")
    print("-" * 70)
    
    for gstin in test_gstins:
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE compliance_complianceriskreferral 
                    SET section_head_review = %s, 
                        section_head_approval = %s, 
                        section_head_review_date = %s,
                        section_head_id = %s
                    WHERE gstin = %s AND assessment_from_period = '2026-05-01'
                """, [
                    f"Section head review for {gstin} - High risk confirmed. Recommend field audit.",
                    'Approved',
                    datetime.now(),
                    section_head.id,
                    gstin
                ])
            print(f"[OK] {gstin}: Section head approved for field audit")
        except Exception as e:
            print(f"[ERROR] {gstin}: Error - {e}")
    
    print()
    
    # Step 2: Officer Assignment
    print("Step 2: Officer Assignment for Field Audit")
    print("-" * 70)
    
    # Get another user to act as officer
    officers = User.objects.all()
    if len(officers) < 2:
        print("Need at least 2 users to demonstrate officer assignment. Creating demo scenario with same user.")
        officers = [section_head] * 5
    else:
        officers = officers[1:6]  # Get next 5 users as officers
    
    assignments = zip(test_gstins, officers)
    
    for gstin, officer in assignments:
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE compliance_complianceriskreferral 
                    SET assigned_officer_id = %s,
                        assignment_date = %s,
                        assignment_status = %s
                    WHERE gstin = %s AND assessment_from_period = '2026-05-01'
                """, [
                    officer.id,
                    datetime.now(),
                    'Assigned',
                    gstin
                ])
            print(f"[OK] {gstin}: Assigned to officer {officer.username}")
        except Exception as e:
            print(f"[ERROR] {gstin}: Error - {e}")
    
    print()
    
    # Step 3: Officer Comments and Recommendations
    print("Step 3: Officer Comments and Recommendations")
    print("-" * 70)
    
    officer_comments = [
        "Taxpayer has history of non-filing. Recommend comprehensive audit of last 3 years.",
        "Large business with complex transactions. Suggest reviewing ITC claims and sales reporting.",
        "New taxpayer with immediate non-filing pattern. Need verification of business activity.",
        "High turnover business. Focus on transaction matching and cross-verification.",
        "Multiple payment defaults. Priority audit with enforcement action recommended."
    ]
    
    for gstin, comment in zip(test_gstins, officer_comments):
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE compliance_complianceriskreferral 
                    SET officer_comments = %s,
                        officer_recommendation = %s,
                        officer_recommendation_date = %s
                    WHERE gstin = %s AND assessment_from_period = '2026-05-01'
                """, [
                    comment,
                    'Proceed with Audit',
                    datetime.now(),
                    gstin
                ])
            print(f"[OK] {gstin}: Officer added comments and recommendation")
        except Exception as e:
            print(f"[ERROR] {gstin}: Error - {e}")
    
    print()
    print("=" * 70)
    print("Workflow Demo Complete!")
    print()
    print("Summary:")
    print(f"- {len(test_gstins)} referrals approved by Section Head")
    print(f"- {len(test_gstins)} referrals assigned to officers")
    print(f"- {len(test_gstins)} officer comments and recommendations added")
    print()
    print("You can now:")
    print("1. Go to the Compliance Risk & Referral admin page")
    print("2. Search for TEST001-TEST005")
    print("3. View the Section Head Review & Delegation section")
    print("4. View the Officer Comments & Recommendation section")
    print("5. See the assigned officers and their recommendations")

if __name__ == "__main__":
    demo_officer_workflow()