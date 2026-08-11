"""
Automation Script for GST Compliance Risk Assessment
Calculates risk scores for all taxpayers and populates ComplianceRiskRegister
"""

import os
import django
from datetime import date

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from taxpayers.models import TaxpayerMaster
from risk_assessment.models import ComplianceRiskRegister
from risk_assessment.risk_analysis_engine import RiskAnalysisEngine


def generate_risk_id(taxpayer, assessment_period):
    """Generate a unique risk ID"""
    # Format: RISK-{full GSTIN or CID}-{period}
    gstin = taxpayer.gstin if taxpayer.gstin else ''
    cid = taxpayer.cid_company_reg_no if taxpayer.cid_company_reg_no else ''
    identifier = gstin if gstin else cid if cid else 'UNKNOWN'
    return f"RISK-{identifier}-{assessment_period}"


def assess_single_taxpayer(taxpayer, assessment_period):
    """Assess risk for a single taxpayer"""
    gstin = taxpayer.gstin if taxpayer.gstin else 'No GSTIN'
    print(f"Assessing risk for taxpayer: {taxpayer.taxpayer_name} ({gstin})")
    
    # Initialize risk analysis engine
    engine = RiskAnalysisEngine(taxpayer, assessment_period)
    
    # Calculate all risk dimensions
    scores, reasons, risk_factors = engine.calculate_all_risks()
    
    # Calculate overall risk
    overall_score, risk_level = engine.calculate_overall_risk()
    
    # Generate audit assertions
    assertions = engine.generate_audit_assertions()
    
    # Determine audit priority and selection
    audit_priority = engine.determine_audit_priority()
    audit_selection = engine.recommend_audit_selection()
    
    # Generate risk ID
    risk_id = generate_risk_id(taxpayer, assessment_period)
    
    # Create or update ComplianceRiskRegister
    risk_register, created = ComplianceRiskRegister.objects.update_or_create(
        taxpayer=taxpayer,
        assessment_period=assessment_period,
        defaults={
            'risk_id': risk_id,
            # Taxpayer Profile
            'gstin': taxpayer.gstin or '',
            'taxpayer_name': taxpayer.taxpayer_name or '',
            'business_name': taxpayer.business_name or '',
            'activity': taxpayer.business_activity or '',
            'sector': taxpayer.sector or '',
            'sub_sector': taxpayer.sub_sector or '',
            'organisation_type': taxpayer.organisation_type or '',
            'frequency': taxpayer.frequency or '',
            'dzongkhag': taxpayer.dzongkhag or '',
            'registration_date': taxpayer.registration_date,
            'taxpayer_status': taxpayer.status or '',
            # Risk Scores
            'inherent_risk': scores['inherent_risk'],
            'control_risk': scores['control_risk'],
            'detection_risk': scores['detection_risk'],
            'gst_behaviour_risk': scores['gst_behaviour_risk'],
            'transaction_risk': scores['transaction_risk'],
            'overall_risk_score': overall_score,
            'overall_risk_level': risk_level,
            # Risk Reasons
            'gst_behaviour_reason': reasons['gst_behaviour_risk'],
            'transaction_risk_reason': reasons['transaction_risk'],
            'overall_risk_reason': reasons['overall_risk'],
            # Audit Assertions
            'primary_assertion': assertions['primary_assertion'],
            'secondary_assertion': assertions['secondary_assertion'],
            'assertion_reason': assertions['assertion_reason'],
            'audit_focus': assertions['audit_focus'],
            # Audit Decision
            'audit_priority': audit_priority,
            'audit_selection': audit_selection,
            # Risk Factors
            'import_sales_ratio': risk_factors.get('import_sales_ratio'),
            'consecutive_negative_returns': risk_factors.get('consecutive_negative_returns', 0),
            'consecutive_credit_filings': risk_factors.get('consecutive_credit_filings', 0),
            'import_zero_sales_periods': risk_factors.get('import_zero_sales_periods', 0),
            'high_domestic_purchases': risk_factors.get('high_domestic_purchases', False),
            'cash_sales_suppression': risk_factors.get('cash_sales_suppression', False),
            'sales_variation': risk_factors.get('sales_variation'),
            'stock_analysis_indicators': risk_factors.get('stock_analysis_indicators', 0),
        }
    )
    
    action = "Created" if created else "Updated"
    print(f"{action} risk register for {taxpayer.taxpayer_name} - Overall Risk: {overall_score:.2f} ({risk_level})")
    
    return risk_register


