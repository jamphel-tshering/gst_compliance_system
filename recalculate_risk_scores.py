import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from compliance.risk_engine import RiskAssessmentEngine
from returns.models import GSTReturn
from decimal import Decimal
from django.db import connection

def recalculate_assessments(from_period_str, to_period_str, period_name):
    """Recalculate risk scores for existing assessments using comprehensive risk logic"""
    print(f"Recalculating risk scores for {period_name} ({from_period_str} to {to_period_str})")
    
    # Get all assessments for the period using raw SQL
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, gstin FROM compliance_complianceriskreferral 
            WHERE assessment_from_period = %s AND assessment_to_period = %s
        """, [from_period_str, to_period_str])
        assessments = cursor.fetchall()
    
    total = len(assessments)
    print(f"Found {total} assessments to recalculate")
    
    engine = RiskAssessmentEngine()
    count = 0
    
    for assessment_id, gstin in assessments:
        try:
            # Get the most recent return
            gst_return = GSTReturn.objects.filter(
                gstin=gstin,
                tax_period__in=engine.get_tax_periods_between(from_period_str, to_period_str)
            ).order_by('-tax_period').first()
            
            if gst_return:
                # Calculate new risk score using comprehensive logic
                filing_status = gst_return.filing_status if gst_return.filing_status else ''
                payment_status = gst_return.payment_status if gst_return.payment_status else ''
                
                # COMPREHENSIVE RISK CALCULATION
                control_risk = Decimal('0')
                detection_risk = Decimal('0')
                transaction_risk = Decimal('0')
                inherent_risk = Decimal('0')
                gst_behaviour_risk = Decimal('0')
                
                # 1. FILING COMPLIANCE (Control Risk - highest weight)
                if 'non' in filing_status.lower() or 'overdue' in filing_status.lower() or not filing_status.strip():
                    control_risk += Decimal('5.0')  # Maximum for non-filing
                elif 'late' in filing_status.lower():
                    control_risk += Decimal('2.5')
                else:
                    control_risk += Decimal('0.5')
                
                # 2. PAYMENT COMPLIANCE (Detection Risk)
                if payment_status and 'not paid' in payment_status.lower():
                    detection_risk += Decimal('4.0')
                elif payment_status and 'credit' in payment_status.lower():
                    detection_risk += Decimal('1.0')
                elif payment_status and 'zero' in payment_status.lower():
                    detection_risk += Decimal('0.3')
                
                # 3. ADVANCED RISK INDICATORS - CRITICAL RISK FACTORS
                
                # 3.1 Check for consecutive negative returns (3 months)
                if engine.check_consecutive_negative_returns(gstin):
                    detection_risk += Decimal('3.0')  # Significant risk factor
                    risk_type = 'Sales & Output GST Risk'
                
                # 3.2 Check Import & Purchase vs Sales + Stock (ITC mismatch)
                if engine.check_itc_mismatch(gst_return):
                    transaction_risk += Decimal('3.5')  # High risk for ITC fraud
                    risk_type = 'Purchase & ITC Risk'
                
                # 3.3 Check for 30% sales variation from previous months
                if engine.check_sales_variation_30_percent(gst_return):
                    transaction_risk += Decimal('2.5')  # Moderate-high risk
                    risk_type = 'Sales & Output GST Risk'
                
                # 3.4 Check for frequent return amendments
                if engine.check_frequent_amendments(gstin):
                    gst_behaviour_risk += Decimal('2.0')  # Behavior risk
                    risk_type = 'GST Behaviour & Compliance History Risk'
                
                # 3.5 TRANSACTION RISK (based on business activity)
                if hasattr(gst_return, 'total_taxable_sales') and gst_return.total_taxable_sales:
                    try:
                        sales_amount = Decimal(str(gst_return.total_taxable_sales))
                        if sales_amount > Decimal('1000000'):
                            transaction_risk += Decimal('1.5')
                        elif sales_amount > Decimal('500000'):
                            transaction_risk += Decimal('1.0')
                        else:
                            transaction_risk += Decimal('0.5')
                    except:
                        transaction_risk += Decimal('0.5')
                else:
                    transaction_risk += Decimal('0.5')
                
                # 4. BASELINE RISKS
                gst_behaviour_risk += Decimal('0.5')
                inherent_risk += Decimal('0.5')
                
                # Calculate overall risk score using comprehensive weights
                overall_risk_score = (
                    (inherent_risk * engine.WEIGHTS['inherent_risk']) +
                    (control_risk * engine.WEIGHTS['control_risk']) +
                    (detection_risk * engine.WEIGHTS['detection_risk']) +
                    (gst_behaviour_risk * engine.WEIGHTS['gst_behaviour_risk']) +
                    (transaction_risk * engine.WEIGHTS['transaction_risk'])
                )
                
                overall_risk_score = min(overall_risk_score, Decimal('5.0'))
                if overall_risk_score < Decimal('0.5'):
                    overall_risk_score = Decimal('0.5')
                
                # Determine risk level using comprehensive thresholds
                if overall_risk_score >= engine.RISK_THRESHOLDS['critical']:
                    risk_level = 'Critical'
                elif overall_risk_score >= engine.RISK_THRESHOLDS['high']:
                    risk_level = 'High'
                elif overall_risk_score >= engine.RISK_THRESHOLDS['medium']:
                    risk_level = 'Medium'
                else:
                    risk_level = 'Low'
                
                # Determine system decision based on comprehensive risk level
                if risk_level in ['Critical', 'High']:
                    system_decision = 'AUDIT'
                elif risk_level == 'Medium':
                    system_decision = 'MONITOR'
                else:
                    system_decision = 'NOT SELECTED'
                
                # Update using raw SQL to avoid decimal issues
                with connection.cursor() as cursor:
                    cursor.execute("""
                        UPDATE compliance_complianceriskreferral 
                        SET risk_score = %s, risk_level = %s, control_risk = %s, detection_risk = %s, 
                            transaction_risk = %s, inherent_risk = %s, gst_behaviour_risk = %s, system_decision = %s
                        WHERE id = %s
                    """, [float(overall_risk_score), risk_level, float(control_risk), float(detection_risk), 
                          float(transaction_risk), float(inherent_risk), float(gst_behaviour_risk), 
                          system_decision, assessment_id])
                
                count += 1
                if count % 50 == 0:
                    print(f"Processed {count}/{total} assessments")
                    
        except Exception as e:
            print(f"Error processing {gstin}: {e}")
    
    print(f"Successfully recalculated {count} assessments")

if __name__ == "__main__":
    # Recalculate for all periods that have existing assessments
    periods = [
        ('2026-01-01', '2026-01-01', 'Jan-2026'),
        ('2026-02-01', '2026-02-01', 'Feb-2026'),
        ('2026-04-01', '2026-04-01', 'Apr-2026'),
        ('2026-05-01', '2026-05-01', 'May-2026'),
    ]
    
    for from_period, to_period, period_name in periods:
        print(f"\n{'='*60}")
        recalculate_assessments(from_period, to_period, period_name)