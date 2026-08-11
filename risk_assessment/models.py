from django.db import models
from taxpayers.models import TaxpayerMaster
from returns.models import GSTReturn
from core.models import User


class AuditAllotment(models.Model):
    """
    Audit Allotment Model - Manages audit assignments to assessors
    Links to Audit Register for tracking audit assignments
    """
    ORGANISATION_TYPES = (
        ('', '---------'),
        ('Sole Proprietorship', 'Sole Proprietorship'),
        ('Private Company', 'Private Company'),
        ('Public Company', 'Public Company'),
        ('Partnership', 'Partnership'),
        ('State Owned Company', 'State Owned Company'),
        ('Joint Venture', 'Joint Venture'),
        ('Foreign Company', 'Foreign Company'),
    )
    
    FREQUENCY_CHOICES = (
        ('', '---------'),
        ('Monthly', 'Monthly'),
        ('Quarterly', 'Quarterly'),
        ('Annual', 'Annual'),
    )
    
    DZONGKHAG_CHOICES = (
        ('', '---------'),
        ('Mongar', 'Mongar'),
        ('Trashigang', 'Trashigang'),
        ('Trashiyangtse', 'Trashiyangtse'),
        ('Lhuntse', 'Lhuntse'),
    )
    
    # Basic Information
    tax_period = models.CharField(max_length=20, default='2026-01-01', verbose_name='Tax Period')
    gstin = models.CharField(max_length=15, null=True, blank=True, verbose_name='GSTIN')
    taxpayer_name = models.CharField(max_length=200, null=True, blank=True, verbose_name='Taxpayer Name')
    dzongkhag = models.CharField(max_length=100, null=True, blank=True, choices=DZONGKHAG_CHOICES, verbose_name='Dzongkhag')
    organisation_type = models.CharField(max_length=30, null=True, blank=True, choices=ORGANISATION_TYPES, verbose_name='Organization Type')
    frequency = models.CharField(max_length=20, null=True, blank=True, choices=FREQUENCY_CHOICES, verbose_name='Frequency')
    
    # Allotment Information
    assessor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_allotments', verbose_name='Assessor')
    allotment_date = models.DateField(null=True, blank=True, verbose_name='Allotment Date')
    remarks = models.TextField(null=True, blank=True, verbose_name='Remarks')
    
    # Link to Audit Register
    audit_register = models.ForeignKey('AuditRegister', on_delete=models.SET_NULL, null=True, blank=True, related_name='allotments', verbose_name='Audit Register')
    
    # System fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_allotments')
    
    class Meta:
        verbose_name = 'Audit Allotment'
        verbose_name_plural = 'Audit Allotments'
        ordering = ['-allotment_date', 'taxpayer_name']
        indexes = [
            models.Index(fields=['tax_period']),
            models.Index(fields=['gstin']),
            models.Index(fields=['assessor']),
            models.Index(fields=['allotment_date']),
        ]
    
    def __str__(self):
        return f"{self.taxpayer_name} - {self.tax_period}"


