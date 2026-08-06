from django.db import models
from taxpayers.models import TaxpayerMaster
from core.models import User

class GSTReturn(models.Model):
    """
    GST Return Model - Exact field specifications
    """
    FREQUENCY_CHOICES = (
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annual', 'Annual'),
    )
    
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
    
    FILING_STATUS_CHOICES = (
        ('filed', 'Filed'),
        ('Filed', 'Filed'),
        ('not_filed', 'Not Filed'),
        ('Not Filed', 'Not Filed'),
        ('extension', 'Extention'),
        ('Extention', 'Extention'),
        ('Extension', 'Extension'),
        ('due', 'Due'),
        ('over_due', 'Over Due'),
    )
    
    PAYMENT_STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('Paid', 'Paid'),
        ('not_paid', 'Not paid'),
        ('Not paid', 'Not paid'),
        ('credit', 'Credit'),
        ('zero_return', 'Zero Return'),
        ('reconciled', 'Reconciled Output Input'),
    )
    
    COMPLIANCE_STATUS_CHOICES = (
        ('compliant', 'Compliant'),
        ('Compliant', 'Compliant'),
        ('late_filer', 'Late Filer'),
        ('late_payment', 'Late payment'),
        ('non_filer', 'Non-Filer'),
        ('return_amended', 'Return Amended'),
        ('under_review', 'Under Review'),
    )
    
    # Period Information
    tax_period = models.CharField(max_length=20, verbose_name='Tax Period (e.g., Jan-2026)')
    return_due_date = models.DateField(null=True, blank=True, verbose_name='Return Due Date')
    return_filing_date = models.DateField(null=True, blank=True, verbose_name='Return Filing Date')
    filing_delay_days = models.IntegerField(default=0, verbose_name='Filing Delay (Days)')
    
    # Taxpayer Information
    gstin = models.CharField(max_length=15, verbose_name='GSTIN')
    taxpayer_name = models.CharField(max_length=200, null=True, blank=True, verbose_name='Taxpayer Name')
    dzongkhag = models.CharField(max_length=100, null=True, blank=True, verbose_name='Dzongkhag')
    organisation_type = models.CharField(max_length=30, choices=ORGANISATION_TYPES, null=True, blank=True, verbose_name='Organisation Type')
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, null=True, blank=True, verbose_name='Frequency')
    
    # Financial Details - Declared
    declared_sales = models.DecimalField(max_digits=15, decimal_places=2, default=0, null=True, blank=True, verbose_name='Declared Sales')
    declared_domestic_purchase = models.DecimalField(max_digits=15, decimal_places=2, default=0, null=True, blank=True, verbose_name='Declared Domestic Purchase/Taxable Expenses')
    declared_import_value = models.DecimalField(max_digits=15, decimal_places=2, default=0, null=True, blank=True, verbose_name='Declared Import Value')
    ecms_import_value = models.DecimalField(max_digits=15, decimal_places=2, default=0, null=True, blank=True, verbose_name='eCMS Import Value')
    declared_import_gst = models.DecimalField(max_digits=15, decimal_places=2, default=0, null=True, blank=True, verbose_name='Declared Import GST')
    
    # ITC Details
    domestic_purchase_itc_claimed = models.DecimalField(max_digits=15, decimal_places=2, default=0, null=True, blank=True, verbose_name='Domestic Purchase ITC Claimed')
    total_itc_claimed = models.DecimalField(max_digits=15, decimal_places=2, default=0, null=True, blank=True, verbose_name='Total ITC Claimed')
    
    # Output GST
    declared_output_gst = models.DecimalField(max_digits=15, decimal_places=2, default=0, null=True, blank=True, verbose_name='Declared Output GST')
    
    # GST Payable/Refundable
    gst_payable_refundable = models.DecimalField(max_digits=15, decimal_places=2, default=0, null=True, blank=True, verbose_name='GST Payable / Refundable (GST Return)')
    actual_gst_payment_received = models.DecimalField(max_digits=15, decimal_places=2, default=0, null=True, blank=True, verbose_name='Actual GST Payment Received')
    bank_deposits = models.DecimalField(max_digits=15, decimal_places=2, default=0, null=True, blank=True, verbose_name='Bank Deposits')
    
    # Status Information
    filing_status = models.CharField(max_length=20, choices=FILING_STATUS_CHOICES, null=True, blank=True, verbose_name='Filing Status')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, null=True, blank=True, verbose_name='Payment Status')
    compliance_status = models.CharField(max_length=20, choices=COMPLIANCE_STATUS_CHOICES, null=True, blank=True, verbose_name='Compliance Status')
    
    # Additional Information
    remarks = models.TextField(blank=True, null=True, verbose_name='Remarks')
    
    # System Fields
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_returns')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_returns')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-tax_period', 'taxpayer_name']
        verbose_name = 'GST Return'
        verbose_name_plural = 'GST Returns'
        indexes = [
            models.Index(fields=['gstin', 'tax_period']),
            models.Index(fields=['tax_period']),
            models.Index(fields=['filing_status']),
            models.Index(fields=['compliance_status']),
        ]
        unique_together = []
    
    def __str__(self):
        return f"{self.taxpayer_name} - {self.tax_period}"
    
    @property
    def is_credit_position(self):
        return self.gst_payable_refundable < 0
    
    @property
    def import_sales_ratio(self):
        if self.declared_sales > 0:
            return (self.declared_import_value / self.declared_sales) * 100
        return 999 if self.declared_import_value > 0 else 0
    
    @property
    def purchase_sales_ratio(self):
        if self.declared_sales > 0:
            return (self.declared_domestic_purchase / self.declared_sales) * 100
        return 999 if self.declared_domestic_purchase > 0 else 0


class NotFile(models.Model):
    """
    Not File Model - For taxpayers who haven't filed returns
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
    
    FILING_STATUS_CHOICES = (
        ('not_filed', 'Not Filed'),
        ('filed_late', 'Filed Late'),
        ('pending', 'Pending'),
    )
    
    PAYMENT_STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('credit', 'Credit'),
        ('pending', 'Pending'),
        ('partial', 'Partial Payment'),
    )
    
    # Taxpayer Information
    gstin = models.CharField(max_length=15, verbose_name='GSTIN')
    taxpayer_name = models.CharField(max_length=200, verbose_name='Taxpayer Name')
    organisation_type = models.CharField(max_length=30, choices=ORGANISATION_TYPES, verbose_name='Organisation Type')
    
    # Return Period
    return_period = models.CharField(max_length=20, verbose_name='Return Period')
    
    # Status Information
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending', verbose_name='Payment Status')
    filing_status = models.CharField(max_length=20, choices=FILING_STATUS_CHOICES, default='not_filed', verbose_name='Filing Status')
    
    # System Fields
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_notfiles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-return_period', 'taxpayer_name']
        verbose_name = 'Not File'
        verbose_name_plural = 'Not Files'
        indexes = [
            models.Index(fields=['gstin', 'return_period']),
            models.Index(fields=['return_period']),
            models.Index(fields=['filing_status']),
        ]
        unique_together = ['gstin', 'return_period']
    
    def __str__(self):
        return f"{self.taxpayer_name} - {self.return_period} ({self.filing_status})"