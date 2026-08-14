from django.db import models
from core.models import User
from compliance.models import ComplianceRiskReferral
from returns.models import GSTReturn
from taxpayers.models import TaxpayerMaster


class AuditCase(models.Model):
    """Audit Case - automatically created from Compliance Risk where Final = AUDIT"""
    
    ASSESSMENT_TYPES = (
        ('desk_assessment', 'Desk Assessment'),
        ('field_audit', 'Field Audit'),
        ('targeted_audit', 'Targeted Audit'),
        ('other', 'Other'),
    )
    
    AUDIT_PRIORITIES = (
        ('critical', 'Critical'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    )
    
    STATUS_CHOICES = (
        ('referred', 'Referred'),
        ('pending_assignment', 'Pending Assignment'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('field_audit', 'Field Audit'),
        ('assessment', 'Assessment'),
        ('completed', 'Completed'),
        ('closed', 'Closed'),
    )
    
    # Case Information
    audit_case_id = models.CharField(max_length=20, unique=True, verbose_name='Audit Case ID')
    risk_referral = models.ForeignKey(ComplianceRiskReferral, on_delete=models.PROTECT, verbose_name='Risk Referral')
    assessment_date = models.DateField(verbose_name='Assessment Date')
    from_tax_period = models.CharField(max_length=20, verbose_name='From Tax Period')
    to_tax_period = models.CharField(max_length=20, verbose_name='To Tax Period')
    gstin = models.CharField(max_length=15, verbose_name='GSTIN')
    taxpayer_name = models.CharField(max_length=200, verbose_name='Taxpayer Name')
    dzongkhag = models.CharField(max_length=100, blank=True, verbose_name='Dzongkhag')
    organisation_type = models.CharField(max_length=50, blank=True, verbose_name='Organisation Type')
    frequency = models.CharField(max_length=20, blank=True, verbose_name='Frequency')
    assessment_type = models.CharField(max_length=20, choices=ASSESSMENT_TYPES, verbose_name='Assessment Type')
    audit_priority = models.CharField(max_length=20, choices=AUDIT_PRIORITIES, default='medium', verbose_name='Audit Priority')
    
    # Assignment
    assigned_officer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_audit_cases', verbose_name='Assigned Officer')
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_assignments', verbose_name='Assigned By')
    assigned_date = models.DateField(null=True, blank=True, verbose_name='Assigned Date')
    due_date = models.DateField(null=True, blank=True, verbose_name='Due Date')
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='referred', verbose_name='Status')
    case_closed_date = models.DateField(null=True, blank=True, verbose_name='Case Closed Date')
    assessment_duration = models.IntegerField(null=True, blank=True, verbose_name='Assessment Duration (Days)')
    
    # Original assessor from risk assessment
    assessor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assessed_audit_cases', verbose_name='Assessor')
    
    # Remarks
    remarks = models.TextField(blank=True, verbose_name='Remarks')
    
    # System fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Audit Case'
        verbose_name_plural = 'Audit Cases'
        indexes = [
            models.Index(fields=['audit_case_id']),
            models.Index(fields=['gstin']),
            models.Index(fields=['status']),
            models.Index(fields=['assigned_officer']),
            models.Index(fields=['from_tax_period']),
        ]
    
    def __str__(self):
        return f"{self.audit_case_id} - {self.taxpayer_name}"


class AuditAssessment(models.Model):
    """Audit Assessment - detailed assessment calculations and findings"""
    
    OUTCOME_CHOICES = (
        ('no_discrepancy', 'No Discrepancy'),
        ('adjustment_required', 'Adjustment Required'),
        ('additional_gst_payable', 'Additional GST Payable'),
        ('itc_disallowed', 'ITC Disallowed'),
        ('refund_adjustment', 'Refund Adjustment'),
        ('penalty_enforcement', 'Penalty / Enforcement Referral'),
        ('other', 'Other'),
    )
    
    ACTION_CHOICES = (
        ('accepted', 'Accepted'),
        ('adjusted', 'Adjusted'),
        ('itc_disallowed', 'ITC Disallowed'),
        ('additional_gst_assessed', 'Additional GST Assessed'),
        ('referred_enforcement', 'Referred for Enforcement'),
        ('other', 'Other'),
    )
    
    # Case Information
    audit_case = models.ForeignKey(AuditCase, on_delete=models.CASCADE, related_name='assessments', verbose_name='Audit Case')
    asc_no = models.CharField(max_length=20, unique=True, verbose_name='ASC No.')
    assessment_date = models.DateField(verbose_name='Assessment Date')
    tax_period = models.CharField(max_length=20, verbose_name='Tax Period')
    gstin = models.CharField(max_length=15, verbose_name='GSTIN')
    taxpayer_name = models.CharField(max_length=200, verbose_name='Taxpayer Name')
    dzongkhag = models.CharField(max_length=100, blank=True, verbose_name='Dzongkhag')
    organisation_type = models.CharField(max_length=50, blank=True, verbose_name='Organisation Type')
    frequency = models.CharField(max_length=20, blank=True, verbose_name='Frequency')
    assessment_type = models.CharField(max_length=20, blank=True, verbose_name='Assessment Type')
    
    # GST Return Information (Auto-fetched)
    gst_return = models.ForeignKey(GSTReturn, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='GST Return')
    declared_sales = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='Declared Sales (GST Return)')
    gst_on_declared_sales = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='GST on Declared Sales')
    declared_import_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='Declared Import Value (GST Return)')
    gst_on_declared_import = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='GST on Declared Import')
    declared_domestic_purchase = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='Declared Domestic Purchase & Taxable Expenses')
    gst_on_declared_domestic_purchase = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='GST on Declared Domestic Purchase')
    itc = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='ITC')
    gst_payable_refundable_return = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='GST Payable / Refundable (GST Return)')
    actual_payment = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='Actual Payment')
    
    # Assessed Information (Officer enters)
    assessed_sales_turnover = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='Assessed Sales Turnover')
    actual_import_value_ecms = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='Actual Import Value (eCMS)')
    assessed_import_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='Assessed Import Value')
    gst_on_assessed_import = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='GST on Assessed Import Value')
    assessed_domestic_purchase = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='Assessed Domestic Purchase & Taxable Expenses')
    gst_on_assessed_domestic_purchase = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='GST on Assessed Domestic Purchase')
    gst_payable_refundable_assessed = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='GST Payable / Refundable (Assessed)')
    
    # Calculations
    variation = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='Variation')
    variation_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Variation %')
    
    # Findings
    reason_code = models.CharField(max_length=20, blank=True, verbose_name='Reason Code')
    discrepancy = models.TextField(blank=True, verbose_name='Discrepancy')
    
    # Outcome
    assessment_outcome = models.CharField(max_length=30, choices=OUTCOME_CHOICES, blank=True, verbose_name='Assessment / Audit Outcome')
    action_taken = models.CharField(max_length=30, choices=ACTION_CHOICES, blank=True, verbose_name='Action Taken')
    
    # Status
    status = models.CharField(max_length=20, blank=True, verbose_name='Status')
    case_closed_date = models.DateField(null=True, blank=True, verbose_name='Case Closed Date')
    assessment_duration = models.IntegerField(null=True, blank=True, verbose_name='Assessment Duration (Days)')
    
    # Assessor
    assessor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_assessments', verbose_name='Assessor')
    
    # System fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Audit Assessment'
        verbose_name_plural = 'Audit Assessments'
        indexes = [
            models.Index(fields=['asc_no']),
            models.Index(fields=['audit_case']),
            models.Index(fields=['gstin']),
        ]
    
    def __str__(self):
        return f"{self.asc_no} - {self.taxpayer_name}"