class AuditRegister(models.Model):
    """
    Audit Register Model - Exact field specifications (auto-populated from Taxpayer Master and GST Return)
    """
    ORGANISATION_TYPES = (
        ('', '---------'),
        ('Sole Proprietorship', 'Sole Proprietorship'),
        ('Private Company', 'Private Company'),
        ('Public Company', 'Public Company'),
        ('Partnership', 'Partnership'),
        ('State Owned Company', 'State Owned Company'),
        ('Joint Venture', 'Joint Venture'),
        ('Foreign Company', 'Foreign Company'),
    )
    
    FREQUENCY_CHOICES = (
        ('', '---------'),
        ('Monthly', 'Monthly'),
        ('Quarterly', 'Quarterly'),
        ('Annual', 'Annual'),
    )
    
    DZONGKHAG_CHOICES = (
        ('', '---------'),
        ('Mongar', 'Mongar'),
        ('Trashigang', 'Trashigang'),
        ('Trashiyangtse', 'Trashiyangtse'),
        ('Lhuntse', 'Lhuntse'),
    )
    
    ASSESSMENT_TYPES = (
        ('', '---------'),
        ('comprehensive', 'Comprehensive Assessment'),
        ('limited', 'Limited Assessment'),
        ('desk_audit', 'Desk Audit'),
        ('investigation', 'Investigation'),
    )
    
    STATUS_CHOICES = (
        ('', '---------'),
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('closed', 'Closed'),
        ('reopened', 'Reopened'),
    )
    
    # Assessment Information
    asc_no = models.CharField(max_length=50, unique=True, verbose_name='ASC No.')
    assessment_date = models.DateField(verbose_name='Assessment Date')
    tax_period = models.CharField(max_length=20, verbose_name='Tax Period')
    
    # Taxpayer Information (from Taxpayer Master)
    gstin = models.CharField(max_length=15, verbose_name='GSTIN')
    taxpayer_name = models.CharField(max_length=200, verbose_name='Taxpayer Name')
    dzongkhag = models.CharField(max_length=100, choices=DZONGKHAG_CHOICES, verbose_name='Dzongkhag')
    organisation_type = models.CharField(max_length=30, choices=ORGANISATION_TYPES, verbose_name='Organisation Type')
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, verbose_name='Frequency')
    assessment_type = models.CharField(max_length=30, choices=ASSESSMENT_TYPES, verbose_name='Assessment Type')
    
    # GST Return Information (Declared) - Auto-pulled from GST Returns
    declared_sales = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='Declared Sales (GST Return)')
    gst_on_declared_sales = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='GST on Declared Sales')
    declared_import_value = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='Declared Import Value (GST Return)')
    gst_on_declared_import = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='GST on Declared Import')
    declared_domestic_purchase = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='Declared Domestic Purchase & Taxable Expenses (GST Return)')
    gst_on_declared_domestic_purchase = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='GST on Declared Domestic Purchase')
    
    # Assessed Information (from eCMS) - Manual entry
    assessed_sales_turnover = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='Assessed Sales Turnover')
    actual_import_value = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='Actual Import Value (eCMS)')
    assessed_import_value = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='Assessed Import Value')
    gst_on_assessed_import_value = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='GST on Assessed Import Value (Auto-calculated)')
    assessed_domestic_purchase = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='Assessed Domestic Purchase & Taxable Expenses')
    gst_on_assessed_domestic_purchase = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='GST on Assessed Domestic Purchase (Auto-calculated)')
    
    # GST Payable/Refundable - Auto-pulled from GST Returns and auto-calculated
    gst_payable_refundable_return = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='GST Payable / Refundable (GST Return - Auto)')
    gst_payable_refundable_assessed = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='GST Payable / Refundable (Assessed - Auto-calculated)')
    
    # Variation Analysis - Auto-calculated
    variation = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='Variation (Auto-calculated)')
    variation_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Variation % (Auto-calculated)')
    
    # Assessment Details
    reason_code = models.CharField(max_length=50, blank=True, verbose_name='Reason Code')
    discrepancy = models.TextField(blank=True, verbose_name='Discrepancy')
    assessment_audit_outcome = models.TextField(blank=True, verbose_name='Assessment/Audit Outcome')
    action_taken = models.TextField(blank=True, verbose_name='Action Taken')
    
    # Status and Timeline
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Status')
    case_closed_date = models.DateField(null=True, blank=True, verbose_name='Case Closed Date')
    assessment_duration_days = models.IntegerField(default=0, verbose_name='Assessment Duration (Days)')
    
    # Assessor Information
    assessor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assessments', verbose_name='Assessor')
    
    # System Fields
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_audit_registers')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_audit_registers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-assessment_date', 'taxpayer_name']
        verbose_name = 'Audit Register'
        verbose_name_plural = 'Audit Registers'
        indexes = [
            models.Index(fields=['asc_no']),
            models.Index(fields=['gstin', 'tax_period']),
            models.Index(fields=['assessment_date']),
            models.Index(fields=['status']),
            models.Index(fields=['assessment_type']),
        ]
    
    def __str__(self):
        return f"{self.asc_no} - {self.taxpayer_name} ({self.assessment_date})"
    
    @property
    def has_variation(self):
        return self.variation != 0
    
    @property
    def is_overdue(self):
        if self.assessment_date and self.status == 'pending':
            from django.utils import timezone
            return timezone.now().date() > self.assessment_date
        return False
    
    def save(self, *args, **kwargs):
        """Auto-calculate fields before saving"""
        from decimal import Decimal
        
        # Auto-calculate GST on Assessed Import Value (5% of Assessed Import Value)
        if self.assessed_import_value:
            self.gst_on_assessed_import_value = self.assessed_import_value * Decimal('0.05')
        
        # Auto-calculate GST on Assessed Domestic Purchase (5% of Assessed Domestic Purchase)
        if self.assessed_domestic_purchase:
            self.gst_on_assessed_domestic_purchase = self.assessed_domestic_purchase * Decimal('0.05')
        
        # Auto-calculate GST Payable/Refundable (Assessed)
        # Formula: (GST on Assessed Import + GST on Assessed Domestic Purchase) - (GST on Declared Sales + GST on Declared Domestic Purchase + GST on Declared Import)
        total_gst_assessed = (self.gst_on_assessed_import_value or Decimal('0') + 
                              self.gst_on_assessed_domestic_purchase or Decimal('0'))
        total_gst_declared = (self.gst_on_declared_sales or Decimal('0') + 
                               self.gst_on_declared_domestic_purchase or Decimal('0') + 
                               self.gst_on_declared_import or Decimal('0'))
        self.gst_payable_refundable_assessed = total_gst_assessed - total_gst_declared
        
        # Auto-calculate Variation (Assessed Sales Turnover - Declared Sales)
        if self.assessed_sales_turnover and self.declared_sales:
            self.variation = self.assessed_sales_turnover - self.declared_sales
            
            # Auto-calculate Variation %
            if self.declared_sales != 0:
                self.variation_percentage = (self.variation / self.declared_sales) * Decimal('100')
            else:
                self.variation_percentage = Decimal('0')
        
        # Auto-calculate Assessment Duration (Days)
        if self.case_closed_date and self.assessment_date:
            from datetime import datetime
            try:
                duration = (self.case_closed_date - self.assessment_date).days
                self.assessment_duration_days = max(0, duration)
            except:
                self.assessment_duration_days = 0
        
        super().save(*args, **kwargs)

