"""
Risk Analysis Engine for GST Compliance Risk Assessment
Calculates risk scores across 5 dimensions on a 0-5 scale
"""

from decimal import Decimal
from datetime import date, datetime
from django.db.models import Avg, Sum, Count, Q, F
from django.db.models.functions import Coalesce


class RiskAnalysisEngine:
    """
    Risk Analysis Engine - Calculates risk scores for GST compliance assessment
    Uses a 0-5 scale for each risk dimension
    """
    
    def __init__(self, taxpayer, assessment_period):
        self.taxpayer = taxpayer
        self.assessment_period = assessment_period
        self.gstin = taxpayer.gstin if taxpayer.gstin else ''
        self.risk_factors = {}
        self.scores = {
            'inherent_risk': Decimal('0.00'),
            'control_risk': Decimal('0.00'),
            'detection_risk': Decimal('0.00'),
            'gst_behaviour_risk': Decimal('0.00'),
            'transaction_risk': Decimal('0.00'),
        }
        self.reasons = {
            'inherent_risk': '',
            'control_risk': '',
            'detection_risk': '',
            'gst_behaviour_risk': '',
            'transaction_risk': '',
        }
    
    def calculate_all_risks(self):
        """Calculate all risk dimensions"""
        self.calculate_inherent_risk()
        self.calculate_control_risk()
        self.calculate_detection_risk()
        self.calculate_gst_behaviour_risk()
        self.calculate_transaction_risk()
        
        return self.scores, self.reasons, self.risk_factors
    
    def calculate_inherent_risk(self):
        """
        Inherent Risk (0-5): Based on taxpayer characteristics
        Factors: Organization type, Business sector, Age of business, Geography
        """
        score = Decimal('0.00')
        reasons = []
        
        # 1. Organization Type Risk
        org_risk = self._calculate_org_type_risk()
        score += org_risk['score']
        if org_risk['reason']:
            reasons.append(org_risk['reason'])
        
        # 2. Sector Risk
        sector_risk = self._calculate_sector_risk()
        score += sector_risk['score']
        if sector_risk['reason']:
            reasons.append(sector_risk['reason'])
        
        # 3. Business Age Risk
        age_risk = self._calculate_business_age_risk()
        score += age_risk['score']
        if age_risk['reason']:
            reasons.append(age_risk['reason'])
        
        # 4. Geography Risk
        geo_risk = self._calculate_geography_risk()
        score += geo_risk['score']
        if geo_risk['reason']:
            reasons.append(geo_risk['reason'])
        
        # Cap at 5
        self.scores['inherent_risk'] = min(score, Decimal('5.00'))
        self.reasons['inherent_risk'] = '; '.join(reasons)
        
        # Store risk factors
        self.risk_factors['org_type_risk'] = org_risk['score']
        self.risk_factors['sector_risk'] = sector_risk['score']
        self.risk_factors['age_risk'] = age_risk['score']
        self.risk_factors['geo_risk'] = geo_risk['score']
    
    def _calculate_org_type_risk(self):
        """Calculate risk based on organization type"""
        org_type = self.taxpayer.organisation_type
        
        # Risk scores by organization type
        org_risk_map = {
            'Sole Proprietorship': 1.5,
            'Partnership': 1.2,
            'Private Company': 0.8,
            'Public Company': 0.5,
            'Government Entity': 0.3,
            'Foreign Company': 1.8,
            'Joint Venture': 1.0,
            'State Owned Company': 0.6,
            'Other': 1.0,
        }
        
        score = Decimal(str(org_risk_map.get(org_type, 1.0)))
        reason = f"Organization type {org_type} has risk score {score}"
        
        return {'score': score, 'reason': reason}
    
    def _calculate_sector_risk(self):
        """Calculate risk based on business sector"""
        sector = self.taxpayer.sector
        
        # Risk scores by sector
        sector_risk_map = {
            'Construction': 1.5,
            'Manufacturing': 1.2,
            'Trading': 1.0,
            'Services': 0.8,
            'Hospitality': 1.2,
            'Transport': 1.0,
            'Real Estate': 1.3,
            'Mining': 1.8,
            'Agriculture': 0.5,
            'Finance': 0.7,
            'Other': 1.0,
        }
        
        score = Decimal(str(sector_risk_map.get(sector, 1.0)))
        reason = f"Sector {sector} has risk score {score}"
        
        return {'score': score, 'reason': reason}
    
    def _calculate_business_age_risk(self):
        """Calculate risk based on business age"""
        if not self.taxpayer.registration_date:
            return {'score': Decimal('1.5'), 'reason': 'No registration date - moderate risk'}
        
        today = date.today()
        reg_date = self.taxpayer.registration_date
        
        # Calculate years in business
        years_in_business = Decimal(str((today - reg_date).days / 365.25))
        
        if years_in_business < 1:
            score = Decimal('1.5')
            reason = f'New business ({years_in_business:.1f} years) - higher risk'
        elif years_in_business < 3:
            score = Decimal('1.0')
            reason = f'Young business ({years_in_business:.1f} years) - moderate risk'
        elif years_in_business < 5:
            score = Decimal('0.7')
            reason = f'Established business ({years_in_business:.1f} years) - lower risk'
        else:
            score = Decimal('0.5')
            reason = f'Mature business ({years_in_business:.1f} years) - low risk'
        
        return {'score': score, 'reason': reason}
    
    def _calculate_geography_risk(self):
        """Calculate risk based on geographic location"""
        dzongkhag = self.taxpayer.dzongkhag
        
        # Risk scores by dzongkhag (can be customized)
        geo_risk_map = {
            'Mongar': 0.8,
            'Trashigang': 0.8,
            'Trashiyangtse': 0.9,
            'Lhuentse': 1.0,
        }
        
        score = Decimal(str(geo_risk_map.get(dzongkhag, 0.8)))
        reason = f"Dzongkhag {dzongkhag} has risk score {score}"
        
        return {'score': score, 'reason': reason}
    
    def calculate_control_risk(self):
        """
        Control Risk (0-5): Based on internal controls and compliance history
        Factors: Filing consistency, Tax payment history, Compliance status
        """
        from returns.models import GSTReturn
        
        score = Decimal('0.00')
        reasons = []
        
        # Get GST returns for this taxpayer (using gstin)
        returns = GSTReturn.objects.filter(gstin=self.gstin)
        
        if not returns.exists():
            self.scores['control_risk'] = Decimal('3.0')
            self.reasons['control_risk'] = 'No GST returns history - high control risk'
            return
        
        # 1. Filing Consistency Risk
        filing_risk = self._calculate_filing_consistency_risk(returns)
        score += filing_risk['score']
        if filing_risk['reason']:
            reasons.append(filing_risk['reason'])
        
        # 2. Tax Payment Risk
        payment_risk = self._calculate_tax_payment_risk(returns)
        score += payment_risk['score']
        if payment_risk['reason']:
            reasons.append(payment_risk['reason'])
        
        # 3. Compliance Status Risk
        compliance_risk = self._calculate_compliance_status_risk(returns)
        score += compliance_risk['score']
        if compliance_risk['reason']:
            reasons.append(compliance_risk['reason'])
        
        # Cap at 5
        self.scores['control_risk'] = min(score, Decimal('5.00'))
        self.reasons['control_risk'] = '; '.join(reasons)
        
        # Store risk factors
        self.risk_factors['filing_consistency_risk'] = filing_risk['score']
        self.risk_factors['payment_risk'] = payment_risk['score']
        self.risk_factors['compliance_status_risk'] = compliance_risk['score']
    
    def _calculate_filing_consistency_risk(self, returns):
        """Calculate risk based on filing consistency"""
        total_returns = returns.count()
        filed_returns = returns.filter(filing_status__in=['Filed On Time', 'Late Filer']).count()
        
        if total_returns == 0:
            return {'score': Decimal('3.0'), 'reason': 'No returns to analyze'}
        
        filing_rate = Decimal(str((filed_returns / total_returns) * 100))
        
        if filing_rate >= 95:
            score = Decimal('0.5')
            reason = f'Excellent filing rate ({filing_rate:.1f}%) - low risk'
        elif filing_rate >= 85:
            score = Decimal('1.0')
            reason = f'Good filing rate ({filing_rate:.1f}%) - moderate risk'
        elif filing_rate >= 70:
            score = Decimal('2.0')
            reason = f'Fair filing rate ({filing_rate:.1f}%) - elevated risk'
        else:
            score = Decimal('3.0')
            reason = f'Poor filing rate ({filing_rate:.1f}%) - high risk'
        
        return {'score': score, 'reason': reason}
    
    def _calculate_tax_payment_risk(self, returns):
        """Calculate risk based on tax payment history"""
        # Check for any late payments or outstanding amounts
        outstanding_returns = returns.filter(
            filing_status__in=['Filed On Time', 'Late Filer'],
            payment_status='Not paid'
        ).count()
        
        total_filed = returns.filter(filing_status__in=['Filed On Time', 'Late Filer']).count()
        
        if total_filed == 0:
            return {'score': Decimal('1.0'), 'reason': 'No filed returns to analyze'}
        
        if outstanding_returns == 0:
            score = Decimal('0.5')
            reason = 'No outstanding tax payments - low risk'
        else:
            default_rate = Decimal(str((outstanding_returns / total_filed) * 100))
            score = Decimal(str(min(default_rate / 10, 3.0)))
            reason = f'{outstanding_returns} outstanding payments ({default_rate:.1f}%) - elevated risk'
        
        return {'score': score, 'reason': reason}
    
    def _calculate_compliance_status_risk(self, returns):
        """Calculate risk based on overall compliance status"""
        compliant_returns = returns.filter(compliance_status='Compliant').count()
        total_returns = returns.count()
        
        if total_returns == 0:
            return {'score': Decimal('1.0'), 'reason': 'No returns to analyze'}
        
        compliance_rate = Decimal(str((compliant_returns / total_returns) * 100))
        
        if compliance_rate >= 90:
            score = Decimal('0.5')
            reason = f'High compliance rate ({compliance_rate:.1f}%) - low risk'
        elif compliance_rate >= 75:
            score = Decimal('1.5')
            reason = f'Moderate compliance rate ({compliance_rate:.1f}%) - medium risk'
        else:
            score = Decimal('2.5')
            reason = f'Low compliance rate ({compliance_rate:.1f}%) - high risk'
        
        return {'score': score, 'reason': reason}
    
    def calculate_detection_risk(self):
        """
        Detection Risk (0-5): Based on auditability and transparency
        Factors: Record quality, Transaction traceability, Documentation
        """
        score = Decimal('0.00')
        reasons = []
        
        # 1. Business License Risk
        license_risk = self._calculate_business_license_risk()
        score += license_risk['score']
        if license_risk['reason']:
            reasons.append(license_risk['reason'])
        
        # 2. Contact Information Risk
        contact_risk = self._calculate_contact_info_risk()
        score += contact_risk['score']
        if contact_risk['reason']:
            reasons.append(contact_risk['reason'])
        
        # 3. Activity Clarity Risk
        activity_risk = self._calculate_activity_clarity_risk()
        score += activity_risk['score']
        if activity_risk['reason']:
            reasons.append(activity_risk['reason'])
        
        # Cap at 5
        self.scores['detection_risk'] = min(score, Decimal('5.00'))
        self.reasons['detection_risk'] = '; '.join(reasons)
        
        # Store risk factors
        self.risk_factors['license_risk'] = license_risk['score']
        self.risk_factors['contact_risk'] = contact_risk['score']
        self.risk_factors['activity_risk'] = activity_risk['score']
    
    def _calculate_business_license_risk(self):
        """Calculate risk based on business license status"""
        if not self.taxpayer.cid_company_reg_no:
            return {'score': Decimal('2.0'), 'reason': 'Missing CID/Company Reg No - high detection risk'}
        
        if not self.taxpayer.is_primary_license:
            return {'score': Decimal('1.0'), 'reason': 'Additional license - moderate detection risk'}
        
        return {'score': Decimal('0.5'), 'reason': 'Valid primary license - low detection risk'}
    
    def _calculate_contact_info_risk(self):
        """Calculate risk based on contact information completeness"""
        missing_contacts = []
        
        if not self.taxpayer.email_address:
            missing_contacts.append('email')
        if not self.taxpayer.mobile_number:
            missing_contacts.append('mobile')
        if not self.taxpayer.business_address:
            missing_contacts.append('address')
        
        if len(missing_contacts) == 0:
            score = Decimal('0.5')
            reason = 'Complete contact information - low detection risk'
        elif len(missing_contacts) == 1:
            score = Decimal('1.0')
            reason = f'Missing {missing_contacts[0]} - moderate detection risk'
        else:
            score = Decimal('2.0')
            reason = f'Missing {", ".join(missing_contacts)} - high detection risk'
        
        return {'score': score, 'reason': reason}
    
    def _calculate_activity_clarity_risk(self):
        """Calculate risk based on business activity clarity"""
        if not self.taxpayer.business_activity:
            return {'score': Decimal('1.5'), 'reason': 'Missing business activity - moderate detection risk'}
        
        if not self.taxpayer.sector or not self.taxpayer.sub_sector:
            return {'score': Decimal('1.0'), 'reason': 'Incomplete sector classification - moderate detection risk'}
        
        return {'score': Decimal('0.5'), 'reason': 'Clear business activity - low detection risk'}
    
    def calculate_gst_behaviour_risk(self):
        """
        GST Behaviour Risk (0-5): Based on GST filing and payment patterns
        Factors: Filing timeliness, Consecutive Credit Filings, Payment consistency, Return filing history
        """
        from returns.models import GSTReturn
        
        score = Decimal('0.00')
        reasons = []
        
        # Get GST returns for this taxpayer (using gstin)
        returns = GSTReturn.objects.filter(gstin=self.gstin)
        
        if not returns.exists():
            self.scores['gst_behaviour_risk'] = Decimal('3.0')
            self.reasons['gst_behaviour_risk'] = 'No GST returns history - high behaviour risk'
            return
        
        # 1. Filing Timeliness Risk
        timeliness_risk = self._calculate_filing_timeliness_risk(returns)
        score += timeliness_risk['score']
        if timeliness_risk['reason']:
            reasons.append(timeliness_risk['reason'])
        
        # 2. Negative Returns Risk
        negative_risk = self._calculate_negative_returns_risk(returns)
        score += negative_risk['score']
        if negative_risk['reason']:
            reasons.append(negative_risk['reason'])
        
        # 3. Consecutive Credit Filings Risk
        credit_risk = self._calculate_consecutive_credit_filings_risk(returns)
        score += credit_risk['score']
        if credit_risk['reason']:
            reasons.append(credit_risk['reason'])
        
        # 4. Zero Sales Risk
        zero_sales_risk = self._calculate_zero_sales_risk(returns)
        score += zero_sales_risk['score']
        if zero_sales_risk['reason']:
            reasons.append(zero_sales_risk['reason'])
        
        # Cap at 5
        self.scores['gst_behaviour_risk'] = min(score, Decimal('5.00'))
        self.reasons['gst_behaviour_risk'] = '; '.join(reasons)
        
        # Store risk factors
        self.risk_factors['timeliness_risk'] = timeliness_risk['score']
        self.risk_factors['negative_returns_risk'] = negative_risk['score']
        self.risk_factors['consecutive_credit_filings'] = credit_risk.get('count', 0)
        self.risk_factors['zero_sales_risk'] = zero_sales_risk['score']
        self.risk_factors['consecutive_negative_returns'] = negative_risk.get('count', 0)
        self.risk_factors['import_zero_sales_periods'] = zero_sales_risk.get('count', 0)
    
    def _calculate_filing_timeliness_risk(self, returns):
        """Calculate risk based on filing timeliness"""
        # Count late filings (using 'Late Filer' status)
        late_filings = returns.filter(filing_status='Late Filer').count()
        total_returns = returns.count()
        
        if total_returns == 0:
            return {'score': Decimal('1.0'), 'reason': 'No returns to analyze'}
        
        late_rate = Decimal(str((late_filings / total_returns) * 100))
        
        if late_rate == 0:
            score = Decimal('0.5')
            reason = 'No late filings - low behaviour risk'
        elif late_rate <= 10:
            score = Decimal('1.0')
            reason = f'Low late filing rate ({late_rate:.1f}%) - moderate behaviour risk'
        elif late_rate <= 25:
            score = Decimal('2.0')
            reason = f'Moderate late filing rate ({late_rate:.1f}%) - elevated behaviour risk'
        else:
            score = Decimal('3.0')
            reason = f'High late filing rate ({late_rate:.1f}%) - high behaviour risk'
        
        return {'score': score, 'reason': reason}
    
    def _calculate_negative_returns_risk(self, returns):
        """Calculate risk based on consecutive negative returns"""
        # Check for consecutive negative GST liability periods
        negative_returns = returns.filter(
            filing_status__in=['Filed On Time', 'Late Filer'],
            gst_payable_refundable__lt=0
        ).order_by('tax_period')
        
        consecutive_count = 0
        max_consecutive = 0
        
        for ret in negative_returns:
            consecutive_count += 1
            max_consecutive = max(max_consecutive, consecutive_count)
        
        if max_consecutive >= 3:
            score = Decimal('2.5')
            reason = f'{max_consecutive} consecutive negative returns - high behaviour risk'
        elif max_consecutive >= 2:
            score = Decimal('1.5')
            reason = f'{max_consecutive} consecutive negative returns - moderate behaviour risk'
        elif max_consecutive >= 1:
            score = Decimal('1.0')
            reason = f'{max_consecutive} negative return - low behaviour risk'
        else:
            score = Decimal('0.5')
            reason = 'No negative returns - low behaviour risk'
        
        return {'score': score, 'reason': reason, 'count': max_consecutive}
    
    def _calculate_consecutive_credit_filings_risk(self, returns):
        """Calculate risk based on Consecutive Credit Filings"""
        # Check for consecutive periods with refunds/credits (negative gst_payable_refundable)
        credit_returns = returns.filter(
            filing_status__in=['Filed On Time', 'Late Filer'],
            gst_payable_refundable__lt=0
        ).order_by('tax_period')
        
        consecutive_credits = 0
        max_consecutive_credits = 0
        
        for ret in credit_returns:
            consecutive_credits += 1
            max_consecutive_credits = max(max_consecutive_credits, consecutive_credits)
        
        if max_consecutive_credits >= 6:
            score = Decimal('3.0')
            reason = f'{max_consecutive_credits} consecutive credit filings - critical behaviour risk'
        elif max_consecutive_credits >= 4:
            score = Decimal('2.5')
            reason = f'{max_consecutive_credits} consecutive credit filings - high behaviour risk'
        elif max_consecutive_credits >= 2:
            score = Decimal('1.5')
            reason = f'{max_consecutive_credits} consecutive credit filings - moderate behaviour risk'
        elif max_consecutive_credits >= 1:
            score = Decimal('1.0')
            reason = f'{max_consecutive_credits} credit filing - low behaviour risk'
        else:
            score = Decimal('0.5')
            reason = 'No consecutive credit filings - low behaviour risk'
        
        return {'score': score, 'reason': reason, 'count': max_consecutive_credits}
    
    def _calculate_zero_sales_risk(self, returns):
        """Calculate risk based on High Import with Zero Sales"""
        # Check for periods with imports but zero domestic sales
        zero_sales_with_import = returns.filter(
            filing_status__in=['Filed On Time', 'Late Filer'],
            declared_sales=0,
            declared_import_value__gt=0
        ).count()
        
        if zero_sales_with_import >= 3:
            score = Decimal('3.0')
            reason = f'{zero_sales_with_import} periods with High Import with Zero Sales - critical transaction risk'
        elif zero_sales_with_import >= 2:
            score = Decimal('2.5')
            reason = f'{zero_sales_with_import} periods with High Import with Zero Sales - high transaction risk'
        elif zero_sales_with_import >= 1:
            score = Decimal('1.5')
            reason = f'{zero_sales_with_import} period with High Import with Zero Sales - moderate transaction risk'
        else:
            score = Decimal('0.5')
            reason = 'No High Import with Zero Sales patterns - low transaction risk'
        
        return {'score': score, 'reason': reason, 'count': zero_sales_with_import}
    
    def calculate_transaction_risk(self):
        """
        Transaction Risk (0-5): Based on transaction patterns and anomalies
        Factors: High Import/Low Sales, High Import with Zero Sales, High Domestic Purchases, 
                 Cash Sales Suppression, Sales Variation, Stock Analysis
        """
        from returns.models import GSTReturn
        
        score = Decimal('0.00')
        reasons = []
        
        # Get GST returns for this taxpayer (using gstin)
        returns = GSTReturn.objects.filter(gstin=self.gstin)
        
        if not returns.exists():
            self.scores['transaction_risk'] = Decimal('3.0')
            self.reasons['transaction_risk'] = 'No GST returns history - high transaction risk'
            return
        
        # 1. Import/Sales Ratio Risk
        import_sales_risk = self._calculate_import_sales_ratio_risk(returns)
        score += import_sales_risk['score']
        if import_sales_risk['reason']:
            reasons.append(import_sales_risk['reason'])
        
        # 2. Sales Variation Risk
        variation_risk = self._calculate_sales_variation_risk(returns)
        score += variation_risk['score']
        if variation_risk['reason']:
            reasons.append(variation_risk['reason'])
        
        # 3. High Domestic Purchases Risk
        domestic_purchase_risk = self._calculate_domestic_purchase_risk(returns)
        score += domestic_purchase_risk['score']
        if domestic_purchase_risk['reason']:
            reasons.append(domestic_purchase_risk['reason'])
        
        # 4. Cash Sales Suppression Risk
        cash_suppression_risk = self._calculate_cash_suppression_risk(returns)
        score += cash_suppression_risk['score']
        if cash_suppression_risk['reason']:
            reasons.append(cash_suppression_risk['reason'])
        
        # 5. Stock Analysis Risk
        stock_risk = self._calculate_stock_analysis_risk(returns)
        score += stock_risk['score']
        if stock_risk['reason']:
            reasons.append(stock_risk['reason'])
        
        # Cap at 5
        self.scores['transaction_risk'] = min(score, Decimal('5.00'))
        self.reasons['transaction_risk'] = '; '.join(reasons)
        
        # Store risk factors
        self.risk_factors['import_sales_ratio'] = import_sales_risk.get('ratio', Decimal('0.00'))
        self.risk_factors['sales_variation'] = variation_risk.get('variation', Decimal('0.00'))
        self.risk_factors['high_domestic_purchases'] = domestic_purchase_risk.get('high_flag', False)
        self.risk_factors['cash_sales_suppression'] = cash_suppression_risk.get('suppression_flag', False)
        self.risk_factors['stock_analysis_indicators'] = stock_risk.get('stock_indicators', 0)
    
    def _calculate_import_sales_ratio_risk(self, returns):
        """Calculate risk based on High Import/Low Sales"""
        # Calculate average import/sales ratio
        total_imports = returns.aggregate(
            total=Coalesce(Sum('declared_import_value'), Decimal('0'))
        )['total']
        
        total_sales = returns.aggregate(
            total=Coalesce(Sum('declared_sales'), Decimal('0'))
        )['total']
        
        if total_sales == 0:
            if total_imports > 0:
                return {'score': Decimal('3.0'), 'reason': 'High Import with Zero Sales - critical transaction risk', 'ratio': Decimal('0.00')}
            return {'score': Decimal('1.0'), 'reason': 'No sales activity - moderate transaction risk', 'ratio': Decimal('0.00')}
        
        ratio = Decimal(str((total_imports / total_sales) * 100))
        
        if ratio > Decimal('80'):
            score = Decimal('2.5')
            reason = f'High Import/Low Sales ratio ({ratio:.1f}%) - critical transaction risk'
        elif ratio > Decimal('50'):
            score = Decimal('2.0')
            reason = f'Elevated Import/Low Sales ratio ({ratio:.1f}%) - high transaction risk'
        elif ratio > Decimal('30'):
            score = Decimal('1.5')
            reason = f'Moderate Import/Low Sales ratio ({ratio:.1f}%) - medium transaction risk'
        else:
            score = Decimal('0.5')
            reason = f'Normal Import/Sales ratio ({ratio:.1f}%) - low transaction risk'
        
        return {'score': score, 'reason': reason, 'ratio': ratio}
    
    def _calculate_sales_variation_risk(self, returns):
        """Calculate risk based on sales variation across periods"""
        sales_data = returns.filter(filing_status__in=['Filed On Time', 'Late Filer']).values_list('declared_sales', flat=True)
        
        if len(sales_data) < 2:
            return {'score': Decimal('1.0'), 'reason': 'Insufficient data for variation analysis', 'variation': Decimal('0.00')}
        
        # Calculate coefficient of variation
        sales_list = [float(s) for s in sales_data if s is not None]
        if not sales_list:
            return {'score': Decimal('1.0'), 'reason': 'No valid sales data', 'variation': Decimal('0.00')}
        
        mean_sales = sum(sales_list) / len(sales_list)
        if mean_sales == 0:
            return {'score': Decimal('1.0'), 'reason': 'Zero mean sales - cannot calculate variation', 'variation': Decimal('0.00')}
        
        variance = sum((x - mean_sales) ** 2 for x in sales_list) / len(sales_list)
        std_dev = variance ** 0.5
        coefficient_of_variation = Decimal(str((std_dev / mean_sales) * 100))
        
        if coefficient_of_variation > Decimal('100'):
            score = Decimal('2.0')
            reason = f'High sales variation ({coefficient_of_variation:.1f}%) - high transaction risk'
        elif coefficient_of_variation > Decimal('50'):
            score = Decimal('1.5')
            reason = f'Moderate sales variation ({coefficient_of_variation:.1f}%) - moderate transaction risk'
        else:
            score = Decimal('0.5')
            reason = f'Low sales variation ({coefficient_of_variation:.1f}%) - low transaction risk'
        
        return {'score': score, 'reason': reason, 'variation': Decimal(str(coefficient_of_variation))}
    
    def _calculate_domestic_purchase_risk(self, returns):
        """Calculate risk based on high domestic purchases relative to sales"""
        # Check for periods with high domestic purchases relative to sales
        high_purchase_periods = 0
        
        for ret in returns.filter(filing_status__in=['Filed On Time', 'Late Filer']):
            if ret.declared_sales > 0:
                purchase_ratio = Decimal(str((ret.declared_domestic_purchase / ret.declared_sales) * 100))
                if purchase_ratio > Decimal('150'):  # Purchases more than 1.5x sales
                    high_purchase_periods += 1
        
        high_flag = high_purchase_periods >= 2
        
        if high_flag:
            score = Decimal('1.5')
            reason = f'{high_purchase_periods} periods with high domestic purchases - moderate transaction risk'
        else:
            score = Decimal('0.5')
            reason = 'Normal domestic purchase patterns - low transaction risk'
        
        return {'score': score, 'reason': reason, 'high_flag': high_flag}
    
    def _calculate_cash_suppression_risk(self, returns):
        """Calculate risk based on potential cash sales suppression"""
        # Look for patterns that might indicate cash sales suppression
        # High sales with low tax liability, or high purchases with low sales
        suppression_indicators = 0
        
        for ret in returns.filter(filing_status__in=['Filed On Time', 'Late Filer']):
            # High sales but very low tax liability (potential cash sales)
            if ret.declared_sales > Decimal('100000') and ret.gst_payable_refundable < Decimal('1000'):
                suppression_indicators += 1
            
            # High purchases but low sales (potential underreporting)
            if ret.declared_domestic_purchase > ret.declared_sales * Decimal('1.5'):
                suppression_indicators += 1
        
        suppression_flag = suppression_indicators >= 2
        
        if suppression_flag:
            score = Decimal('2.0')
            reason = f'{suppression_indicators} indicators of potential cash sales suppression - high transaction risk'
        else:
            score = Decimal('0.5')
            reason = 'No cash sales suppression indicators - low transaction risk'
        
        return {'score': score, 'reason': reason, 'suppression_flag': suppression_flag}
    
    def _calculate_stock_analysis_risk(self, returns):
        """Calculate risk based on Stock Analysis (inventory vs sales patterns)"""
        # Look for inconsistencies between sales and purchases that might indicate stock manipulation
        stock_indicators = 0
        
        for ret in returns.filter(filing_status__in=['Filed On Time', 'Late Filer']):
            # Check for low purchases but high sales (possible stock depletion without replenishment)
            if ret.declared_sales > ret.declared_domestic_purchase * 3 and ret.declared_domestic_purchase > 0:
                stock_indicators += 1
            
            # Check for stagnant inventory (high purchases but low sales over multiple periods)
            if ret.declared_domestic_purchase > ret.declared_sales * 2 and ret.declared_sales > 0:
                stock_indicators += 1
        
        if stock_indicators >= 3:
            score = Decimal('2.5')
            reason = f'{stock_indicators} stock analysis indicators detected - high transaction risk'
        elif stock_indicators >= 2:
            score = Decimal('1.5')
            reason = f'{stock_indicators} stock analysis indicators detected - moderate transaction risk'
        elif stock_indicators >= 1:
            score = Decimal('1.0')
            reason = f'{stock_indicators} stock analysis indicator detected - low transaction risk'
        else:
            score = Decimal('0.5')
            reason = 'No stock analysis indicators - low transaction risk'
        
        return {'score': score, 'reason': reason, 'stock_indicators': stock_indicators}
    
    def calculate_overall_risk(self):
        """
        Calculate overall risk score and level
        Overall Risk = Weighted average of the 5 risk dimensions
        More conservative risk level determination
        """
        # Weight distribution (focused on behavior and transaction risks)
        weights = {
            'inherent_risk': Decimal('0.15'),
            'control_risk': Decimal('0.20'),
            'detection_risk': Decimal('0.10'),
            'gst_behaviour_risk': Decimal('0.30'),
            'transaction_risk': Decimal('0.25'),
        }
        
        weighted_sum = Decimal('0.00')
        for dimension, weight in weights.items():
            weighted_sum += self.scores[dimension] * Decimal(str(weight))
        
        overall_score = min(weighted_sum, Decimal('5.00'))
        
        # More realistic risk level determination
        if overall_score >= Decimal('4.0'):
            risk_level = 'critical'
        elif overall_score >= Decimal('3.5'):
            risk_level = 'high'
        elif overall_score >= Decimal('2.5'):
            risk_level = 'medium'
        elif overall_score >= Decimal('1.5'):
            risk_level = 'low'
        else:
            risk_level = 'minimal'
        
        self.scores['overall_risk_score'] = overall_score
        self.risk_factors['overall_risk_level'] = risk_level
        
        # Generate overall risk reason
        high_risk_dimensions = [dim for dim, score in self.scores.items() 
                               if dim != 'overall_risk_score' and score >= Decimal('3.0')]
        
        if high_risk_dimensions:
            reason = f'High risk in: {", ".join(high_risk_dimensions)}'
        else:
            reason = 'No individual risk dimension exceeds threshold'
        
        self.reasons['overall_risk'] = reason
        
        return overall_score, risk_level
    
    def generate_audit_assertions(self):
        """
        Generate audit assertions based on risk profile
        Returns primary assertion, secondary assertion, assertion reason, and audit focus
        """
        overall_score = self.scores.get('overall_risk_score', Decimal('0.00'))
        
        # Determine primary assertion based on highest risk dimension
        risk_dimensions = {
            'inherent_risk': self.scores['inherent_risk'],
            'control_risk': self.scores['control_risk'],
            'detection_risk': self.scores['detection_risk'],
            'gst_behaviour_risk': self.scores['gst_behaviour_risk'],
            'transaction_risk': self.scores['transaction_risk'],
        }
        
        highest_risk_dimension = max(risk_dimensions, key=risk_dimensions.get)
        highest_risk_score = risk_dimensions[highest_risk_dimension]
        
        # Generate assertions based on risk profile
        assertions = self._generate_assertions_by_risk_type(
            highest_risk_dimension, 
            highest_risk_score,
            overall_score
        )
        
        return assertions
    
    def _generate_assertions_by_risk_type(self, risk_dimension, risk_score, overall_score):
        """Generate audit assertions based on the type of highest risk"""
        
        # Mapping of risk dimensions to audit assertions
        assertion_mapping = {
            'inherent_risk': {
                'primary': 'Existence and Completeness',
                'secondary': 'Valuation',
                'focus': 'Verify business legitimacy, registration details, and organizational structure',
            },
            'control_risk': {
                'primary': 'Completeness and Accuracy',
                'secondary': 'Rights and Obligations',
                'focus': 'Review internal controls, filing procedures, and compliance mechanisms',
            },
            'detection_risk': {
                'primary': 'Existence and Presentation',
                'secondary': 'Completeness',
                'focus': 'Examine record-keeping systems, documentation quality, and information availability',
            },
            'gst_behaviour_risk': {
                'primary': 'Completeness and Timeliness',
                'secondary': 'Accuracy',
                'focus': 'Analyze filing patterns, payment history, and compliance behavior',
            },
            'transaction_risk': {
                'primary': 'Accuracy and Valuation',
                'secondary': 'Completeness',
                'focus': 'Scrutinize transaction patterns, ratios, and anomaly detection',
            },
        }
        
        base_assertions = assertion_mapping.get(risk_dimension, assertion_mapping['transaction_risk'])
        
        # Customize based on overall risk level
        if overall_score >= 4.0:
            assertion_reason = f'Critical overall risk ({overall_score:.2f}) with highest {risk_dimension} ({risk_score:.2f}) - comprehensive audit required'
            audit_focus = base_assertions['focus'] + ' with enhanced sampling and detailed verification'
        elif overall_score >= 3.0:
            assertion_reason = f'High overall risk ({overall_score:.2f}) with elevated {risk_dimension} ({risk_score:.2f}) - focused audit recommended'
            audit_focus = base_assertions['focus'] + ' with targeted testing'
        elif overall_score >= 2.0:
            assertion_reason = f'Medium overall risk ({overall_score:.2f}) with moderate {risk_dimension} ({risk_score:.2f}) - standard audit procedures'
            audit_focus = base_assertions['focus'] + ' with standard verification'
        else:
            assertion_reason = f'Low overall risk ({overall_score:.2f}) - limited scope review may be sufficient'
            audit_focus = base_assertions['focus'] + ' with reduced testing'
        
        return {
            'primary_assertion': base_assertions['primary'],
            'secondary_assertion': base_assertions['secondary'],
            'assertion_reason': assertion_reason,
            'audit_focus': audit_focus,
        }
    
    def determine_audit_priority(self):
        """
        Determine audit priority (1-10) based on overall risk score
        Higher priority = higher need for audit
        """
        overall_score = self.scores.get('overall_risk_score', Decimal('0.00'))
        
        # Convert 0-5 risk score to 1-10 priority
        priority = int((overall_score / Decimal('5')) * Decimal('10'))
        
        # Ensure minimum priority of 1 for any taxpayer with records
        if priority == 0 and overall_score > 0:
            priority = 1
        
        return max(1, min(10, priority))
    
    def recommend_audit_selection(self):
        """
        Recommend whether taxpayer should be selected for audit
        Based on overall risk level and priority - targets 5-15 audit selections, 5-20 reviews
        Adjusted for first-time GST implementation in Bhutan
        """
        overall_score = self.scores.get('overall_risk_score', Decimal('0.00'))
        risk_level = self.risk_factors.get('overall_risk_level', 'minimal')
        
        # Selection criteria for first-time GST implementation (target 5-15 audit, 5-20 review)
        if overall_score >= Decimal('3.73'):
            return 'selected'
        elif overall_score >= Decimal('3.68'):
            return 'review'
        else:
            return 'not_selected'