class AuditFinding(models.Model):
    """Audit Findings - detailed findings for an audit case"""
    
    FINDING_TYPES = (
        ('under_declared_sales', 'Under-declared Sales'),
        ('incorrect_itc', 'Incorrect ITC'),
        ('import_discrepancy', 'Import Discrepancy'),
        ('incorrect_gst_calculation', 'Incorrect GST Calculation'),
        ('non_filing', 'Non-Filing'),
        ('non_payment', 'Non-Payment'),
        ('other', 'Other'),
    )
    
    # Finding Information
    finding_id = models.CharField(max_length=20, unique=True, verbose_name='Finding ID')
    audit_case = models.ForeignKey(AuditCase, on_delete=models.CASCADE, related_name='findings', verbose_name='Audit Case')
    reason_code = models.CharField(max_length=20, blank=True, verbose_name='Reason Code')
    finding_type = models.CharField(max_length=30, choices=FINDING_TYPES, verbose_name='Finding Type')
    discrepancy = models.TextField(blank=True, verbose_name='Discrepancy')
    amount_involved = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='Amount Involved')
    description = models.TextField(blank=True, verbose_name='Description')
    action_taken = models.TextField(blank=True, verbose_name='Action Taken')
    auditor_remarks = models.TextField(blank=True, verbose_name='Auditor Remarks')
    
    # System fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Audit Finding'
        verbose_name_plural = 'Audit Findings'
        indexes = [
            models.Index(fields=['finding_id']),
            models.Index(fields=['audit_case']),
        ]
    
    def __str__(self):
        return f"{self.finding_id} - {self.audit_case.audit_case_id}"