class ComplianceRiskRegister(models.Model):
    """
    Compliance Risk Register Model - Automated Risk Assessment Framework
    """
    RISK_LEVELS = (
        ('low', 'Low (0.00-1.49)'),
        ('moderate', 'Moderate (1.50-2.49)'),
        ('medium', 'Medium (2.50-3.49)'),
        ('high', 'High (3.50-4.24)'),
        ('critical', 'Critical (4.25-5.00)'),
    )
    
    ASSESSMENT_STATUS = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('under_review', 'Under Review'),
        ('finalized', 'Finalized'),
    )
    
    AUDIT_SELECTION = (
        ('selected', 'Selected'),
        ('review', 'Review'),
        ('not_selected', 'Not Selected'),
    )
    
    # Taxpayer Information
    risk_id = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name='Risk ID')
    taxpayer = models.ForeignKey(TaxpayerMaster, on_delete=models.SET_NULL, null=True, blank=True, related_name='risk_registers')
    assessment_period = models.CharField(max_length=20, blank=True, verbose_name='Assessment Period')
    audit_register = models.ForeignKey('AuditRegister', on_delete=models.SET_NULL, null=True, blank=True, related_name='risk_registers', verbose_name='Linked Audit Register')
    
    # Taxpayer Profile (from Taxpayer Master)
    gstin = models.CharField(max_length=15, blank=True, verbose_name='GSTIN')
    taxpayer_name = models.CharField(max_length=200, blank=True, verbose_name='Taxpayer Name')
    business_name = models.CharField(max_length=200, blank=True, verbose_name='Business Name')
    activity = models.CharField(max_length=100, blank=True, verbose_name='Activity')
    sector = models.CharField(max_length=100, blank=True, verbose_name='Sector')
    sub_sector = models.CharField(max_length=100, blank=True, verbose_name='Sub-Sector')
    organisation_type = models.CharField(max_length=30, blank=True, verbose_name='Organisation Type')
    frequency = models.CharField(max_length=20, blank=True, verbose_name='Frequency')
    dzongkhag = models.CharField(max_length=100, blank=True, verbose_name='Dzongkhag')
    
    # Taxpayer Status
    registration_date = models.DateField(null=True, blank=True, verbose_name='Registration Date')
    taxpayer_status = models.CharField(max_length=20, blank=True, verbose_name='Taxpayer Status')
    
    # Risk Scores (5 Dimensions - 0 to 5 scale)
    inherent_risk = models.DecimalField(max_digits=3, decimal_places=2, default=0, verbose_name='Inherent Risk (0-5)')
    control_risk = models.DecimalField(max_digits=3, decimal_places=2, default=0, verbose_name='Control Risk (0-5)')
    detection_risk = models.DecimalField(max_digits=3, decimal_places=2, default=0, verbose_name='Detection Risk (0-5)')
    gst_behaviour_risk = models.DecimalField(max_digits=3, decimal_places=2, default=0, verbose_name='GST Behaviour Risk (0-5)')
    transaction_risk = models.DecimalField(max_digits=3, decimal_places=2, default=0, verbose_name='Transaction Risk (0-5)')
    
    # Overall Risk (0-5 scale)
    overall_risk_score = models.DecimalField(max_digits=3, decimal_places=2, default=0, verbose_name='Overall Risk Score (0-5)')
    overall_risk_level = models.CharField(max_length=20, choices=RISK_LEVELS, default='low')
    risk_rank = models.IntegerField(default=0, verbose_name='Risk Rank')
    
    # Risk Explanation
    gst_behaviour_reason = models.TextField(blank=True, verbose_name='GST Behaviour Reason')
    transaction_risk_reason = models.TextField(blank=True, verbose_name='Transaction Risk Reason')
    overall_risk_reason = models.TextField(blank=True, verbose_name='Overall Risk Reason')
    
    # Audit Assertions
    primary_assertion = models.TextField(blank=True, verbose_name='Primary Assertion')
    secondary_assertion = models.TextField(blank=True, verbose_name='Secondary Assertion')
    assertion_reason = models.TextField(blank=True, verbose_name='Assertion Reason')
    audit_focus = models.TextField(blank=True, verbose_name='Audit Focus')
    
    # Audit Decision
    audit_priority = models.IntegerField(default=0, verbose_name='Audit Priority (1-10)')
    audit_selection = models.CharField(max_length=20, choices=AUDIT_SELECTION, default='not_selected', verbose_name='Audit Selection')
    assigned_assessor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_audits', verbose_name='Assigned Assessor')
    remarks = models.TextField(blank=True, verbose_name='Remarks')
    
    # Assessment Details
    assessment_status = models.CharField(max_length=20, choices=ASSESSMENT_STATUS, default='pending')
    assessment_date = models.DateField(auto_now_add=True)
    assessed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='risk_assessments')
    
    # Risk Factors (for tracking specific indicators)
    import_sales_ratio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Import/Sales Ratio %')
    consecutive_negative_returns = models.IntegerField(default=0, verbose_name='Consecutive Negative Returns')
    consecutive_credit_filings = models.IntegerField(default=0, verbose_name='Consecutive Credit Filings')
    import_zero_sales_periods = models.IntegerField(default=0, verbose_name='High Import with Zero Sales Periods')
    high_domestic_purchases = models.BooleanField(default=False, verbose_name='High Domestic Purchases')
    cash_sales_suppression = models.BooleanField(default=False, verbose_name='Cash Sales Suppression')
    sales_variation = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Sales Variation %')
    stock_analysis_indicators = models.IntegerField(default=0, verbose_name='Stock Analysis Indicators')
    
    # Recommendations
    recommendations = models.TextField(blank=True)
    requires_immediate_audit = models.BooleanField(default=False, verbose_name='Requires Immediate Audit')
    
    # Link to Audit Register (will be populated when assessment is done)
    audit_reference = models.CharField(max_length=50, blank=True, verbose_name='Audit Reference')
    
    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-overall_risk_score', 'taxpayer']
        verbose_name = 'Compliance Risk Register'
        verbose_name_plural = 'Compliance Risk Registers'
        indexes = [
            models.Index(fields=['risk_id']),
            models.Index(fields=['taxpayer', 'assessment_period']),
            models.Index(fields=['overall_risk_level']),
            models.Index(fields=['overall_risk_score']),
            models.Index(fields=['assessment_status']),
            models.Index(fields=['audit_selection']),
        ]
        unique_together = ['taxpayer', 'assessment_period']
    
    def __str__(self):
        return f"{self.risk_id} - {self.taxpayer_name} ({self.overall_risk_level})"
    
    def calculate_overall_risk(self):
        """Calculate overall risk score based on 5 dimensions (0-5 scale)"""
        from decimal import Decimal
        overall = (
            (self.inherent_risk * Decimal('0.20')) +
            (self.control_risk * Decimal('0.20')) +
            (self.detection_risk * Decimal('0.15')) +
            (self.gst_behaviour_risk * Decimal('0.20')) +
            (self.transaction_risk * Decimal('0.25'))
        )
        return round(overall, 2)
    
    def determine_risk_level(self):
        """Determine risk level based on overall score (0-5 scale)"""
        score = self.overall_risk_score
        if score >= 4.25:
            return 'critical'
        elif score >= 3.50:
            return 'high'
        elif score >= 2.50:
            return 'medium'
        elif score >= 1.50:
            return 'moderate'
        else:
            return 'low'
    
    def save(self, *args, **kwargs):
        # Auto-calculate from taxpayer if linked
        if self.taxpayer and not self.gstin:
            self.gstin = self.taxpayer.gstin
            self.taxpayer_name = self.taxpayer.taxpayer_name
            self.business_name = self.taxpayer.business_name
            self.activity = self.taxpayer.activity
            self.sector = self.taxpayer.sector
            self.sub_sector = self.taxpayer.sub_sector
            self.organisation_type = self.taxpayer.organisation_type
            self.frequency = self.taxpayer.frequency
            self.dzongkhag = self.taxpayer.dzongkhag
            self.registration_date = self.taxpayer.registration_date
            self.taxpayer_status = self.taxpayer.status
        
        # Auto-calculate overall risk score and level
        self.overall_risk_score = self.calculate_overall_risk()
        self.overall_risk_level = self.determine_risk_level()
        
        # Generate risk ID if not set
        if not self.risk_id:
            self.risk_id = f"RISK-{self.taxpayer.gstin if self.taxpayer else 'UNK'}-{self.assessment_period}"
        
        super().save(*args, **kwargs)


