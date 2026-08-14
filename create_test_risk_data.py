import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from compliance.models import ComplianceRiskReferral
from django.db import connection

def create_test_risk_data():
    """Create dummy risk assessments with different risk levels for testing audit selection"""
    
    print("Creating test risk assessments for May-2026")
    print("=" * 70)
    
    # Test data for different risk levels - using comprehensive risk scoring
    test_taxpayers = [
        # Critical Risk (should be selected for AUDIT) - Non-filers with payment defaults
        {
            'gstin': 'TEST001',
            'taxpayer_name': 'Test Critical Non-Filer with Payment Default',
            'risk_score': 4.5,
            'risk_level': 'Critical',
            'system_decision': 'AUDIT',
            'risk_type': 'Filing & Payment Risk',
            'risk_indicator': 'Non Filing with Payment Default'
        },
        {
            'gstin': 'TEST002', 
            'taxpayer_name': 'Test Critical High Risk',
            'risk_score': 4.2,
            'risk_level': 'Critical',
            'system_decision': 'AUDIT',
            'risk_type': 'Filing & Payment Risk',
            'risk_indicator': 'Non Filing with Payment Default'
        },
        {
            'gstin': 'TEST003',
            'taxpayer_name': 'Test Critical Non-Filer',
            'risk_score': 4.0,
            'risk_level': 'Critical',
            'system_decision': 'AUDIT',
            'risk_type': 'Filing & Payment Risk',
            'risk_indicator': 'Non Filing with Payment Default'
        },
        
        # High Risk (should be selected for AUDIT) - Non-filers with payment issues
        {
            'gstin': 'TEST004',
            'taxpayer_name': 'Test High Risk Non-Filer',
            'risk_score': 3.8,
            'risk_level': 'High',
            'system_decision': 'AUDIT',
            'risk_type': 'Filing & Payment Risk',
            'risk_indicator': 'Non Filing with Credit Balance'
        },
        {
            'gstin': 'TEST005',
            'taxpayer_name': 'Test High Score Taxpayer',
            'risk_score': 3.5,
            'risk_level': 'High',
            'system_decision': 'AUDIT',
            'risk_type': 'Filing & Payment Risk',
            'risk_indicator': 'Non Filing'
        },
        
        # Medium Risk (should be selected for MONITOR) - Late filers with issues
        {
            'gstin': 'TEST006',
            'taxpayer_name': 'Test Medium Late Filer',
            'risk_score': 2.8,
            'risk_level': 'Medium',
            'system_decision': 'MONITOR',
            'risk_type': 'Filing & Payment Risk',
            'risk_indicator': 'Late Filing with Payment Default'
        },
        {
            'gstin': 'TEST007',
            'taxpayer_name': 'Test Medium Risk',
            'risk_score': 2.5,
            'risk_level': 'Medium',
            'system_decision': 'MONITOR',
            'risk_type': 'Filing & Payment Risk',
            'risk_indicator': 'Late Filing with Credit Balance'
        },
        {
            'gstin': 'TEST008',
            'taxpayer_name': 'Test Medium Non-Filer',
            'risk_score': 2.6,
            'risk_level': 'Medium',
            'system_decision': 'MONITOR',
            'risk_type': 'Filing & Payment Risk',
            'risk_indicator': 'Non Filer but Paid'
        },
        {
            'gstin': 'TEST009',
            'taxpayer_name': 'Test Monitor Candidate',
            'risk_score': 2.2,
            'risk_level': 'Medium',
            'system_decision': 'MONITOR',
            'risk_type': 'Filing & Payment Risk',
            'risk_indicator': 'Late Filing'
        },
        {
            'gstin': 'TEST010',
            'taxpayer_name': 'Test Medium Score',
            'risk_score': 2.0,
            'risk_level': 'Medium',
            'system_decision': 'MONITOR',
            'risk_type': 'Filing & Payment Risk',
            'risk_indicator': 'Late Filing'
        },
        
        # Low Risk (should be NOT SELECTED) - Normal filers
        {
            'gstin': 'TEST011',
            'taxpayer_name': 'Test Low Risk Filer',
            'risk_score': 0.8,
            'risk_level': 'Low',
            'system_decision': 'NOT SELECTED',
            'risk_type': 'Sales & Output GST Risk',
            'risk_indicator': 'Normal Filing'
        },
        {
            'gstin': 'TEST012',
            'taxpayer_name': 'Test Low Risk Taxpayer',
            'risk_score': 0.6,
            'risk_level': 'Low',
            'system_decision': 'NOT SELECTED',
            'risk_type': 'Sales & Output GST Risk',
            'risk_indicator': 'Normal Filing'
        },
        {
            'gstin': 'TEST013',
            'taxpayer_name': 'Test Low Score',
            'risk_score': 0.7,
            'risk_level': 'Low',
            'system_decision': 'NOT SELECTED',
            'risk_type': 'Sales & Output GST Risk',
            'risk_indicator': 'Normal Filing'
        },
    ]
    
    period = '2026-05-01'  # May-2026
    count = 0
    
    for i, taxpayer in enumerate(test_taxpayers):
        try:
            # Check if assessment already exists
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id FROM compliance_complianceriskreferral 
                    WHERE gstin = %s AND assessment_from_period = %s AND assessment_to_period = %s
                    LIMIT 1
                """, [taxpayer['gstin'], period, period])
                existing = cursor.fetchone()
            
            if existing:
                print(f"Skipping {taxpayer['gstin']} - already exists")
                continue
            
            # Generate risk ID
            risk_id = f"RR202605{100 + i}"
            
            # Risk dimensions based on comprehensive logic
            control_risk = taxpayer['risk_score'] * 0.35  # Control risk has highest weight
            detection_risk = taxpayer['risk_score'] * 0.25  # Detection risk high for payment issues
            transaction_risk = taxpayer['risk_score'] * 0.05  # Transaction risk lower weight
            inherent_risk = taxpayer['risk_score'] * 0.25  # Inherent risk baseline
            gst_behaviour_risk = taxpayer['risk_score'] * 0.10  # Behaviour risk baseline
            
            # Create the risk assessment using raw SQL to avoid decimal issues
            now = datetime.now()
            
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO compliance_complianceriskreferral 
                    (risk_id, gstin, taxpayer_name, assessment_from_period, assessment_to_period, 
                     assessment_status, risk_type, risk_indicator, risk_pattern, risk_score, 
                     risk_level, system_decision, final_selection, final_referred_to, action_status,
                     control_risk, detection_risk, transaction_risk, inherent_risk, gst_behaviour_risk,
                     assessment_date, audit_assertion, risk_reason, created_at, updated_at, assessor_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, [
                    risk_id,
                    taxpayer['gstin'],
                    taxpayer['taxpayer_name'],
                    period,
                    period,
                    'Assessment Generated',
                    taxpayer['risk_type'],
                    taxpayer['risk_indicator'],
                    'None',
                    taxpayer['risk_score'],
                    taxpayer['risk_level'],
                    taxpayer['system_decision'],
                    None,
                    None,
                    None,
                    control_risk,
                    detection_risk,
                    transaction_risk,
                    inherent_risk,
                    gst_behaviour_risk,
                    period,
                    taxpayer['risk_type'] + ' requires comprehensive audit' if taxpayer['system_decision'] == 'AUDIT' else taxpayer['risk_type'] + ' requires monitoring',
                    'Detected ' + taxpayer['risk_indicator'] + ' with risk score ' + str(taxpayer['risk_score']),
                    now,
                    now,
                    1  # Default to admin user (ID 1) as assessor
                ])
            
            count += 1
            print(f"Created test assessment for {taxpayer['gstin']} - {taxpayer['risk_level']} ({taxpayer['system_decision']})")
            
        except Exception as e:
            print(f"Error creating {taxpayer['gstin']}: {e}")
    
    print(f"\nSuccessfully created {count} test risk assessments")
    print("\nSummary:")
    print(f"- Critical Risk (AUDIT): 3 taxpayers")
    print(f"- High Risk (AUDIT): 2 taxpayers") 
    print(f"- Medium Risk (MONITOR): 5 taxpayers")
    print(f"- Low Risk (NOT SELECTED): 3 taxpayers")
    print("\nRefresh the dashboard for May-2026 to see the test data")

if __name__ == "__main__":
    create_test_risk_data()