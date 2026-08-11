"""
Period-based Risk Assessment Script
Assesses taxpayer risk for a specific tax period and selects for audit
"""

import os
import django
from datetime import date, datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from taxpayers.models import TaxpayerMaster
from returns.models import GSTReturn
from risk_assessment.models import ComplianceRiskRegister
from risk_assessment.risk_analysis_engine import RiskAnalysisEngine


def assess_period_risk(tax_period):
    """
    Assess risk for all taxpayers for a specific tax period
    Returns detailed statistics on audit selection
    """
    print(f"Starting period-based risk assessment for: {tax_period}")
    print("=" * 60)
    
    # Get all active taxpayers
    taxpayers = TaxpayerMaster.objects.filter(status='Active')
    total_count = taxpayers.count()
    
    print(f"Found {total_count} active taxpayers")
    print()
    
    # Get returns for the specific tax period
    period_returns = GSTReturn.objects.filter(tax_period=tax_period)
    print(f"Found {period_returns.count()} returns for period {tax_period}")
    print()
    
    # Get taxpayers with returns for this period
    taxpayers_with_returns = period_returns.values_list('gstin', flat=True).distinct()
    
    # Check which taxpayers already selected for audit (skip re-assessment)
    already_selected_gstins = ComplianceRiskRegister.objects.filter(
        audit_selection='selected'
    ).values_list('gstin', flat=True)
    
    print(f"Skipping {len(already_selected_gstins)} taxpayers already selected for audit")
    print()
    
    # Assess each taxpayer
    results = {
        'total': total_count,
        'with_returns': len(taxpayers_with_returns),
        'assessed': 0,
        'skipped': len(already_selected_gstins),
        'errors': 0,
        'selected_for_audit': 0,
        'review': 0,
        'not_selected': 0,
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
        if taxpayer.gstin in already_selected_gstins:
            continue
        
        # Skip if no returns for this period
        if taxpayer.gstin not in taxpayers_with_returns:
            continue
        
        try:
            # Initialize risk analysis engine
            engine = RiskAnalysisEngine(taxpayer, tax_period)
            
            # Calculate all risk dimensions
            scores, reasons, risk_factors = engine.calculate_all_risks()
            
            # Calculate overall risk
            overall_score, risk_level = engine.calculate_overall_risk()
            
            # Generate audit assertions
            assertions = engine.generate_audit_assertions()
            
            # Determine audit priority and selection
            audit_priority = engine.determine_audit_priority()
            audit_selection = engine.recommend_audit_selection()
            
            # Create or update risk register
            risk_register, created = ComplianceRiskRegister.objects.update_or_create(
                taxpayer=taxpayer,
                assessment_period=tax_period,
                defaults={
                    'risk_id': f"RISK-{taxpayer.gstin if taxpayer.gstin else taxpayer.cid_company_reg_no[:10] if taxpayer.cid_company_reg_no else 'UNK'}-{tax_period}",
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
            results['assessed'] += 1
            results['risk_distribution'][risk_level] += 1
            
            if audit_selection == 'selected':
                results['selected_for_audit'] += 1
                print(f"SELECTED: {taxpayer.taxpayer_name} - Risk: {overall_score:.2f} ({risk_level})")
            elif audit_selection == 'review':
                results['review'] += 1
                print(f"REVIEW: {taxpayer.taxpayer_name} - Risk: {overall_score:.2f} ({risk_level})")
            else:
                results['not_selected'] += 1
            
            # Progress indicator
            if i % 20 == 0:
                print(f"Progress: {i}/{total_count} taxpayers processed")
            
        except Exception as e:
            results['errors'] += 1
            import traceback
            print(f"Error assessing {taxpayer.taxpayer_name}: {str(e)}")
            traceback.print_exc()
            continue
    
    # Print detailed summary
    print()
    print("=" * 60)
    print("PERIOD-BASED RISK ASSESSMENT SUMMARY")
    print("=" * 60)
    print(f"Tax Period: {tax_period}")
    print(f"Total Taxpayers: {results['total']}")
    print(f"With Returns in Period: {results['with_returns']}")
    print(f"Skipped (Already Selected): {results['skipped']}")
    print(f"Successfully Assessed: {results['assessed']}")
    print(f"Errors: {results['errors']}")
    print()
    print("AUDIT SELECTION RESULTS:")
    if results['assessed'] > 0:
        print(f"  Selected for Audit: {results['selected_for_audit']} ({results['selected_for_audit']/results['assessed']*100:.1f}% of assessed)")
        print(f"  Review: {results['review']} ({results['review']/results['assessed']*100:.1f}% of assessed)")
        print(f"  Not Selected: {results['not_selected']} ({results['not_selected']/results['assessed']*100:.1f}% of assessed)")
    else:
        print("  No taxpayers assessed")
    print()
    print("Risk Distribution:")
    for level, count in results['risk_distribution'].items():
        percentage = (count / results['assessed'] * 100) if results['assessed'] > 0 else 0
        print(f"  {level.capitalize()}: {count} ({percentage:.1f}%)")
    print("=" * 60)
    
    return results


if __name__ == "__main__":
    import sys
    
    # Get tax period from command line
    if len(sys.argv) > 1:
        tax_period = sys.argv[1]
    else:
        # Default to current month if not specified
        current_date = date.today()
        tax_period = current_date.strftime('%b-%Y')
        print(f"No tax period specified, using current period: {tax_period}")
    
    assess_period_risk(tax_period)