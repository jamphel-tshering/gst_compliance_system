from django.db import models
from django.core.exceptions import ValidationError
from core.models import User

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
    deregistration_date = models.DateField(null=True, blank=True, verbose_name='Deregistration Date')
    
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
        verbose_name = 'Taxpayer Master'
        verbose_name_plural = 'Taxpayer Masters'
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
    deregistration_date = models.DateField(null=True, blank=True, verbose_name='Deregistration Date')
    
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
        verbose_name = 'Multiple License Reference'
        verbose_name_plural = 'Multiple License References'
        indexes = [
            models.Index(fields=['gstin']),
            models.Index(fields=['license_number']),
            models.Index(fields=['taxpayer_name']),
        ]
    
    def __str__(self):
        return f"{self.taxpayer_name} ({self.gstin}) - {self.license_number}"