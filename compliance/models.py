from django.db import models
from taxpayers.models import TaxpayerMaster
from returns.models import GSTReturn
from core.models import User


class ComplianceMonitoring(models.Model):
    """
    Compliance Monitoring Model - Tracks routine GST compliance
    """
    COMPLIANCE_STATUS_CHOICES = (
        ('Compliant', 'Compliant'),
        ('Late Filer', 'Late Filer'),
        ('Non-Filer', 'Non-Filer'),
        ('Payment Default', 'Payment Default'),
        ( 'Other Non-Compliance', 'Other Non-Compliance'),
    )
    
    COMPLIANCE_FLAG_CHOICES = (
        ('Green', 'Green'),
        ('Yellow', 'Yellow'),
        ('Red', 'Red'),
    )
    
    # Assessment Information
    compliance_id = models.CharField(max_length=20, unique=True, blank=True, null=True, verbose_name='Compliance ID')
    tax_period = models.CharField(max_length=20, verbose_name='Tax Period')
    assessment_date = models.DateField(auto_now_add=True, verbose_name='Assessment Date')
    
    # Taxpayer Information (from GST Returns, not duplicated)
    gstin = models.CharField(max_length=15, verbose_name='GSTIN')
    taxpayer_name = models.CharField(max_length=200, verbose_name='Taxpayer Name')
    
    # Compliance Details (calculated from GST Returns)
    filing_status = models.CharField(max_length=20, blank=True, null=True, verbose_name='Filing Status')
    filing_delay = models.IntegerField(default=0, null=True, blank=True, verbose_name='Filing Delay (Days)')
    payment_status = models.CharField(max_length=30, blank=True, null=True, verbose_name='Payment Status')
    compliance_status = models.CharField(max_length=30, choices=COMPLIANCE_STATUS_CHOICES, blank=True, null=True, verbose_name='Compliance Status')
    compliance_flag = models.CharField(max_length=10, choices=COMPLIANCE_FLAG_CHOICES, blank=True, null=True, verbose_name='Compliance Flag')
    
    # Additional Information
    remarks = models.TextField(blank=True, null=True, verbose_name='Remarks')
    
    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-tax_period', 'taxpayer_name']
        verbose_name = 'Compliance & Enforcement'
        verbose_name_plural = 'Compliance & Enforcement'
        indexes = [
            models.Index(fields=['gstin', 'tax_period']),
            models.Index(fields=['tax_period']),
            models.Index(fields=['compliance_status']),
            models.Index(fields=['compliance_flag']),
        ]
        unique_together = ['gstin', 'tax_period']
    
    def __str__(self):
        return f"{self.compliance_id} - {self.taxpayer_name} ({self.tax_period})"
    
    def save(self, *args, **kwargs):
        # Auto-generate compliance ID if not set
        if not self.compliance_id:
            from datetime import datetime
            year = datetime.now().year
            count = ComplianceMonitoring.objects.filter(compliance_id__startswith=f'CM{year}').count()
            self.compliance_id = f'CM{year}{str(count + 1).zfill(4)}'
        
        super().save(*args, **kwargs)