class RiskFactorDetail(models.Model):
    """
    Individual Risk Factor Details with Scoring
    """
    FACTOR_TYPES = (
        ('import_sales', 'High Import/Low Sales'),
        ('consecutive_credit', 'Consecutive Credit Filings'),
        ('import_zero_sales', 'Import with Zero Sales'),
        ('high_purchases', 'High Domestic Purchases'),
        ('cash_suppression', 'Cash Sales Suppression'),
        ('sales_variation', 'Sales Variation'),
        ('stock_analysis', 'Stock Analysis'),
        ('filing_compliance', 'Filing Compliance'),
    )
    
    risk_register = models.ForeignKey(ComplianceRiskRegister, on_delete=models.CASCADE, related_name='risk_factors')
    factor_type = models.CharField(max_length=30, choices=FACTOR_TYPES)
    
    factor_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    factor_score = models.IntegerField(default=0, verbose_name='Factor Score')
    max_score = models.IntegerField(default=25, verbose_name='Maximum Score')
    
    description = models.TextField(blank=True)
    severity = models.CharField(max_length=20, choices=ComplianceRiskRegister.RISK_LEVELS, default='low')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Risk Factor Detail'
        verbose_name_plural = 'Risk Factor Details'
    
    def __str__(self):
        return f"{self.get_factor_type_display()} - {self.factor_score}/{self.max_score}"


class RiskAlert(models.Model):
    """
    Risk Alerts and Notifications
    """
    ALERT_TYPES = (
        ('critical', 'Critical Alert'),
        ('warning', 'Warning'),
        ('information', 'Information'),
    )
    
    ALERT_STATUS = (
        ('active', 'Active'),
        ('acknowledged', 'Acknowledged'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    )
    
    taxpayer = models.ForeignKey(TaxpayerMaster, on_delete=models.SET_NULL, null=True, blank=True, related_name='risk_alerts')
    risk_register = models.ForeignKey(ComplianceRiskRegister, on_delete=models.SET_NULL, null=True, related_name='alerts')
    
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES, default='information')
    alert_status = models.CharField(max_length=20, choices=ALERT_STATUS, default='active')
    
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    acknowledged_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='acknowledged_alerts')
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution_notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Risk Alert'
        verbose_name_plural = 'Risk Alerts'
        indexes = [
            models.Index(fields=['taxpayer']),
            models.Index(fields=['alert_status']),
            models.Index(fields=['alert_type']),
        ]
    
    def __str__(self):
        if self.taxpayer:
            return f"{self.title} - {self.taxpayer.taxpayer_name}"
        return f"{self.title} - Unknown Taxpayer"