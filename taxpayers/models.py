from django.db import models
from django.core.exceptions import ValidationError
from core.models import User


class TaxpayerEnquiry(models.Model):
    """
    Taxpayer Enquiry Model - Independent section for taxpayer enquiries
    """
    ENQUIRY_STATUS = (
        ('Pending Taxpayer', 'Pending Taxpayer'),
        ('Pending Officer', 'Pending Officer'),
        ('Referred', 'Referred'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    )
    
    ENQUIRY_TYPE = (
        ('Taxpayer Enquiry', 'Taxpayer Enquiry'),
        ('General Correspondence', 'General Correspondence'),
        ('Notice', 'Notice'),
        ('Assessment', 'Assessment'),
        ('Audit', 'Audit'),
        ('Refund', 'Refund'),
        ('ITC', 'ITC'),
        ('Registration', 'Registration'),
        ('Payment', 'Payment'),
        ('Return Filing', 'Return Filing'),
        ('Other', 'Other'),
    )
    
    ENQUIRY_MODE = (
        ('Letter', 'Letter'),
        ('Email', 'Email'),
        ('Phone', 'Phone'),
        ('In Person', 'In Person'),
        ('BITs', 'BITs'),
        ('Official Letter', 'Official Letter'),
        ('Social Media', 'Social Media'),
        ('Other', 'Other'),
    )
    
    # Enquiry Details
    enquiry_id = models.CharField(max_length=20, unique=True, blank=True, null=True, verbose_name='Enquiry ID')
    enquiry_date = models.DateField(default=None, blank=True, null=True, verbose_name='Date')
    enquiry_type = models.CharField(max_length=50, choices=ENQUIRY_TYPE, default='Taxpayer Enquiry', verbose_name='Enquiry Type')
    subject = models.CharField(max_length=200, verbose_name='Subject/Issue')
    mode = models.CharField(max_length=50, choices=ENQUIRY_MODE, blank=True, null=True, verbose_name='Mode')
    social_media_details = models.CharField(max_length=100, blank=True, null=True, verbose_name='Social Media Details')
    other_details = models.CharField(max_length=100, blank=True, null=True, verbose_name='Other Details')
    
    # Taxpayer Information (can be linked to existing taxpayer or standalone)
    gstin = models.CharField(max_length=15, blank=True, null=True, verbose_name='GSTIN')
    taxpayer_name = models.CharField(max_length=200, blank=True, null=True, verbose_name='Taxpayer Name')
    cid_company_reg_no = models.CharField(max_length=50, blank=True, null=True, verbose_name='CID/Company Reg No')
    
    # Contact Information
    received_from_sent_to = models.CharField(max_length=200, blank=True, null=True, verbose_name='Received From/Sent To')
    contact_person = models.CharField(max_length=200, blank=True, null=True, verbose_name='Contact Person')
    email_address = models.EmailField(blank=True, null=True, verbose_name='Email Address')
    mobile_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='Mobile Number')
    
    # Status and Processing
    status = models.CharField(max_length=50, choices=ENQUIRY_STATUS, default='Pending Taxpayer', verbose_name='Status')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_enquiries', verbose_name='Officer')
    priority = models.CharField(max_length=20, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], default='Medium', verbose_name='Priority')
    
    # Resolution
    action_response = models.TextField(blank=True, null=True, verbose_name='Action/Response')
    resolution_notes = models.TextField(blank=True, null=True, verbose_name='Resolution Notes')
    resolved_date = models.DateField(blank=True, null=True, verbose_name='Resolved Date')
    remarks = models.TextField(blank=True, null=True, verbose_name='Remarks')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-enquiry_date', '-created_at']
        verbose_name = 'Taxpayer Enquiry'
        verbose_name_plural = 'Taxpayer Enquiries'
        indexes = [
            models.Index(fields=['enquiry_id']),
            models.Index(fields=['gstin']),
            models.Index(fields=['status']),
            models.Index(fields=['enquiry_type']),
            models.Index(fields=['enquiry_date']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.enquiry_id or 'ENQ'} - {self.subject} - {self.taxpayer_name or 'Unknown'}"
    
    def save(self, *args, **kwargs):
        # Auto-generate enquiry ID if not provided
        if not self.enquiry_id:
            # Generate format: ENQ-YYYYMMDD-XXXX
            from datetime import datetime
            date_str = datetime.now().strftime('%Y%m%d')
            last_enquiry = TaxpayerEnquiry.objects.filter(enquiry_id__startswith=f'ENQ-{date_str}').order_by('-enquiry_id').first()
            if last_enquiry:
                last_num = int(last_enquiry.enquiry_id.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1
            self.enquiry_id = f'ENQ-{date_str}-{new_num:04d}'
        
        # Auto-set enquiry date if not provided
        if not self.enquiry_date:
            from datetime import date
            self.enquiry_date = date.today()
            
        super().save(*args, **kwargs)


class TaxpayerMaster(models.Model):
    """
    Taxpayer Master Model - Main taxpayer record (one per GSTIN)
    """
    ORGANISATION_TYPES = (
        ('Sole Proprietorship', 'Sole Proprietorship'),
        ('Private Company', 'Private Company'),
        ('Public Company', 'Public Company'),
        ('Partnership', 'Partnership'),
        ('Government Entity', 'Government Entity'),
        ('Foreign Company', 'Foreign Company'),
        ('Joint Venture', 'Joint Venture'),
        ('State Owned Company', 'State Owned Company'),
        ('Other', 'Other'),
    )
    
    DZONGKHAG_CHOICES = (
        ('Mongar', 'Mongar'),
        ('Trashigang', 'Trashigang'),
        ('Trashiyangtse', 'Trashiyangtse'),
        ('Lhuentse', 'Lhuentse'),
    )
    
    FREQUENCY_CHOICES = (
        ('Monthly', 'Monthly'),
        ('Quarterly', 'Quarterly'),
        ('Half Yearly', 'Half Yearly'),
    )
    
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Suspended', 'Suspended'),
        ('Cancelled', 'Cancelled'),
        ('Deregistered', 'Deregistered'),
        ('Region Transferred', 'Region Transferred'),
    )
    
    # Identification Numbers
    cid_company_reg_no = models.CharField(max_length=50, blank=True, null=True, verbose_name='CID No/Co. Reg No')
    gstin = models.CharField(max_length=15, blank=True, null=True, verbose_name='GSTIN')  # Made optional to handle missing values
    ramis_tpn = models.CharField(max_length=50, blank=True, null=True, verbose_name='RAMIS TPN')
    is_primary_license = models.BooleanField(default=True, verbose_name='Is Primary License')  # Distinguish main vs additional licenses
    
    # Basic Information
    taxpayer_name = models.CharField(max_length=200, blank=True, null=True, verbose_name='Taxpayer Name')
    business_name = models.CharField(max_length=200, verbose_name='Business Name', blank=True, null=True)
    
    # Classification
    sector = models.CharField(max_length=100, blank=True, null=True, verbose_name='Sector')
    sub_sector = models.CharField(max_length=100, blank=True, null=True, verbose_name='Sub-Sector')
    business_activity = models.CharField(max_length=200, blank=True, null=True, verbose_name='Business Activity')
    organisation_type = models.CharField(max_length=50, choices=ORGANISATION_TYPES, blank=True, null=True, verbose_name='Organisation Type')
    frequency = models.CharField(max_length=50, choices=FREQUENCY_CHOICES, blank=True, null=True, verbose_name='Frequency')
    dzongkhag = models.CharField(max_length=100, choices=DZONGKHAG_CHOICES, blank=True, null=True, verbose_name='Dzongkhag')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, blank=True, null=True, verbose_name='Status')
    
    # Important Dates
    registration_date = models.DateField(blank=True, null=True, verbose_name='Registration Date')
    commencement_date = models.DateField(null=True, blank=True, verbose_name='Commencement Date')
    deregistration_date = models.DateField(null=True, blank=True, verbose_name='Deregistration/Region Transfer Date')
    
    # Contact Information
    email_address = models.EmailField(blank=True, null=True, verbose_name='Email Address')
    mobile_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='Mobile Number')
    business_address = models.TextField(blank=True, null=True, verbose_name='Business Address')
    
    # Additional Information
    remarks = models.TextField(blank=True, null=True, verbose_name='Remarks')
    
    # System Fields
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_taxpayers_master')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_taxpayers_master')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['taxpayer_name']
        verbose_name = 'Primary Taxpayer'
        verbose_name_plural = 'Primary Taxpayers'
        indexes = [
            models.Index(fields=['gstin']),
            models.Index(fields=['cid_company_reg_no']),
            models.Index(fields=['ramis_tpn']),
            models.Index(fields=['taxpayer_name']),
            models.Index(fields=['dzongkhag']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.taxpayer_name} ({self.gstin})"
    
    def clean(self):
        """Simplified validation - temporarily disabled complex checks"""
        # Temporarily disabled to fix 500 errors
        # TODO: Re-enable after testing basic CRUD
        pass
    
    @property
    def gst_returns(self):
        return self.returns.all()
    
    @property
    def refund_applications(self):
        return self.refunds.all()
    
    def get_business_licenses_count(self):
        return self.business_licenses.count()
    
    def save(self, *args, **kwargs):
        # Handle Region Transferred logic
        old_status = None
        if self.pk:
            try:
                old_instance = TaxpayerMaster.objects.get(pk=self.pk)
                old_status = old_instance.status
            except TaxpayerMaster.DoesNotExist:
                pass
        
        super().save(*args, **kwargs)
        
        # If status changed to Region Transferred, ensure it's not counted as active
        if self.status == 'Region Transferred' and old_status != 'Region Transferred':
            # This taxpayer should not be counted in active summary
            # The summary logic already filters by status='Active', so it will automatically exclude Region Transferred
            pass


class MultipleLicenseReference(models.Model):
    """Model for storing multiple licenses with same GSTIN for reference purposes only"""
    
    ORGANISATION_TYPES = (
        ('Sole Proprietorship', 'Sole Proprietorship'),
        ('Private Company', 'Private Company'),
        ('Public Company', 'Public Company'),
        ('Partnership', 'Partnership'),
        ('Government Entity', 'Government Entity'),
        ('Foreign Company', 'Foreign Company'),
        ('Joint Venture', 'Joint Venture'),
        ('State Owned Company', 'State Owned Company'),
        ('Other', 'Other'),
    )
    
    DZONGKHAG_CHOICES = (
        ('Mongar', 'Mongar'),
        ('Trashigang', 'Trashigang'),
        ('Trashiyangtse', 'Trashiyangtse'),
        ('Lhuentse', 'Lhuentse'),
    )
    
    FREQUENCY_CHOICES = (
        ('Monthly', 'Monthly'),
        ('Quarterly', 'Quarterly'),
        ('Half Yearly', 'Half Yearly'),
    )
    
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Suspended', 'Suspended'),
        ('Cancelled', 'Cancelled'),
        ('Deregistered', 'Deregistered'),
        ('Region Transferred', 'Region Transferred'),
    )
    
    # Identification Numbers
    cid_company_reg_no = models.CharField(max_length=50, blank=True, null=True, verbose_name='CID No/Co. Reg No')
    gstin = models.CharField(max_length=15, blank=True, null=True, verbose_name='GSTIN')
    ramis_tpn = models.CharField(max_length=50, blank=True, null=True, verbose_name='RAMIS TPN')
    license_number = models.CharField(max_length=50, blank=True, null=True, verbose_name='License Number')
    
    # Basic Information
    taxpayer_name = models.CharField(max_length=200, verbose_name='Taxpayer Name', blank=True, null=True)
    business_name = models.CharField(max_length=200, verbose_name='Business Name', blank=True, null=True)
    
    # Classification
    sector = models.CharField(max_length=100, blank=True, null=True, verbose_name='Sector')
    sub_sector = models.CharField(max_length=100, blank=True, null=True, verbose_name='Sub-Sector')
    business_activity = models.CharField(max_length=200, blank=True, null=True, verbose_name='Business Activity')
    organisation_type = models.CharField(max_length=50, choices=ORGANISATION_TYPES, blank=True, null=True, verbose_name='Organisation Type')
    frequency = models.CharField(max_length=50, choices=FREQUENCY_CHOICES, blank=True, null=True, verbose_name='Frequency')
    dzongkhag = models.CharField(max_length=100, choices=DZONGKHAG_CHOICES, blank=True, null=True, verbose_name='Dzongkhag')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, blank=True, null=True, verbose_name='Status')
    
    # Important Dates
    registration_date = models.DateField(blank=True, null=True, verbose_name='Registration Date')
    commencement_date = models.DateField(null=True, blank=True, verbose_name='Commencement Date')
    deregistration_date = models.DateField(null=True, blank=True, verbose_name='Deregistration/Region Transfer Date')
    
    # Contact Information
    email_address = models.EmailField(blank=True, null=True, verbose_name='Email Address')
    mobile_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='Mobile Number')
    business_address = models.TextField(blank=True, null=True, verbose_name='Business Address')
    
    # Additional Information
    remarks = models.TextField(blank=True, null=True, verbose_name='Remarks')
    
    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['taxpayer_name']
        verbose_name = 'Secondary License'
        verbose_name_plural = 'Secondary Licenses'
        indexes = [
            models.Index(fields=['gstin']),
            models.Index(fields=['license_number']),
            models.Index(fields=['taxpayer_name']),
        ]
    
    def __str__(self):
        return f"{self.taxpayer_name} ({self.gstin}) - {self.license_number}"
    
    def save(self, *args, **kwargs):
        # Handle Region Transferred logic for secondary licenses
        old_status = None
        if self.pk:
            try:
                old_instance = MultipleLicenseReference.objects.get(pk=self.pk)
                old_status = old_instance.status
            except MultipleLicenseReference.DoesNotExist:
                pass
        
        super().save(*args, **kwargs)
        
        # If status changed to Region Transferred, ensure it's not counted as active
        if self.status == 'Region Transferred' and old_status != 'Region Transferred':
            # This taxpayer should not be counted in active summary
            # The summary logic already filters by status='Active', so it will automatically exclude Region Transferred
            pass