class ComplianceRiskReferral(models.Model):
    """
    Compliance Risk & Referral Model - Risk-based selection engine
    """
    RISK_LEVEL_CHOICES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    )
    
    RISK_TYPE_CHOICES = (
        ('Filing & Payment Risk', 'Filing & Payment Risk'),
        ('Sales & Output GST Risk', 'Sales & Output GST Risk'),
        ('Purchase & ITC Risk', 'Purchase & ITC Risk'),
        ('Import & Transaction Risk', 'Import & Transaction Risk'),
        ('Refund Risk', 'Refund Risk'),
        ('GST Behaviour & Compliance History Risk', 'GST Behaviour & Compliance History Risk'),
    )
    
    SELECTION_CHOICES = (
        ('AUDIT', 'AUDIT'),
        ('REVIEW', 'REVIEW'),
        ('MONITOR', 'MONITOR'),
        ('NOT SELECTED', 'NOT SELECTED'),
    )
    
    REFERRAL_STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Referred', 'Referred'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
    )
    
    OFFICER_RISK_RATING_CHOICES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    )
    
    ASSESSMENT_STATUS_CHOICES = (
        ('Not Assessed', 'Not Assessed'),
        ('Assessment Generated', 'Assessment Generated'),
        ('Under Officer Review', 'Under Officer Review'),
        ('Finalized', 'Finalized'),
    )
    
    ACTION_STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Assigned', 'Assigned'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    )
    
    REFERRAL_STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Referred', 'Referred'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
    )
    
    AUDIT_ASSERTION_CHOICES = (
        ('A01 – Completeness', 'A01 – Completeness'),
        ('A02 – Occurrence', 'A02 – Occurrence'),
        ('A03 – Accuracy', 'A03 – Accuracy'),
        ('A04 – Cut-off', 'A04 – Cut-off'),
        ('A05 – Classification', 'A05 – Classification'),
        ('A06 – Existence', 'A06 – Existence'),
        ('A07 – Rights & Obligations', 'A07 – Rights & Obligations'),
        ('A08 – Valuation', 'A08 – Valuation'),
        ('A09 – Compliance', 'A09 – Compliance'),
    )
    
    # Risk Assessment Information
    risk_id = models.CharField(max_length=20, unique=True, blank=True, null=True, verbose_name='Risk ID')
    assessment_from_period = models.CharField(max_length=20, verbose_name='Assessment From Period')
    assessment_to_period = models.CharField(max_length=20, verbose_name='Assessment To Period')
    assessment_date = models.DateField(auto_now_add=True, verbose_name='Assessment Date')
    assessment_status = models.CharField(max_length=30, blank=True, null=True, verbose_name='Assessment Status')
    assessor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assessed_risks', verbose_name='Assessor')
    
    # Taxpayer Information (from GST Returns, not duplicated)
    gstin = models.CharField(max_length=15, verbose_name='GSTIN')
    taxpayer_name = models.CharField(max_length=200, verbose_name='Taxpayer Name')
    
    # Risk Assessment
    risk_type = models.CharField(max_length=50, choices=RISK_TYPE_CHOICES, blank=True, null=True, verbose_name='Risk Type')
    risk_indicator = models.CharField(max_length=100, blank=True, null=True, verbose_name='Risk Indicator')
    risk_pattern = models.CharField(max_length=100, blank=True, null=True, verbose_name='Risk Pattern')
    
    # Risk Dimensions (for scoring)
    inherent_risk = models.DecimalField(max_digits=3, decimal_places=2, default=0, verbose_name='Inherent Risk (0-5)')
    control_risk = models.DecimalField(max_digits=3, decimal_places=2, default=0, verbose_name='Control Risk (0-5)')
    detection_risk = models.DecimalField(max_digits=3, decimal_places=2, default=0, verbose_name='Detection Risk (0-5)')
    gst_behaviour_risk = models.DecimalField(max_digits=3, decimal_places=2, default=0, verbose_name='GST Behaviour Risk (0-5)')
    transaction_risk = models.DecimalField(max_digits=3, decimal_places=2, default=0, verbose_name='Transaction Risk (0-5)')
    
    risk_score = models.DecimalField(max_digits=3, decimal_places=2, default=0, verbose_name='Risk Score (0-5)')
    risk_level = models.CharField(max_length=20, choices=RISK_LEVEL_CHOICES, blank=True, null=True, verbose_name='Risk Level')
    
    # Audit Assertions
    audit_assertion = models.CharField(max_length=50, choices=AUDIT_ASSERTION_CHOICES, blank=True, null=True, verbose_name='Audit Assertion')
    risk_reason = models.TextField(blank=True, null=True, verbose_name='Risk Reason')
    
    # Selection & Referral (System-Generated Only)
    system_decision = models.CharField(max_length=20, choices=SELECTION_CHOICES, blank=True, null=True, verbose_name='System Decision', editable=False)
    selection = models.CharField(max_length=20, choices=SELECTION_CHOICES, blank=True, null=True, verbose_name='Selection (Auto-Generated)', editable=False)
    referred_to = models.CharField(max_length=50, blank=True, null=True, verbose_name='Referred To (Auto-Generated)', editable=False)
    
    # Prescribed Officer Action
    prescribed_officer_action = models.TextField(blank=True, null=True, verbose_name='Prescribed Officer Action', editable=False)
    
    # Officer Professional Judgment
    officer_assessment = models.TextField(blank=True, null=True, verbose_name='Officer Assessment / Judgment')
    additional_risk_factor = models.TextField(blank=True, null=True, verbose_name='Additional Risk Factor')
    officer_risk_rating = models.CharField(max_length=20, blank=True, null=True, verbose_name='Officer Risk Rating')
    officer_remarks = models.TextField(blank=True, null=True, verbose_name='Officer Remarks')
    
    # Final Selection
    final_selection = models.CharField(max_length=20, choices=SELECTION_CHOICES, blank=True, null=True, verbose_name='Final Selection')
    final_referred_to = models.CharField(max_length=50, blank=True, null=True, verbose_name='Final Referred To')
    
    # Action Status
    action_status = models.CharField(max_length=20, blank=True, null=True, verbose_name='Action Status')
    
    # Officer Override
    override_reason = models.TextField(blank=True, null=True, verbose_name='Override Reason')
    overridden_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='risk_overrides', verbose_name='Overridden By')
    override_date = models.DateTimeField(null=True, blank=True, verbose_name='Override Date')
    
    # Section Head Review & Delegation
    section_head_review = models.TextField(blank=True, null=True, verbose_name='Section Head Review Comments')
    section_head_approval = models.CharField(max_length=20, blank=True, null=True, choices=[('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Pending', 'Pending')], verbose_name='Section Head Approval')
    section_head_review_date = models.DateTimeField(null=True, blank=True, verbose_name='Section Head Review Date')
    section_head = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='section_head_reviews', verbose_name='Section Head')
    
    # Officer Assignment for Field Audit
    assigned_officer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_audits', verbose_name='Assigned Officer')
    assignment_date = models.DateTimeField(null=True, blank=True, verbose_name='Assignment Date')
    assignment_status = models.CharField(max_length=20, blank=True, null=True, choices=[('Pending', 'Pending'), ('Assigned', 'Assigned'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], verbose_name='Assignment Status')
    
    # Officer Comments on Audit
    officer_comments = models.TextField(blank=True, null=True, verbose_name='Officer Comments')
    officer_recommendation = models.CharField(max_length=50, blank=True, null=True, choices=[('Proceed with Audit', 'Proceed with Audit'), ('Monitor Only', 'Monitor Only'), ('No Action Required', 'No Action Required')], verbose_name='Officer Recommendation')
    officer_recommendation_date = models.DateTimeField(null=True, blank=True, verbose_name='Officer Recommendation Date')
    
    # Original calculated values (preserved for audit trail)
    original_risk_score = models.DecimalField(max_digits=3, decimal_places=2, default=0, verbose_name='Original Risk Score')
    original_risk_level = models.CharField(max_length=20, blank=True, null=True, verbose_name='Original Risk Level')
    original_selection = models.CharField(max_length=20, blank=True, null=True, verbose_name='Original Selection')
    original_system_decision = models.CharField(max_length=20, blank=True, null=True, verbose_name='Original System Decision')
    
    # Additional Information
    remarks = models.TextField(blank=True, null=True, verbose_name='Remarks')
    
    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-assessment_date', 'assessment_from_period', 'taxpayer_name']
        verbose_name = 'Compliance Risk & Referral'
        verbose_name_plural = 'Compliance Risk & Referral'
        indexes = [
            models.Index(fields=['gstin', 'assessment_from_period']),
            models.Index(fields=['assessment_from_period']),
            models.Index(fields=['assessment_to_period']),
            models.Index(fields=['risk_level']),
            models.Index(fields=['risk_type']),
            models.Index(fields=['system_decision']),
            models.Index(fields=['final_selection']),
            models.Index(fields=['assessment_status']),
        ]
        unique_together = ['gstin', 'assessment_from_period', 'assessment_to_period']
    
    def __str__(self):
        return f"{self.risk_id} - {self.taxpayer_name} ({self.assessment_from_period} to {self.assessment_to_period})"
    
    def save(self, *args, **kwargs):
        # Auto-generate risk ID if not set
        if not self.risk_id:
            from datetime import datetime
            year = datetime.now().year
            count = ComplianceRiskReferral.objects.filter(risk_id__startswith=f'RR{year}').count()
            self.risk_id = f'RR{year}{str(count + 1).zfill(4)}'
        
        # Preserve original values on first save
        if not self.pk:
            self.original_risk_score = self.risk_score
            self.original_risk_level = self.risk_level
            self.original_selection = self.selection
            self.original_system_decision = self.system_decision
        
        super().save(*args, **kwargs)


class EnforcementRecovery(models.Model):
    """
    Enforcement & Recovery Model - Case management
    """
    CASE_TYPE_CHOICES = (
        ('Non-Filing', 'Non-Filing'),
        ('Non-Payment', 'Non-Payment'),
        ('Recovery', 'Recovery'),
        ('Other', 'Other'),
    )
    
    STATUS_CHOICES = (
        ('Open', 'Open'),
        ('Follow-up', 'Follow-up'),
        ('Recovered', 'Recovered'),
        ('Closed', 'Closed'),
    )
    
    # Case Information
    case_id = models.CharField(max_length=20, unique=True, blank=True, null=True, verbose_name='Case ID')
    tax_period = models.CharField(max_length=20, blank=True, null=True, verbose_name='Tax Period')
    
    # Taxpayer Information
    gstin = models.CharField(max_length=15, verbose_name='GSTIN')
    taxpayer_name = models.CharField(max_length=200, verbose_name='Taxpayer Name')
    
    # Case Details
    case_type = models.CharField(max_length=20, choices=CASE_TYPE_CHOICES, blank=True, null=True, verbose_name='Case Type')
    amount_due = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='Amount Due')
    notice_date = models.DateField(null=True, blank=True, verbose_name='Notice Date')
    
    # Action & Recovery
    action_taken = models.TextField(blank=True, null=True, verbose_name='Action Taken')
    amount_recovered = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='Amount Recovered')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True, verbose_name='Status')
    
    # Additional Information
    remarks = models.TextField(blank=True, null=True, verbose_name='Remarks')
    
    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at', 'case_id']
        verbose_name = 'Enforcement & Recovery'
        verbose_name_plural = 'Enforcement & Recovery'
        indexes = [
            models.Index(fields=['gstin']),
            models.Index(fields=['case_type']),
            models.Index(fields=['status']),
            models.Index(fields=['tax_period']),
        ]
    
    def __str__(self):
        return f"{self.case_id} - {self.taxpayer_name} ({self.status})"
    
    def save(self, *args, **kwargs):
        # Auto-generate case ID if not set
        if not self.case_id:
            from datetime import datetime
            year = datetime.now().year
            count = EnforcementRecovery.objects.filter(case_id__startswith=f'ER{year}').count()
            self.case_id = f'ER{year}{str(count + 1).zfill(4)}'
        
        super().save(*args, **kwargs)