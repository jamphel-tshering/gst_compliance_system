"""
Compliance Risk Assessment Engine

This module implements the risk-based selection engine as specified in the requirements.
It uses existing GST Return data to calculate risk scores and generate recommendations.
"""

from decimal import Decimal
from django.db.models import Q, Sum, Avg, Count
from returns.models import GSTReturn
from taxpayers.models import TaxpayerMaster
from .models import ComplianceRiskReferral


class RiskAssessmentEngine:
    """
    Risk Assessment Engine - Implements the risk-based selection methodology
    """
    
    # Risk scoring weights (configurable) - balanced for rational audit selection
    WEIGHTS = {
        'inherent_risk': Decimal('0.25'),
        'control_risk': Decimal('0.35'),  # Increased weight on compliance behavior
        'detection_risk': Decimal('0.25'),  # Payment defaults are critical
        'gst_behaviour_risk': Decimal('0.10'),
        'transaction_risk': Decimal('0.05'),  # Reduced weight
    }
    
    # Risk level thresholds (configurable) - adjusted for realistic scoring
    RISK_THRESHOLDS = {
        'low': Decimal('1.0'),      # Low risk: minimal issues
        'medium': Decimal('2.0'),   # Medium risk: some compliance issues
        'high': Decimal('3.0'),     # High risk: significant compliance issues
        'critical': Decimal('4.0')  # Critical risk: severe non-compliance
    }
    
    # Audit selection targets (for first-time GST system in Bhutan)
    AUDIT_TARGETS = {
        'critical': (2, 5),      # 2-5 taxpayers
        'high': (5, 20),         # 5-20 taxpayers  
        'review': (5, 20),       # 5-20 taxpayers
        'monitor': (10, 30),     # 10-30 taxpayers
    }
    
    # Sales variation threshold (configurable)
    SALES_VARIATION_THRESHOLD = Decimal('30.0')
    
    # Risk indicator definitions
    RISK_INDICATORS = {
        # Filing & Payment Risk
        'late_filing': {'weight': 1.5, 'dimension': 'control_risk'},
        'non_filing': {'weight': 2.5, 'dimension': 'control_risk'},
        'payment_default': {'weight': 2.0, 'dimension': 'control_risk'},
        'repeated_late_filing': {'weight': 2.0, 'dimension': 'gst_behaviour_risk'},
        'repeated_payment_default': {'weight': 2.5, 'dimension': 'gst_behaviour_risk'},
        
        # Sales & Output GST Risk
        'high_low_sales_pattern': {'weight': 1.0, 'dimension': 'transaction_risk'},
        'sales_variation_30_plus': {'weight': 1.5, 'dimension': 'transaction_risk'},
        'low_sales_imports': {'weight': 2.0, 'dimension': 'transaction_risk'},
        'low_sales_transaction_activity': {'weight': 1.5, 'dimension': 'transaction_risk'},
        
        # Purchase & ITC Risk
        'high_itc_claim': {'weight': 1.5, 'dimension': 'transaction_risk'},
        'high_itc_sales_ratio': {'weight': 2.0, 'dimension': 'transaction_risk'},
        'significant_itc_increase': {'weight': 1.5, 'dimension': 'transaction_risk'},
        'itc_disproportionate_output': {'weight': 2.5, 'dimension': 'transaction_risk'},
        
        # Import & Transaction Risk
        'high_import_low_sales': {'weight': 2.5, 'dimension': 'transaction_risk'},
        'high_import_zero_sales': {'weight': 3.0, 'dimension': 'transaction_risk'},
        'import_without_sales': {'weight': 2.0, 'dimension': 'transaction_risk'},
        'ecms_import_mismatch': {'weight': 2.0, 'dimension': 'transaction_risk'},
        
        # GST Behaviour Risk
        'three_consecutive_negative': {'weight': 2.5, 'dimension': 'gst_behaviour_risk'},
        'repeated_amendments': {'weight': 1.5, 'dimension': 'gst_behaviour_risk'},
        
        # Inherent/Structural Risk
        'multiple_licenses': {'weight': 1.0, 'dimension': 'inherent_risk'},
        'multiple_business_activities': {'weight': 0.5, 'dimension': 'inherent_risk'},
        'complex_business_structure': {'weight': 1.0, 'dimension': 'inherent_risk'},
        
        # Refund Risk
        'large_refund_claim': {'weight': 2.0, 'dimension': 'transaction_risk'},
        'repeated_refund_claims': {'weight': 1.5, 'dimension': 'gst_behaviour_risk'},
        'high_itc_supporting_refund': {'weight': 2.0, 'dimension': 'transaction_risk'},
        'unusual_refund_pattern': {'weight': 1.5, 'dimension': 'transaction_risk'},
    }
    
    # Risk pattern recognition
    RISK_PATTERNS = {
        'import_suppression': [
            'high_import_low_sales',
            'high_import_zero_sales',
            'import_without_sales'
        ],
        'itc_refund_risk': [
            'high_itc_claim',
            'negative_return',
            'large_refund_claim'
        ],
        'payment_compliance_risk': [
            'repeated_late_filing',
            'payment_default'
        ],
        'amendment_variation_risk': [
            'repeated_amendments',
            'sales_variation_30_plus'
        ],
    }
    
    # Risk type determination (system decision logic)
    SYSTEM_DECISION_MAPPING = {
        'Audit': 'AUDIT',
        'Review': 'REVIEW', 
        'Monitoring': 'MONITOR',
        'Not Selected': 'NOT SELECTED',
    }
    
    # Audit assertion mapping
    AUDIT_ASSERTIONS = {
        'filing_payment_risk': ['A01 – Completeness', 'A03 – Accuracy', 'A04 – Cut-off', 'A09 – Compliance'],
        'sales_output_risk': ['A01 – Completeness', 'A02 – Occurrence', 'A03 – Accuracy', 'A04 – Cut-off'],
        'purchase_itc_risk': ['A02 – Occurrence', 'A01 – Completeness', 'A03 – Accuracy', 'A07 – Rights & Obligations', 'A09 – Compliance'],
        'import_transaction_risk': ['A01 – Completeness', 'A03 – Accuracy', 'A04 – Cut-off', 'A02 – Occurrence', 'A08 – Valuation'],
        'refund_risk': ['A06 – Existence', 'A03 – Accuracy', 'A08 – Valuation', 'A07 – Rights & Obligations', 'A09 – Compliance'],
        'gst_behaviour_risk': ['A01 – Completeness', 'A03 – Accuracy', 'A04 – Cut-off', 'A09 – Compliance'],
        'inherent_structural_risk': ['A05 – Classification', 'A01 – Completeness', 'A09 – Compliance'],
    }
    
    def assess_all_returns(self, user):
        """Assess all GST returns for risk - DEPRECATED in favor of period-based assessment"""
        # This method is deprecated in favor of assess_period
        return self.assess_period('Jan-2026', 'Dec-2027', user)
    
    def assess_period(self, from_period, to_period, user):
        """Assess GST returns within a specific period for risk"""
        count = 0
        new_assessments = []
        total_processed = 0
        
        # Get tax periods in order
        tax_periods = self.get_tax_periods_between(from_period, to_period)
        
        for tax_period in tax_periods:
            gst_returns = GSTReturn.objects.filter(tax_period=tax_period)
            
            for gst_return in gst_returns:
                total_processed += 1
                
                # Check if risk assessment already exists for this period using raw query to avoid decimal issues
                from django.db import connection
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT id FROM compliance_complianceriskreferral 
                        WHERE gstin = %s AND assessment_from_period = %s AND assessment_to_period = %s
                        LIMIT 1
                    """, [gst_return.gstin, from_period, to_period])
                    existing = cursor.fetchone()
                
                if not existing:
                    # Create risk assessment
                    risk_assessment = self.assess_return_for_period(gst_return, from_period, to_period, user)
                    if risk_assessment:
                        new_assessments.append(risk_assessment)
                        count += 1
        
        # Apply audit targets if we have new assessments
        if len(new_assessments) > 0:
            new_assessments = self.apply_audit_targets(new_assessments)
            # Save the updated assessments
            for assessment in new_assessments:
                assessment.save()
        
        return total_processed  # Return total processed instead of just new ones
    
    def apply_audit_targets(self, assessments):
        """
        Apply audit selection targets for first-time GST system in Bhutan
        - Critical: 2-5 taxpayers
        - High: 5-20 taxpayers  
        - Review: 5-20 taxpayers
        - Monitor: 10-30 taxpayers
        - Rest: Not selected
        Higher risk should be at top
        """
        # Group by risk level
        critical = [a for a in assessments if a.risk_level == 'Critical']
        high = [a for a in assessments if a.risk_level == 'High']
        medium = [a for a in assessments if a.risk_level == 'Medium']
        low = [a for a in assessments if a.risk_level == 'Low']
        
        # Sort each group by risk score (highest first)
        critical.sort(key=lambda x: x.risk_score, reverse=True)
        high.sort(key=lambda x: x.risk_score, reverse=True)
        medium.sort(key=lambda x: x.risk_score, reverse=True)
        low.sort(key=lambda x: x.risk_score, reverse=True)
        
        # Apply targets
        min_critical, max_critical = self.AUDIT_TARGETS['critical']
        min_high, max_high = self.AUDIT_TARGETS['high']
        min_review, max_review = self.AUDIT_TARGETS['review']
        min_monitor, max_monitor = self.AUDIT_TARGETS['monitor']
        
        # Select Critical for AUDIT (2-5)
        critical_audit = critical[:min(max_critical, len(critical))]
        for assessment in critical_audit:
            assessment.system_decision = 'AUDIT'
            assessment.referred_to = 'Audit & Investigation'
            assessment.audit_assertion = f"Critical risk assessment - {assessment.risk_type} requires comprehensive audit"
        
        # Select High for AUDIT (5-20)
        high_audit = high[:min(max_high, len(high))]
        for assessment in high_audit:
            assessment.system_decision = 'AUDIT'
            assessment.referred_to = 'Audit & Investigation'
            assessment.audit_assertion = f"High risk assessment - {assessment.risk_type} requires targeted audit"
        
        # Select remaining High/Medium for REVIEW (5-20)
        remaining_high = high[min(max_high, len(high)):]
        review_candidates = remaining_high + medium
        review_candidates.sort(key=lambda x: x.risk_score, reverse=True)
        review_selected = review_candidates[:min(max_review, len(review_candidates))]
        for assessment in review_selected:
            assessment.system_decision = 'REVIEW'
            assessment.referred_to = 'Review & Compliance'
            assessment.audit_assertion = f"Risk review required - {assessment.risk_type} needs detailed examination"
        
        # Select remaining for MONITOR (10-30)
        # Remove selected ones from review_candidates to get remaining
        review_selected_ids = {a.id for a in review_selected}
        remaining_after_review = [a for a in review_candidates if a.id not in review_selected_ids]
        monitor_candidates = remaining_after_review + low
        monitor_candidates.sort(key=lambda x: x.risk_score, reverse=True)
        monitor_selected = monitor_candidates[:min(max_monitor, len(monitor_candidates))]
        for assessment in monitor_selected:
            assessment.system_decision = 'MONITOR'
            assessment.referred_to = 'Compliance Monitoring'
            assessment.audit_assertion = f"Compliance monitoring - {assessment.risk_type} to be tracked"
        
        # Rest: NOT SELECTED
        monitor_selected_ids = {a.id for a in monitor_selected}
        not_selected = [a for a in assessments if a.id not in 
                       {a.id for a in critical_audit + high_audit + review_selected + monitor_selected}]
        for assessment in not_selected:
            assessment.system_decision = 'NOT SELECTED'
            assessment.referred_to = 'Compliance Monitoring'
            assessment.audit_assertment = f"No immediate action required - {assessment.risk_type} within acceptable risk"
        
        return assessments
    
    def date_to_month_year(self, date_str):
        """Convert date format '2026-05-01' to 'May-2026' format"""
        if not date_str:
            return date_str
        
        try:
            if '-' in date_str and len(date_str) >= 7:
                parts = date_str.split('-')
                if len(parts) >= 2:
                    year = parts[0]
                    month_part = parts[1]
                    
                    month_map = {
                        '01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr',
                        '05': 'May', '06': 'Jun', '07': 'Jul', '08': 'Aug',
                        '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'
                    }
                    
                    if month_part in month_map:
                        return f"{month_map[month_part]}-{year}"
            
            return date_str
        except:
            return date_str

    def get_tax_periods_between(self, from_period, to_period):
        """Get list of tax periods that match the requested period range"""
        # Get all available periods from database
        all_periods = list(GSTReturn.objects.values_list('tax_period', flat=True).distinct())
        
        # Convert UI format (May-2026) to match database format (2026-05-01 or Jan-Mar 2026)
        matching_periods = []
        
        for period in all_periods:
            period_matches = False
            
            # Try to match with various formats
            if from_period and to_period:
                # Extract year and month from requested period (e.g., "May-2026" -> "2026", "May")
                from_parts = from_period.split('-')
                to_parts = to_period.split('-')
                
                if len(from_parts) == 2 and len(to_parts) == 2:
                    requested_year = from_parts[1]
                    requested_month = from_parts[0]
                    
                    # Check if this period matches the year and month
                    if requested_year in period:
                        # Check for month match in various formats
                        if requested_month in period.lower() or \
                           requested_month[:3] in period.lower():
                            period_matches = True
                        # Also check if it's a quarterly period that includes this month
                        elif 'jan-mar' in period.lower() and requested_month in ['jan', 'feb', 'mar']:
                            period_matches = True
                        elif 'apr-jun' in period.lower() and requested_month in ['apr', 'may', 'jun']:
                            period_matches = True
                        elif 'jul-sep' in period.lower() and requested_month in ['jul', 'aug', 'sep']:
                            period_matches = True
                        elif 'oct-dec' in period.lower() and requested_month in ['oct', 'nov', 'dec']:
                            period_matches = True
            
            if period_matches:
                matching_periods.append(period)
        
        # If no matches, return all periods to ensure we don't miss any data
        return matching_periods if matching_periods else all_periods
    
    def date_to_month_year(self, date_str):
        """Convert date format '2026-05-01' to 'May-2026' format"""
        if not date_str:
            return date_str
        
        try:
            if '-' in date_str and len(date_str) >= 7:
                parts = date_str.split('-')
                if len(parts) >= 2:
                    year = parts[0]
                    month_part = parts[1]
                    
                    month_map = {
                        '01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr',
                        '05': 'May', '06': 'Jun', '07': 'Jul', '08': 'Aug',
                        '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'
                    }
                    
                    if month_part in month_map:
                        return f"{month_map[month_part]}-{year}"
            
            return date_str
        except:
            return date_str
    
    def assess_return(self, gst_return, user):
        """Assess a single GST return for risk - DEPRECATED"""
        return self.assess_return_for_period(gst_return, 'Jan-2026', 'Dec-2027', user)
    
    def assess_return_for_period(self, gst_return, from_period, to_period, user):
        """Assess a single GST return for risk within a specific period"""
        # Create risk assessment record
        risk_assessment = ComplianceRiskReferral.objects.create(
            gstin=gst_return.gstin,
            taxpayer_name=gst_return.taxpayer_name,
            assessment_from_period=from_period,
            assessment_to_period=to_period,
            assessment_status='Assessment Generated',
            assessor=user  # Auto-set the user who ran the assessment as assessor
        )
        
        # Calculate risk
        self.calculate_risk_score(risk_assessment, gst_return, from_period, to_period)
        
        # Save the risk assessment to ensure risk scores are persisted
        risk_assessment.save()
        
        # Don't generate selection recommendation immediately - will be done with audit targets
        return risk_assessment
    
    def calculate_risk_score(self, risk_assessment, gst_return=None, from_period=None, to_period=None):
        """Calculate comprehensive risk score based on rational compliance assessment with advanced risk indicators"""
        if gst_return is None:
            # Get the most recent return within the assessment period
            gst_return = GSTReturn.objects.filter(
                gstin=risk_assessment.gstin,
                tax_period__in=self.get_tax_periods_between(from_period, to_period)
            ).order_by('-tax_period').first()
        
        if not gst_return:
            return
        
        # Initialize risk dimensions
        inherent_risk = Decimal('0')
        control_risk = Decimal('0')
        detection_risk = Decimal('0')
        gst_behaviour_risk = Decimal('0')
        transaction_risk = Decimal('0')
        
        detected_indicators = []
        risk_type = None
        primary_indicator = None
        
        # Get filing and payment status
        filing_status = gst_return.filing_status if gst_return.filing_status else ''
        payment_status = gst_return.payment_status if gst_return.payment_status else ''
        
        # COMPREHENSIVE RISK ASSESSMENT LOGIC
        
        # 1. FILING COMPLIANCE (Control Risk - highest weight)
        if 'non' in filing_status.lower() or 'overdue' in filing_status.lower() or not filing_status.strip():
            # Non-filer - severe compliance issue
            control_risk += Decimal('5.0')  # Maximum score for non-filing
            detected_indicators.append('non_filing')
            primary_indicator = 'Non Filing'
            risk_type = 'Filing & Payment Risk'
        elif 'late' in filing_status.lower():
            # Late filer - moderate compliance issue
            control_risk += Decimal('2.5')
            detected_indicators.append('late_filing')
            primary_indicator = 'Late Filing'
            risk_type = 'Filing & Payment Risk'
        else:
            # Normal filer - baseline compliance
            control_risk += Decimal('0.5')
            risk_type = 'Sales & Output GST Risk'
        
        # 2. PAYMENT COMPLIANCE (Detection Risk - critical for revenue)
        if payment_status and 'not paid' in payment_status.lower():
            # Payment default - critical revenue risk
            detection_risk += Decimal('4.0')
            detected_indicators.append('payment_default')
        elif payment_status and 'credit' in payment_status.lower():
            # Credit balance - moderate concern
            detection_risk += Decimal('1.0')
            detected_indicators.append('credit_balance')
        elif payment_status and 'zero' in payment_status.lower():
            # Zero return - low revenue risk
            detection_risk += Decimal('0.3')
            detected_indicators.append('zero_return')
        
        # 3. ADVANCED RISK INDICATORS - CRITICAL RISK FACTORS
        
        # 3.1 Check for consecutive negative returns (3 months)
        if self.check_consecutive_negative_returns(gst_return.gstin):
            detection_risk += Decimal('3.0')  # Significant risk factor
            detected_indicators.append('consecutive_negative_returns')
            primary_indicator = 'Consecutive Negative Returns'
            risk_type = 'Sales & Output GST Risk'
        
        # 3.2 Check Import & Purchase vs Sales + Stock (ITC mismatch)
        if self.check_itc_mismatch(gst_return):
            transaction_risk += Decimal('3.5')  # High risk for ITC fraud
            detected_indicators.append('itc_mismatch')
            primary_indicator = 'ITC Mismatch'
            risk_type = 'Purchase & ITC Risk'
        
        # 3.3 Check for 30% sales variation from previous months
        if self.check_sales_variation_30_percent(gst_return):
            transaction_risk += Decimal('2.5')  # Moderate-high risk
            detected_indicators.append('sales_variation_30_percent')
            primary_indicator = 'Sales Variation'
            risk_type = 'Sales & Output GST Risk'
        
        # 3.4 Check for frequent return amendments
        if self.check_frequent_amendments(gst_return.gstin):
            gst_behaviour_risk += Decimal('2.0')  # Behavior risk
            detected_indicators.append('frequent_amendments')
            primary_indicator = 'Frequent Amendments'
            risk_type = 'GST Behaviour & Compliance History Risk'
        
        # 4. TRANSACTION RISK (based on business activity)
        # Check for large sales or unusual patterns
        if hasattr(gst_return, 'total_taxable_sales') and gst_return.total_taxable_sales:
            try:
                sales_amount = Decimal(str(gst_return.total_taxable_sales))
                if sales_amount > Decimal('1000000'):  # Large business
                    transaction_risk += Decimal('1.5')
                    detected_indicators.append('large_business')
                elif sales_amount > Decimal('500000'):  # Medium business
                    transaction_risk += Decimal('1.0')
                    detected_indicators.append('medium_business')
                else:  # Small business
                    transaction_risk += Decimal('0.5')
                    detected_indicators.append('small_business')
            except:
                transaction_risk += Decimal('0.5')  # Default baseline
        else:
            transaction_risk += Decimal('0.5')  # Default baseline
        
        # 5. GST BEHAVIOR RISK (historical compliance)
        # This would be enhanced with historical data in future
        gst_behaviour_risk += Decimal('0.5')  # Baseline
        
        # 6. INHERENT RISK (business complexity factors)
        # This would be enhanced with business complexity indicators
        inherent_risk += Decimal('0.5')  # Baseline
        
        # Calculate overall risk score using weighted dimensions
        overall_risk_score = (
            (inherent_risk * self.WEIGHTS['inherent_risk']) +
            (control_risk * self.WEIGHTS['control_risk']) +
            (detection_risk * self.WEIGHTS['detection_risk']) +
            (gst_behaviour_risk * self.WEIGHTS['gst_behaviour_risk']) +
            (transaction_risk * self.WEIGHTS['transaction_risk'])
        )
        
        # Cap at 5.0
        overall_risk_score = min(overall_risk_score, Decimal('5.0'))
        
        # Ensure minimum score for any taxpayer (baseline risk)
        if overall_risk_score < Decimal('0.5'):
            overall_risk_score = Decimal('0.5')
        
        # Determine risk level using comprehensive thresholds
        if overall_risk_score >= self.RISK_THRESHOLDS['critical']:
            risk_level = 'Critical'
        elif overall_risk_score >= self.RISK_THRESHOLDS['high']:
            risk_level = 'High'
        elif overall_risk_score >= self.RISK_THRESHOLDS['medium']:
            risk_level = 'Medium'
        else:
            risk_level = 'Low'
        
        # Determine risk type based on dominant dimension
        risk_type = self.determine_risk_type(inherent_risk, control_risk, detection_risk, gst_behaviour_risk, transaction_risk)
        
        # Generate risk reason
        risk_reason = self.generate_risk_reason(detected_indicators, gst_return)
        
        # Map to audit assertions
        audit_assertion = self.map_to_audit_assertion(risk_type)
        
        # Update risk assessment
        risk_assessment.inherent_risk = inherent_risk
        risk_assessment.control_risk = control_risk
        risk_assessment.detection_risk = detection_risk
        risk_assessment.gst_behaviour_risk = gst_behaviour_risk
        risk_assessment.transaction_risk = transaction_risk
        risk_assessment.risk_score = overall_risk_score
        risk_assessment.risk_level = risk_level
        risk_assessment.risk_type = risk_type
        risk_assessment.risk_indicator = primary_indicator or detected_indicators[0] if detected_indicators else None
        risk_assessment.audit_assertion = audit_assertion
        risk_assessment.risk_reason = risk_reason
        
        risk_assessment.save()
    
    def check_consecutive_negative_returns(self, gstin):
        """Check if taxpayer has consecutive negative returns for 3 months"""
        try:
            # Get last 3 returns including current period
            returns = GSTReturn.objects.filter(
                gstin=gstin
            ).order_by('-tax_period')[:3]
            
            if len(returns) < 3:
                return False
            
            # Check if all 3 returns are negative
            negative_count = 0
            for ret in returns:
                if hasattr(ret, 'net_tax_liability') and ret.net_tax_liability:
                    try:
                        liability = Decimal(str(ret.net_tax_liability))
                        if liability < 0:
                            negative_count += 1
                    except:
                        pass
                elif hasattr(ret, 'total_tax') and ret.total_tax:
                    try:
                        total_tax = Decimal(str(ret.total_tax))
                        if total_tax < 0:
                            negative_count += 1
                    except:
                        pass
            
            return negative_count >= 3
        except Exception as e:
            return False
    
    def check_itc_mismatch(self, gst_return):
        """Check for Import & Purchase vs Sales + Stock mismatch (ITC fraud risk)"""
        try:
            # Check if the return has the necessary fields
            if not hasattr(gst_return, 'total_itc_claimed') or not hasattr(gst_return, 'total_taxable_sales'):
                return False
            
            itc_claimed = Decimal(str(gst_return.total_itc_claimed)) if gst_return.total_itc_claimed else Decimal('0')
            sales = Decimal(str(gst_return.total_taxable_sales)) if gst_return.total_taxable_sales else Decimal('0')
            
            # If ITC claimed is more than 50% of sales, it's suspicious
            if sales > 0 and (itc_claimed / sales) > Decimal('0.5'):
                return True
            
            # If ITC claimed is very high and sales are low/negative
            if itc_claimed > Decimal('100000') and sales < Decimal('50000'):
                return True
            
            return False
        except Exception as e:
            return False
    
    def check_sales_variation_30_percent(self, gst_return):
        """Check for 30% sales variation from previous months"""
        try:
            if not hasattr(gst_return, 'total_taxable_sales') or not gst_return.total_taxable_sales:
                return False
            
            current_sales = Decimal(str(gst_return.total_taxable_sales))
            
            # Get previous month's return
            previous_returns = GSTReturn.objects.filter(
                gstin=gst_return.gstin,
                tax_period__lt=gst_return.tax_period
            ).order_by('-tax_period')[:3]
            
            if not previous_returns:
                return False
            
            # Check against each of the last 3 months
            for prev_return in previous_returns:
                if hasattr(prev_return, 'total_taxable_sales') and prev_return.total_taxable_sales:
                    try:
                        prev_sales = Decimal(str(prev_return.total_taxable_sales))
                        
                        # Avoid division by zero
                        if prev_sales == 0:
                            if current_sales > 0:
                                return True  # Any sales after zero is 100% increase
                            continue
                        
                        # Calculate percentage variation
                        variation = abs((current_sales - prev_sales) / prev_sales) * 100
                        
                        if variation >= 30:  # 30% variation threshold
                            return True
                    except:
                        pass
            
            return False
        except Exception as e:
            return False
    
    def check_frequent_amendments(self, gstin):
        """Check for frequent return amendments"""
        try:
            # Get returns for the last 6 months
            recent_returns = GSTReturn.objects.filter(
                gstin=gstin
            ).order_by('-tax_period')[:6]
            
            amendment_count = 0
            for ret in recent_returns:
                # Check if the return indicates it's an amendment
                if hasattr(ret, 'return_type') and ret.return_type:
                    if 'amend' in ret.return_type.lower() or 'revised' in ret.return_type.lower():
                        amendment_count += 1
                # Also check filing status for amendment indicators
                if hasattr(ret, 'filing_status') and ret.filing_status:
                    if 'amend' in ret.filing_status.lower() or 'revised' in ret.filing_status.lower():
                        amendment_count += 1
            
            # If 2 or more amendments in last 6 months, it's frequent
            return amendment_count >= 2
        except Exception as e:
            return False
    
    def check_indicator(self, indicator, gst_return, taxpayer):
        """Check if a specific risk indicator is present"""
        try:
            if indicator == 'late_filing':
                return gst_return.filing_delay_days > 0 and gst_return.filing_status == 'Late Filer'
            
            elif indicator == 'non_filing':
                # Check for various non-filing statuses - more comprehensive check
                non_filing_statuses = ['Overdue / Non-Filer', 'Non-Filer', 'Overdue', 'Not Filed', 'Non Filer', 'None', '', None]
                current_status = gst_return.filing_status if gst_return.filing_status else ''
                is_non_filer = current_status in non_filing_statuses or (not current_status.strip() if current_status else True)
                # Also check if the status is explicitly about non-filing
                is_non_filer = is_non_filer or 'non' in current_status.lower() or 'overdue' in current_status.lower()
                return is_non_filer
            
            elif indicator == 'payment_default':
                return gst_return.payment_status == 'Not paid'
            
            elif indicator == 'repeated_late_filing':
                return self.check_repeated_late_filing(gst_return.gstin)
            
            elif indicator == 'repeated_payment_default':
                return self.check_repeated_payment_default(gst_return.gstin)
            
            elif indicator == 'high_low_sales_pattern':
                return self.check_high_low_sales_pattern(gst_return.gstin)
            
            elif indicator == 'sales_variation_30_plus':
                return self.check_sales_variation(gst_return)
            
            elif indicator == 'low_sales_imports':
                return self.check_low_sales_imports(gst_return)
            
            elif indicator == 'low_sales_transaction_activity':
                return self.check_low_sales_transaction_activity(gst_return)
            
            elif indicator == 'high_itc_claim':
                return self.check_high_itc_claim(gst_return)
            
            elif indicator == 'high_itc_sales_ratio':
                return self.check_high_itc_sales_ratio(gst_return)
            
            elif indicator == 'significant_itc_increase':
                return self.check_significant_itc_increase(gst_return)
            
            elif indicator == 'itc_disproportionate_output':
                return self.check_itc_disproportionate_output(gst_return)
            
            elif indicator == 'high_import_low_sales':
                return self.check_high_import_low_sales(gst_return)
            
            elif indicator == 'high_import_zero_sales':
                return self.check_high_import_zero_sales(gst_return)
            
            elif indicator == 'import_without_sales':
                return self.check_import_without_sales(gst_return)
            
            elif indicator == 'ecms_import_mismatch':
                return self.check_ecms_import_mismatch(gst_return)
            
            elif indicator == 'three_consecutive_negative':
                return self.check_three_consecutive_negative(gst_return.gstin)
            
            elif indicator == 'repeated_amendments':
                return self.check_repeated_amendments(gst_return.gstin)
            
            elif indicator == 'multiple_licenses':
                return taxpayer and taxpayer.business_licenses.count() > 1 if taxpayer else False
            
            elif indicator == 'multiple_business_activities':
                return taxpayer and len(taxpayer.business_activity.split(',')) > 1 if taxpayer else False
            
            elif indicator == 'complex_business_structure':
                return taxpayer and taxpayer.organisation_type in ['Private Company', 'Public Company', 'Joint Venture'] if taxpayer else False
            
            elif indicator == 'large_refund_claim':
                return gst_return.gst_payable_refundable < -10000  # Large refund (configurable threshold)
            
            elif indicator == 'repeated_refund_claims':
                return self.check_repeated_refund_claims(gst_return.gstin)
            
            elif indicator == 'high_itc_supporting_refund':
                return self.check_high_itc_supporting_refund(gst_return)
            
            elif indicator == 'unusual_refund_pattern':
                return self.check_unusual_refund_pattern(gst_return.gstin)
            
            elif indicator == 'negative_return':
                return gst_return.gst_payable_refundable < 0
            
            return False
        except:
            return False
    
    def check_repeated_late_filing(self, gstin):
        """Check for repeated late filing"""
        late_filings = GSTReturn.objects.filter(
            gstin=gstin,
            filing_status='Late Filer'
        ).count()
        return late_filings >= 3  # Configurable threshold
    
    def check_repeated_payment_default(self, gstin):
        """Check for repeated payment default"""
        defaults = GSTReturn.objects.filter(
            gstin=gstin,
            payment_status='Not paid'
        ).count()
        return defaults >= 2  # Configurable threshold
    
    def check_high_low_sales_pattern(self, gstin):
        """Check for high/low sales pattern"""
        returns = GSTReturn.objects.filter(gstin=gstin).order_by('tax_period')
        if returns.count() < 3:
            return False
        
        sales_values = [ret.declared_sales for ret in returns if ret.declared_sales]
        if not sales_values:
            return False
        
        avg_sales = sum(sales_values) / len(sales_values)
        max_sales = max(sales_values)
        min_sales = min(sales_values)
        
        # Significant variation between max and min
        return (max_sales - min_sales) > (avg_sales * 0.5)
    
    def check_sales_variation(self, gst_return):
        """Check for 30% or more sales variation compared to previous return"""
        previous_return = GSTReturn.objects.filter(
            gstin=gst_return.gstin,
            tax_period__lt=gst_return.tax_period
        ).order_by('-tax_period').first()
        
        if not previous_return or not previous_return.declared_sales:
            return False
        
        if previous_return.declared_sales == 0:
            return gst_return.declared_sales > 0
        
        variation = abs(gst_return.declared_sales - previous_return.declared_sales) / previous_return.declared_sales * 100
        return variation >= self.SALES_VARIATION_THRESHOLD
    
    def check_low_sales_imports(self, gst_return):
        """Check for low sales relative to imports"""
        if not gst_return.declared_import_value or gst_return.declared_import_value == 0:
            return False
        
        return gst_return.declared_sales < (gst_return.declared_import_value * 0.5)  # Configurable ratio
    
    def check_low_sales_transaction_activity(self, gst_return):
        """Check for low sales relative to overall transaction activity"""
        total_activity = (
            gst_return.declared_sales + 
            gst_return.declared_domestic_purchase + 
            gst_return.declared_import_value
        )
        
        if total_activity == 0:
            return False
        
        return gst_return.declared_sales < (total_activity * 0.3)  # Configurable ratio
    
    def check_high_itc_claim(self, gst_return):
        """Check for high ITC claim"""
        if not gst_return.declared_sales or gst_return.declared_sales == 0:
            return False
        
        itc_ratio = gst_return.total_itc_claimed / gst_return.declared_sales
        return itc_ratio > 0.15  # Configurable threshold
    
    def check_high_itc_sales_ratio(self, gst_return):
        """Check for high ITC-to-sales ratio"""
        if not gst_return.declared_sales or gst_return.declared_sales == 0:
            return False
        
        if not gst_return.declared_output_gst or gst_return.declared_output_gst == 0:
            return gst_return.total_itc_claimed > 0
        
        itc_output_ratio = gst_return.total_itc_claimed / gst_return.declared_output_gst
        return itc_output_ratio > 1.0  # Configurable threshold
    
    def check_significant_itc_increase(self, gst_return):
        """Check for significant increase in ITC"""
        previous_return = GSTReturn.objects.filter(
            gstin=gst_return.gstin,
            tax_period__lt=gst_return.tax_period
        ).order_by('-tax_period').first()
        
        if not previous_return or not previous_return.total_itc_claimed:
            return False
        
        if previous_return.total_itc_claimed == 0:
            return gst_return.total_itc_claimed > 0
        
        increase = (gst_return.total_itc_claimed - previous_return.total_itc_claimed) / previous_return.total_itc_claimed * 100
        return increase >= 50  # Configurable threshold
    
    def check_itc_disproportionate_output(self, gst_return):
        """Check for ITC disproportionate to output GST"""
        if not gst_return.declared_output_gst or gst_return.declared_output_gst == 0:
            return gst_return.total_itc_claimed > 0
        
        ratio = gst_return.total_itc_claimed / gst_return.declared_output_gst
        return ratio > 1.5  # Configurable threshold
    
    def check_high_import_low_sales(self, gst_return):
        """Check for high import and low sales"""
        if not gst_return.declared_import_value or gst_return.declared_import_value == 0:
            return False
        
        return gst_return.declared_sales < (gst_return.declared_import_value * 0.3)  # Configurable ratio
    
    def check_high_import_zero_sales(self, gst_return):
        """Check for high import and zero sales"""
        return (gst_return.declared_import_value > 50000 and  # Configurable threshold
                gst_return.declared_sales == 0)
    
    def check_import_without_sales(self, gst_return):
        """Check for import without corresponding sales"""
        return (gst_return.declared_import_value > 0 and 
                gst_return.declared_sales == 0)
    
    def check_ecms_import_mismatch(self, gst_return):
        """Check for eCMS import vs declared import mismatch"""
        if not gst_return.ecms_import_value or not gst_return.declared_import_value:
            return False
        
        mismatch = abs(gst_return.ecms_import_value - gst_return.declared_import_value)
        return mismatch > (gst_return.declared_import_value * 0.2)  # Configurable threshold
    
    def check_three_consecutive_negative(self, gstin):
        """Check for three consecutive negative returns"""
        recent_returns = GSTReturn.objects.filter(
            gstin=gstin
        ).order_by('-tax_period')[:3]
        
        if recent_returns.count() < 3:
            return False
        
        return all(ret.gst_payable_refundable < 0 for ret in recent_returns)
    
    def check_repeated_amendments(self, gstin):
        """Check for repeated return amendments"""
        # This would need to be tracked separately in a real system
        # For now, assume it's checked via updated_at timestamps
        recent_returns = GSTReturn.objects.filter(
            gstin=gstin
        ).order_by('-tax_period')[:5]
        
        if recent_returns.count() < 2:
            return False
        
        # Check if recent returns have been updated frequently
        # This is a simplified check
        return False  # Would need amendment tracking
    
    def check_repeated_refund_claims(self, gstin):
        """Check for repeated refund claims"""
        refund_returns = GSTReturn.objects.filter(
            gstin=gstin,
            gst_payable_refundable__lt=0
        ).count()
        return refund_returns >= 3  # Configurable threshold
    
    def check_high_itc_supporting_refund(self, gst_return):
        """Check for high ITC supporting refund"""
        if gst_return.gst_payable_refundable >= 0:
            return False
        
        if gst_return.total_itc_claimed == 0:
            return False
        
        refund_amount = abs(gst_return.gst_payable_refundable)
        itc_refund_ratio = gst_return.total_itc_claimed / refund_amount
        return itc_refund_ratio > 0.8  # Configurable threshold
    
    def check_unusual_refund_pattern(self, gstin):
        """Check for unusual refund pattern"""
        refund_returns = GSTReturn.objects.filter(
            gstin=gstin,
            gst_payable_refundable__lt=0
        ).order_by('-tax_period')[:6]
        
        if refund_returns.count() < 3:
            return False
        
        # Check for alternating refund/non-refund pattern
        refund_count = refund_returns.count()
        pattern_variation = 0
        
        for i in range(1, refund_returns.count()):
            if (refund_returns[i-1].gst_payable_refundable < 0) != (refund_returns[i].gst_payable_refundable < 0):
                pattern_variation += 1
        
        return pattern_variation >= 2  # Configurable threshold
    
    def apply_pattern_adjustments(self, detected_indicators, inherent_risk, control_risk, detection_risk, gst_behaviour_risk, transaction_risk):
        """Apply pattern recognition adjustments to avoid double counting"""
        # Check for import suppression pattern
        import_indicators = [ind for ind in detected_indicators if ind in self.RISK_PATTERNS['import_suppression']]
        if len(import_indicators) >= 2:
            # Apply pattern adjustment - count as one strong risk instead of multiple
            excess = len(import_indicators) - 1
            transaction_risk -= (Decimal(str(excess)) * Decimal('0.5'))
        
        # Check for ITC/refund risk pattern
        itc_refund_indicators = [ind for ind in detected_indicators if ind in self.RISK_PATTERNS['itc_refund_risk']]
        if len(itc_refund_indicators) >= 2:
            excess = len(itc_refund_indicators) - 1
            transaction_risk -= (Decimal(str(excess)) * Decimal('0.5'))
        
        # Check for payment compliance risk pattern
        payment_indicators = [ind for ind in detected_indicators if ind in self.RISK_PATTERNS['payment_compliance_risk']]
        if len(payment_indicators) >= 2:
            excess = len(payment_indicators) - 1
            gst_behaviour_risk -= (Decimal(str(excess)) * Decimal('0.5'))
        
        return inherent_risk, control_risk, detection_risk, gst_behaviour_risk, transaction_risk
    
    def determine_risk_level(self, risk_score):
        """Determine risk level based on overall score"""
        if risk_score >= self.RISK_THRESHOLDS['high']:
            return 'Critical'
        elif risk_score >= self.RISK_THRESHOLDS['medium']:
            return 'High'
        elif risk_score >= self.RISK_THRESHOLDS['low']:
            return 'Medium'
        else:
            return 'Low'
    
    def determine_risk_type(self, inherent_risk, control_risk, detection_risk, gst_behaviour_risk, transaction_risk):
        """Determine risk type based on dominant dimension"""
        risk_dimensions = {
            'Inherent/Structural Risk': inherent_risk,
            'Filing & Payment Risk': control_risk,
            'Detection Risk': detection_risk,
            'GST Behaviour & Compliance History Risk': gst_behaviour_risk,
            'Transaction Risk': transaction_risk,
        }
        
        # Find the dominant dimension
        dominant_risk = max(risk_dimensions.items(), key=lambda x: x[1])
        
        # Map to standard risk types
        risk_type_mapping = {
            'Inherent/Structural Risk': 'GST Behaviour & Compliance History Risk',
            'Filing & Payment Risk': 'Filing & Payment Risk',
            'Detection Risk': 'Filing & Payment Risk',
            'GST Behaviour & Compliance History Risk': 'GST Behaviour & Compliance History Risk',
            'Transaction Risk': 'Sales & Output GST Risk',  # Default transaction risk
        }
        
        return risk_type_mapping.get(dominant_risk[0], 'Sales & Output GST Risk')
    
    def generate_risk_reason(self, detected_indicators, gst_return):
        """Generate clear risk reason based on detected indicators"""
        if not detected_indicators:
            return "No significant risk indicators detected."
        
        reasons = []
        
        for indicator in detected_indicators[:3]:  # Top 3 indicators
            indicator_reason = self.get_indicator_reason(indicator, gst_return)
            if indicator_reason:
                reasons.append(indicator_reason)
        
        return " | ".join(reasons) if reasons else "Risk indicators detected."
    
    def get_indicator_reason(self, indicator, gst_return):
        """Get human-readable reason for an indicator"""
        reason_map = {
            'late_filing': f"Return filed {gst_return.filing_delay_days} days late",
            'non_filing': "Return not filed (Overdue)",
            'payment_default': "GST payment not received",
            'repeated_late_filing': "Repeated late filing pattern detected",
            'repeated_payment_default': "Repeated payment default pattern detected",
            'high_low_sales_pattern': "Significant sales variation pattern detected",
            'sales_variation_30_plus': f"Sales variation {self.SALES_VARIATION_THRESHOLD}%+ compared to previous period",
            'low_sales_imports': "Sales unusually low relative to import activity",
            'low_sales_transaction_activity': "Sales low relative to overall transaction activity",
            'high_itc_claim': "ITC claim unusually high relative to sales",
            'high_itc_sales_ratio': "ITC-to-sales ratio above normal threshold",
            'significant_itc_increase': "Significant increase in ITC claimed",
            'itc_disproportionate_output': "ITC claimed disproportionate to output GST",
            'high_import_low_sales': "High import activity with low sales",
            'high_import_zero_sales': "High import activity with zero sales",
            'import_without_sales': "Import activity without corresponding sales",
            'ecms_import_mismatch': "eCMS import value differs from declared import",
            'three_consecutive_negative': "Three consecutive negative returns filed",
            'repeated_amendments': "Repeated return amendments detected",
            'multiple_licenses': "Multiple GST licenses held",
            'multiple_business_activities': "Multiple business activities",
            'complex_business_structure': "Complex business structure",
            'large_refund_claim': "Large refund claim made",
            'repeated_refund_claims': "Repeated refund claims pattern",
            'high_itc_supporting_refund': "High ITC supporting refund claim",
            'unusual_refund_pattern': "Unusual refund pattern detected",
            'negative_return': "Negative return filed",
        }
        
        return reason_map.get(indicator, f"{indicator.replace('_', ' ').title()} detected")
    
    def map_to_audit_assertion(self, risk_type):
        """Map risk type to appropriate audit assertions"""
        return self.AUDIT_ASSERTIONS.get(risk_type.lower().replace(' ', '_'), ['A09 – Compliance'])[0]
    
    def generate_selection_recommendation(self, risk_assessment):
        """Generate automatic system decision based on risk level and other factors"""
        risk_level = risk_assessment.risk_level
        risk_score = risk_assessment.risk_score
        risk_type = risk_assessment.risk_type
        risk_indicator = risk_assessment.risk_indicator
        
        # System Decision Logic (Automated - No manual selection)
        if risk_level == 'Critical':
            system_decision = 'AUDIT'
            referred_to = 'Audit & Investigation'
            prescribed_action = f"Conduct comprehensive audit. Focus on {risk_type}. Verify {risk_assessment.audit_assertion}. Review {risk_indicator} with supporting documentation."
        elif risk_level == 'High':
            system_decision = 'AUDIT'
            referred_to = 'Audit & Investigation'
            prescribed_action = f"Conduct targeted audit. Address {risk_type}. Verify {risk_assessment.audit_assertion}. Review {risk_indicator} and related transactions."
        elif risk_level == 'Medium':
            # Medium risk - more nuanced decision
            if risk_score >= 3.5:  # High end of medium
                system_decision = 'REVIEW'
                referred_to = 'Review & Compliance'
                prescribed_action = f"Conduct detailed review of {risk_type}. Verify {risk_assessment.audit_assertion}. Request clarification on {risk_indicator}. Monitor subsequent filings."
            else:
                system_decision = 'MONITOR'
                referred_to = 'Compliance Monitoring'
                prescribed_action = f"Monitor compliance status. Track {risk_type} indicators. Conduct periodic review of {risk_indicator}. Check future filing patterns."
        else:  # Low risk
            system_decision = 'NOT SELECTED'
            referred_to = 'Compliance Monitoring'
            prescribed_action = f"Continue routine monitoring. Maintain standard compliance checks. No immediate action required for {risk_type}."
        
        # Override for specific risk types
        if 'Refund' in risk_type:
            system_decision = 'REVIEW'
            referred_to = 'Refund Review Team'
            prescribed_action = f"Review refund claim for {risk_type}. Verify ITC documentation. Validate refund calculation. Cross-check with audit assertions."
        elif 'Payment' in risk_type or risk_indicator in ['non_filing', 'payment_default']:
            system_decision = 'AUDIT'
            referred_to = 'Enforcement & Recovery'
            prescribed_action = f"Immediate enforcement action required. Initiate recovery proceedings for {risk_indicator}. Document all communication. Escalate for legal action if needed."
        
        risk_assessment.system_decision = system_decision
        risk_assessment.selection = system_decision  # Keep for backward compatibility
        risk_assessment.referred_to = referred_to
        risk_assessment.prescribed_officer_action = prescribed_action
        risk_assessment.referral_status = 'Pending'
        
        risk_assessment.save()