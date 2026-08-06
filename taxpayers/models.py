from django.db import models
from django.core.exceptions import ValidationError
from core.models import User

class TaxpayerMaster(models.Model):
    """
    Taxpayer Master Model - Main taxpayer record (one per GSTIN)
    """
    ORGANISATION_TYPES = (
        ('sole_proprietorship', 'Sole Proprietorship'),
        ('private_company', 'Private Company'),
        ('public_company', 'Public Company'),
        ('partnership', 'Partnership'),
        ('llp', 'Limited Liability Partnership'),
        ('trust', 'Trust'),
        ('government', 'Government Entity'),
        ('foreign_company', 'Foreign Company'),
        ('joint_venture', 'Joint Venture'),
        ('state_owned_company', 'State Owned Company'),
        ('other', 'Other'),
    )
    
    FREQUENCY_CHOICES = (
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annual', 'Annual'),
    )
    
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
        ('cancelled', 'Cancelled'),
        ('deregistered', 'Deregistered'),
    )
    
    # Identification Numbers
    cid_company_reg_no = models.CharField(max_length=50, blank=True, null=True, verbose_name='CID No/Co. Reg No')
    gstin = models.CharField(max_length=15, verbose_name='GSTIN')  # Keep non-unique for now
    ramis_tpn = models.CharField(max_length=50, blank=True, null=True, verbose_name='RAMIS TPN')
    is_primary_license = models.BooleanField(default=True, verbose_name='Is Primary License')  # Distinguish main vs additional licenses
    primary_taxpayer = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='additional_licenses', verbose_name='Primary Taxpayer')  # Link additional licenses to primary
    
    # Basic Information
    taxpayer_name = models.CharField(max_length=200, verbose_name='Taxpayer Name')
    business_name = models.CharField(max_length=200, verbose_name='Business Name', blank=True)
    
    # Classification
    sector = models.CharField(max_length=100, blank=True, null=True, verbose_name='Sector')
    sub_sector = models.CharField(max_length=100, blank=True, null=True, verbose_name='Sub-Sector')
    business_activity = models.CharField(max_length=200, blank=True, null=True, verbose_name='Business Activity')
    organisation_type = models.CharField(max_length=50, choices=ORGANISATION_TYPES, blank=True, null=True, verbose_name='Organisation Type')
    frequency = models.CharField(max_length=50, choices=FREQUENCY_CHOICES, blank=True, null=True, verbose_name='Frequency')
    dzongkhag = models.CharField(max_length=100, blank=True, null=True, verbose_name='Dzongkhag')
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
        """Ensure only one record per GSTIN can be marked as primary"""
        if self.is_primary_license:
            # Check if there's another primary license for the same GSTIN
            other_primary = TaxpayerMaster.objects.filter(
                gstin=self.gstin,
                is_primary_license=True
            ).exclude(pk=self.pk).exists()
            
            if other_primary:
                raise ValidationError({
                    'is_primary_license': 'Only one record per GSTIN can be marked as primary license.'
                })
        
        # If this is an additional license, it must have a primary taxpayer
        if not self.is_primary_license and not self.primary_taxpayer:
            # Try to find primary taxpayer with same GSTIN
            primary = TaxpayerMaster.objects.filter(
                gstin=self.gstin,
                is_primary_license=True
            ).first()
            
            if primary:
                self.primary_taxpayer = primary
            else:
                raise ValidationError({
                    'primary_taxpayer': 'Additional licenses must be linked to a primary taxpayer with the same GSTIN.'
                })
    
    @property
    def gst_returns(self):
        return self.returns.all()
    
    @property
    def refund_applications(self):
        return self.refunds.all()
    
    def get_business_licenses_count(self):
        return self.business_licenses.count()


class AdditionalLicense(TaxpayerMaster):
    """Proxy model for additional licenses - separate admin section"""
    class Meta:
        proxy = True
        verbose_name = 'Additional License'
        verbose_name_plural = 'Additional Licenses'