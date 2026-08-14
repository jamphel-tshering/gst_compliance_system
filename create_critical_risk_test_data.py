import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from compliance.models import ComplianceRiskReferral
from django.db import connection

def create_critical_risk_test_data():
    """Create test data demonstrating the new critical risk indicators"""
    
    print("Creating test data for new critical risk indicators")
    print("=" * 70)
    
    # Test data for new critical risk indicators
    critical_risk_taxpayers = [
        # 1. Consecutive Negative Returns (3 months)
        {
            'gstin': 'CRIT001',
            'taxpayer_name': 'Test Consecutive Negative Returns',
            'risk_score': 4.2,
            'risk_level': 'Critical',
            'system_decision': 'AUDIT',
            'risk_type': 'Sales & Output GST Risk',
            'risk_indicator': 'Consecutive Negative Returns'
        },
        {
            'gstin': 'CRIT002',
            'taxpayer_name': 'Test 3-Month Negative Pattern',
            'risk_score': 4.0,
            'risk_level': 'Critical',
            'system_decision': 'AUDIT',
            'risk_type': 'Sales & Output GST Risk',
            'risk_indicator': 'Consecutive Negative Returns'
        },
        
        # 2. Import & Purchase vs Sales + Stock Mismatch (ITC Fraud)
        {
            'gstin': 'CRIT003',
            'taxpayer_name': 'Test ITC Mismatch High Risk',
            'risk_score': 4.5,
            'risk_level': 'Critical',
            'system_decision': 'AUDIT',
            'risk_type': 'Purchase & ITC Risk',
            'risk_indicator': 'ITC Mismatch'
        },
        {
            'gstin': 'CRIT004',
            'taxpayer_name': 'Test Import Purchase Mismatch',
            'risk_score': 4.3,
            'risk_level': 'Critical',
            'system_decision': 'AUDIT',
            'risk_type': 'Purchase & ITC Risk',
            'risk_indicator': 'ITC Mismatch'
        },
        
        # 3. 30% Sales Variation from Previous Months
        {
            'gstin': 'CRIT005',
            'taxpayer_name': 'Test Sales Variation 30%',
            'risk_score': 3.8,
            'risk_level': 'High',
            'system_decision': 'AUDIT',
            'risk_type': 'Sales & Output GST Risk',
            'risk_indicator': 'Sales Variation'
        },
        {
            'gstin': 'CRIT006',
            'taxpayer_name': 'Test Sales Fluctuation Risk',
            'risk_score': 3.5,
            'risk_level': 'High',
            'system_decision': 'AUDIT',
            'risk_type': 'Sales & Output GST Risk',
            'risk_indicator': 'Sales Variation'
        },
        
        # 4. Frequent Return Amendments
        {
            'gstin': 'CRIT007',
            'taxpayer_name': 'Test Frequent Amendments',
            'risk_score': 3.2,
            'risk_level': 'High',
            'system_decision': 'AUDIT',
            'risk_type': 'GST Behaviour & Compliance History Risk',
            'risk_indicator': 'Frequent Amendments'
        },
        {
            'gstin': 'CRIT008',
            'taxpayer_name': 'Test Return Revision Pattern',
            'risk_score': 3.0,
            'risk_level': 'High',
            'system_decision': 'AUDIT',
            'risk_type': 'GST Behaviour & Compliance History Risk',
            'risk_indicator': 'Frequent Amendments'
        },
    ]
    
    period = '2026-05-01'  # May-2026
    count = 0
    
    for i, taxpayer in enumerate(critical_risk_taxpayers):
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
            risk_id = f"RR202605{200 + i}"
            
            # Risk dimensions based on comprehensive logic
            control_risk = taxpayer['risk_score'] * 0.35  # Control risk has highest weight
            detection_risk = taxpayer['risk_score'] * 0.25  # Detection risk high for payment issues
            transaction_risk = taxpayer['risk_score'] * 0.05  # Transaction risk lower weight
            inherent_risk = taxpayer['risk_score'] * 0.25  # Inherent risk baseline
            gst_behaviour_risk = taxpayer['risk_score'] * 0.10  # Behaviour risk baseline
            
            # Adjust based on risk type
            if 'ITC' in taxpayer['risk_type']:
                transaction_risk = taxpayer['risk_score'] * 0.40  # Higher transaction risk for ITC issues
                control_risk = taxpayer['risk_score'] * 0.20
            elif 'Behaviour' in taxpayer['risk_type']:
                gst_behaviour_risk = taxpayer['risk_score'] * 0.30  # Higher behavior risk for amendments
                control_risk = taxpayer['risk_score'] * 0.20
            
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
                    'Advanced Risk Pattern Detected',
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
                    taxpayer['risk_type'] + ' requires comprehensive audit - ' + taxpayer['risk_indicator'],
                    'Advanced risk indicator: ' + taxpayer['risk_indicator'] + ' detected with risk score ' + str(taxpayer['risk_score']),
                    now,
                    now,
                    1  # Default to admin user (ID 1) as assessor
                ])
            
            count += 1
            print(f"Created critical risk test for {taxpayer['gstin']} - {taxpayer['risk_indicator']} ({taxpayer['risk_level']})")
            
        except Exception as e:
            print(f"Error creating {taxpayer['gstin']}: {e}")
    
    print(f"\nSuccessfully created {count} critical risk test assessments")
    print("\nSummary of New Critical Risk Indicators:")
    print("- Consecutive Negative Returns (3 months): 2 cases - CRITICAL")
    print("- Import & Purchase vs Sales + Stock Mismatch: 2 cases - CRITICAL")
    print("- 30% Sales Variation from Previous Months: 2 cases - HIGH")
    print("- Frequent Return Amendments: 2 cases - HIGH")
    print("\nAll marked for AUDIT due to critical risk indicators")
    print("Refresh the dashboard for May-2026 to see the new critical risk indicators")

if __name__ == "__main__":
    create_critical_risk_test_data()