def assess_all_taxpayers(assessment_period=None):
    """Assess risk for all taxpayers, skipping those already selected for audit"""
    if assessment_period is None:
        assessment_period = f"{date.today().year}"
    
    print(f"Starting risk assessment for period: {assessment_period}")
    print("=" * 60)
    
    # Get all active taxpayers
    taxpayers = TaxpayerMaster.objects.filter(status='Active')
    total_count = taxpayers.count()
    
    print(f"Found {total_count} active taxpayers to assess")
    print()
    
    # Get taxpayers already selected for audit (to skip re-assessment)
    already_selected = ComplianceRiskRegister.objects.filter(
        audit_selection='selected'
    ).values_list('taxpayer_id', flat=True)
    
    print(f"Skipping {len(already_selected)} taxpayers already selected for audit")
    print()
    
    # Assess each taxpayer
    results = {
        'total': total_count,
        'assessed': 0,
        'skipped': len(already_selected),
        'errors': 0,
        'risk_distribution': {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0,
            'minimal': 0,
        }
    }
    
    for i, taxpayer in enumerate(taxpayers, 1):
        # Skip if already selected for audit
        if taxpayer.id in already_selected:
            print(f"Skipping {taxpayer.taxpayer_name} - already selected for audit")
            continue
        
        try:
            risk_register = assess_single_taxpayer(taxpayer, assessment_period)
            results['assessed'] += 1
            results['risk_distribution'][risk_register.overall_risk_level] += 1
            
            # Progress indicator
            if i % 10 == 0:
                print(f"Progress: {i}/{total_count} taxpayers assessed")
            
        except Exception as e:
            results['errors'] += 1
            import traceback
            print(f"Error assessing {taxpayer.taxpayer_name}: {str(e)}")
            traceback.print_exc()
            continue
    
    # Print summary
    print()
    print("=" * 60)
    print("RISK ASSESSMENT SUMMARY")
    print("=" * 60)
    print(f"Total Taxpayers: {results['total']}")
    print(f"Skipped (Already Selected): {results['skipped']}")
    print(f"Successfully Assessed: {results['assessed']}")
    print(f"Errors: {results['errors']}")
    print()
    print("Risk Distribution:")
    for level, count in results['risk_distribution'].items():
        percentage = (count / results['assessed'] * 100) if results['assessed'] > 0 else 0
        print(f"  {level.capitalize()}: {count} ({percentage:.1f}%)")
    print("=" * 60)
    
    return results