class RefundRegister(models.Model):
    """
    Refund Register Model - moved from refunds app to audit_refund app
    """
    STATUS_CHOICES = (
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('processing', 'Processing'),
        ('paid', 'Paid'),
        ('closed', 'Closed'),
    )
    
    # Identification
    refund_id = models.CharField(max_length=50, unique=True, verbose_name='Refund ID')
    gst_tpn = models.CharField(max_length=15, verbose_name='GST TPN')
    taxpayer_name = models.CharField(max_length=200, verbose_name='Taxpayer Name')
    
    # Period and Claim Details
    tax_period = models.CharField(max_length=20, verbose_name='Tax Period')
    claim_date = models.DateField(verbose_name='Claim Date')
    claimed_amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Claimed Amount')
    
    # GST Return Reference
    gst_return = models.ForeignKey('returns.GSTReturn', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='GST Return', related_name='refund_registers_audit')
    
    # Compliance Risk Reference (optional)
    risk_referral = models.ForeignKey('compliance.ComplianceRiskReferral', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Risk Referral', related_name='refund_registers_audit')
    
    # Audit Case Reference (optional)
    audit_case = models.ForeignKey('AuditCase', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Audit Case', related_name='linked_refunds_audit')
    
    # Adjustment and Approval Details
    adjustment = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='Adjustment')
    refund_disallowed = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='Refund Disallowed')
    refund_approved = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='Refund Approved')
    refund_adjustment_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Refund Adjustment %')
    
    # Processing Details
    processing_days = models.IntegerField(default=0, verbose_name='Processing Days')
    processed_date = models.DateField(null=True, blank=True, verbose_name='Processed Date')
    processed_by = models.CharField(max_length=100, blank=True, verbose_name='Processed By')
    
    # Status and Reason
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted', verbose_name='Status')
    refund_reason = models.TextField(blank=True, verbose_name='Refund Reason')
    reason_code = models.CharField(max_length=50, blank=True, verbose_name='Reason Code')
    remarks = models.TextField(blank=True, verbose_name='Remarks')
    
    # System Fields
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_refunds_audit')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_refunds_audit')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-claim_date']
        verbose_name = 'Refund Register'
        verbose_name_plural = 'Refund Registers'
        indexes = [
            models.Index(fields=['refund_id']),
            models.Index(fields=['gst_tpn']),
            models.Index(fields=['tax_period']),
            models.Index(fields=['status']),
            models.Index(fields=['claim_date']),
        ]
    
    def __str__(self):
        return f"{self.refund_id} - {self.taxpayer_name} (Nu. {self.claimed_amount})"
    
    @property
    def is_approved(self):
        return self.status == 'approved'
    
    @property
    def is_paid(self):
        return self.status == 'paid'