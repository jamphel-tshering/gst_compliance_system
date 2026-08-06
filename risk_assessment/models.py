from django.db import models
from taxpayers.models import TaxpayerMaster
from returns.models import GSTReturn
from core.models import User


class AuditRegister(models.Model):
    """
    Audit Register Model - Exact field specifications (auto-populated from Taxpayer Master and GST Return)
    """
    ORGANISATION_TYPES = (
        ('sole_proprietorship', 'Sole Proprietorship'),
        ('private_company', 'Private Company'),
        ('public_company', 'Public Company'),
        ('partnership', 'Partnership'),
        ('llp', 'Limited Liability Partnership'),
        ('trust', 'Trust'),
        ('government', 'Government Entity'),
        ('other', 'Other'),
    )
    
    FREQUENCY_CHOICES = (
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annual', 'Annual'),
    )
    
    ASSESSMENT_TYPES = (
        ('comprehensive', 'Comprehensive Assessment'),
        ('limited', 'Limited Assessment'),
        ('desk_audit', 'Desk Audit'),
        ('investigation', 'Investigation'),
    )
    
    STATUS_CHOICES = (
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
    dzongkhag = models.CharField(max_length=100, verbose_name='Dzongkhag')
    organisation_type = models.CharField(max_length=30, choices=ORGANISATION_TYPES, verbose_name='Organisation Type')
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, verbose_name='Frequency')
    assessment_type = models.CharField(max_length=30, choices=ASSESSMENT_TYPES, verbose_name='Assessment Type')
    
    # GST Return Information (Declared)
    declared_sales = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='Declared Sales (GST Return)')
    gst_on_declared_sales = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='GST on Declared Sales')
    declared_import_value = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='Declared Import Value (GST Return)')
    gst_on_declared_import = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='GST on Declared Import')
    declared_domestic_purchase = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='Declared Domestic Purchase & Taxable Expenses (GST Return)')
    gst_on_declared_domestic_purchase = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='GST on Declared Domestic Purchase')
    
    # Assessed Information (from eCMS)
    assessed_sales_turnover = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='Assessed Sales Turnover')
    actual_import_value = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='Actual Import Value (eCMS)')
    assessed_import_value = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='Assessed Import Value')
    gst_on_assessed_import_value = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='GST on Assessed Import Value')
    assessed_domestic_purchase = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='Assessed Domestic Purchase & Taxable Expenses')
    gst_on_assessed_domestic_purchase = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='GST on Assessed Domestic Purchase & Taxable Expenses')
    
    # GST Payable/Refundable
    gst_payable_refundable_return = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='GST Payable / Refundable (GST Return)')
    gst_payable_refundable_assessed = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='GST Payable / Refundable (Assessed)')
    
    # Variation Analysis
    variation = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='Variation')
    variation_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Variation %')
    
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

class ComplianceRiskRegister(models.Model):
    """
    Compliance Risk Register Model - Designed based on your existing risk framework
    """
    RISK_CATEGORIES = (
        ('critical', 'Critical Risk (80-100)'),
        ('high', 'High Risk (60-79)'),
        ('medium', 'Medium Risk (40-59)'),
        ('low', 'Low Risk (20-39)'),
        ('minimal', 'Minimal Risk (0-19)'),
    )
    
    ASSESSMENT_STATUS = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('under_review', 'Under Review'),
        ('finalized', 'Finalized'),
    )
    
    # Taxpayer Information
    taxpayer = models.ForeignKey(TaxpayerMaster, on_delete=models.CASCADE, related_name='risk_registers')
    assessment_period = models.CharField(max_length=20, verbose_name='Assessment Period')
    
    # Risk Scores (5 Dimensions as per your framework)
    inherent_risk = models.IntegerField(default=0, verbose_name='Inherent Risk (20%)')
    control_risk = models.IntegerField(default=0, verbose_name='Control Risk (15%)')
    detection_risk = models.IntegerField(default=0, verbose_name='Detection Risk (15%)')
    transaction_risk = models.IntegerField(default=0, verbose_name='Transaction Risk (25%)')
    behavior_risk = models.IntegerField(default=0, verbose_name='Behavior Risk (25%)')
    
    # Overall Risk Score
    overall_risk_score = models.IntegerField(default=0, verbose_name='Overall Risk Score')
    risk_category = models.CharField(max_length=20, choices=RISK_CATEGORIES, default='minimal')
    
    # Assessment Details
    assessment_status = models.CharField(max_length=20, choices=ASSESSMENT_STATUS, default='pending')
    assessment_date = models.DateField(auto_now_add=True)
    assessed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='risk_assessments')
    
    # Risk Factors (from your existing system)
    import_sales_ratio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Import/Sales Ratio %')
    consecutive_negative_returns = models.IntegerField(default=0, verbose_name='Consecutive Negative Returns')
    import_zero_sales_periods = models.IntegerField(default=0, verbose_name='Import with Zero Sales Periods')
    high_domestic_purchases = models.BooleanField(default=False, verbose_name='High Domestic Purchases')
    cash_sales_suppression = models.BooleanField(default=False, verbose_name='Cash Sales Suppression')
    sales_variation = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Sales Variation %')
    
    # Recommendations and Actions
    recommendations = models.TextField(blank=True)
    audit_priority = models.IntegerField(default=0, verbose_name='Audit Priority (1-10)')
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
            models.Index(fields=['taxpayer', 'assessment_period']),
            models.Index(fields=['risk_category']),
            models.Index(fields=['overall_risk_score']),
            models.Index(fields=['assessment_status']),
        ]
        unique_together = ['taxpayer', 'assessment_period']
    
    def __str__(self):
        return f"{self.taxpayer.taxpayer_name} - {self.assessment_period} ({self.risk_category})"
    
    def calculate_overall_risk(self):
        """Calculate overall risk score based on 5 dimensions"""
        overall = (
            (self.inherent_risk * 0.20) +
            (self.control_risk * 0.15) +
            (self.detection_risk * 0.15) +
            (self.transaction_risk * 0.25) +
            (self.behavior_risk * 0.25)
        )
        return int(overall)
    
    def determine_risk_category(self):
        """Determine risk category based on overall score"""
        score = self.overall_risk_score
        if score >= 80:
            return 'critical'
        elif score >= 60:
            return 'high'
        elif score >= 40:
            return 'medium'
        elif score >= 20:
            return 'low'
        else:
            return 'minimal'
    
    def save(self, *args, **kwargs):
        self.overall_risk_score = self.calculate_overall_risk()
        self.risk_category = self.determine_risk_category()
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
    severity = models.CharField(max_length=20, choices=ComplianceRiskRegister.RISK_CATEGORIES, default='minimal')
    
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
    
    taxpayer = models.ForeignKey(TaxpayerMaster, on_delete=models.CASCADE, related_name='risk_alerts')
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
        return f"{self.title} - {self.taxpayer.taxpayer_name}"