def backfill_existing_records():
    """Backfill risk assessment for existing ComplianceRiskRegister records"""
    print("Backfilling risk assessment for existing records...")
    print("=" * 60)
    
    # Get existing risk registers without calculated scores
    existing_registers = ComplianceRiskRegister.objects.filter(
        overall_risk_score=0
    )
    
    total_count = existing_registers.count()
    print(f"Found {total_count} records to backfill")
    print()
    
    results = {
        'total': total_count,
        'backfilled': 0,
        'errors': 0,
    }
    
    for i, register in enumerate(existing_registers, 1):
        try:
            if register.taxpayer:
                # Use the existing assessment period
                assessment_period = register.assessment_period or f"{date.today().year}"
                
                # Initialize risk analysis engine
                engine = RiskAnalysisEngine(register.taxpayer, assessment_period)
                
                # Calculate all risk dimensions
                scores, reasons, risk_factors = engine.calculate_all_risks()
                
                # Calculate overall risk
                overall_score, risk_level = engine.calculate_overall_risk()
                
                # Generate audit assertions
                assertions = engine.generate_audit_assertions()
                
                # Determine audit priority and selection
                audit_priority = engine.determine_audit_priority()
                audit_selection = engine.recommend_audit_selection()
                
                # Generate risk ID if missing
                if not register.risk_id:
                    register.risk_id = generate_risk_id(register.taxpayer, assessment_period)
                
                # Update the register
                register.inherent_risk = scores['inherent_risk']
                register.control_risk = scores['control_risk']
                register.detection_risk = scores['detection_risk']
                register.gst_behaviour_risk = scores['gst_behaviour_risk']
                register.transaction_risk = scores['transaction_risk']
                register.overall_risk_score = overall_score
                register.overall_risk_level = risk_level
                register.gst_behaviour_reason = reasons['gst_behaviour_risk']
                register.transaction_risk_reason = reasons['transaction_risk']
                register.overall_risk_reason = reasons['overall_risk']
                register.primary_assertion = assertions['primary_assertion']
                register.secondary_assertion = assertions['secondary_assertion']
                register.assertion_reason = assertions['assertion_reason']
                register.audit_focus = assertions['audit_focus']
                register.audit_priority = audit_priority
                register.audit_selection = audit_selection
                register.import_sales_ratio = risk_factors.get('import_sales_ratio')
                register.consecutive_negative_returns = risk_factors.get('consecutive_negative_returns', 0)
                register.import_zero_sales_periods = risk_factors.get('import_zero_sales_periods', 0)
                register.high_domestic_purchases = risk_factors.get('high_domestic_purchases', False)
                register.cash_sales_suppression = risk_factors.get('cash_sales_suppression', False)
                register.sales_variation = risk_factors.get('sales_variation')
                
                register.save()
                
                results['backfilled'] += 1
                print(f"Backfilled {i}/{total_count}: {register.taxpayer.taxpayer_name} - Risk: {overall_score:.2f} ({risk_level})")
                
                # Progress indicator
                if i % 10 == 0:
                    print(f"Progress: {i}/{total_count} records backfilled")
            
        except Exception as e:
            results['errors'] += 1
            print(f"Error backfilling register {register.id}: {str(e)}")
            continue
    
    print()
    print("=" * 60)
    print("BACKFILL SUMMARY")
    print("=" * 60)
    print(f"Total Records: {results['total']}")
    print(f"Successfully Backfilled: {results['backfilled']}")
    print(f"Errors: {results['errors']}")
    print("=" * 60)
    
    return results


if __name__ == "__main__":
    import sys
    
    # Check command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "assess_all":
            # Optional: specify assessment period
            period = sys.argv[2] if len(sys.argv) > 2 else None
            assess_all_taxpayers(period)
        
        elif command == "backfill":
            backfill_existing_records()
        
        elif command == "assess_single":
            # Assess a single taxpayer by GSTIN
            if len(sys.argv) > 2:
                gstin = sys.argv[2]
                period = sys.argv[3] if len(sys.argv) > 3 else f"{date.today().year}"
                
                try:
                    taxpayer = TaxpayerMaster.objects.get(gstin=gstin)
                    assess_single_taxpayer(taxpayer, period)
                except TaxpayerMaster.DoesNotExist:
                    print(f"Taxpayer with GSTIN {gstin} not found")
            else:
                print("Usage: python automate_risk_assessment.py assess_single <gstin> [period]")
        
        else:
            print("Unknown command. Available commands:")
            print("  assess_all [period]  - Assess all active taxpayers")
            print("  backfill            - Backfill existing risk register records")
            print("  assess_single <gstin> [period] - Assess a single taxpayer by GSTIN")
    else:
        # Default: assess all taxpayers for current year
        assess_all_taxpayers()