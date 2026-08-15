from django.db import models
from taxpayers.models import TaxpayerMaster
from core.models import User

class GSTReturn(models.Model):
    """
    GST Return Model - Exact field specifications
    """
    FREQUENCY_CHOICES = (
        ('Monthly', 'Monthly'),
        ('Quarterly', 'Quarterly'),
        ('Annual', 'Annual'),
    )
    
    ORGANISATION_TYPES = (
        ('Sole Proprietorship', 'Sole Proprietorship'),
        ('Private Company', 'Private Company'),
        ('Public Company', 'Public Company'),
        ('Partnership', 'Partnership'),
        ('State Owned Company', 'State Owned Company'),
        ('Joint Venture', 'Joint Venture'),
        ('Foreign Company', 'Foreign Company'),
    )
    
    DZONGKHAG_CHOICES = (
        ('Mongar', 'Mongar'),
        ('Trashigang', 'Trashigang'),
        ('Trashiyangtse', 'Trashiyangtse'),
        ('Lhuentse', 'Lhuentse'),
    )
    
    FILING_STATUS_CHOICES = (
        ('Filed', 'Filed'),
        ('Overdue / Non-Filer', 'Overdue / Non-Filer'),
        ('Late Filer', 'Late Filer'),
        ('Pending', 'Pending'),
    )
    
    PAYMENT_STATUS_CHOICES = (
        ('Paid', 'Paid'),
        ('Not paid', 'Not paid'),
        ('Partial Payment', 'Partial Payment'),
        ('Pending', 'Pending'),
    )
    
    COMPLIANCE_STATUS_CHOICES = (
        ('Compliant', 'Compliant'),
        ('Late Filer', 'Late Filer'),
        ('Non-Filer', 'Non-Filer'),
        ('Pending', 'Pending'),
        ('Inactive Taxpayer', 'Inactive Taxpayer'),
        ('Unknown Taxpayer', 'Unknown Taxpayer'),
    )
    

    
    TAX_PERIOD_CHOICES = (
        ('Jan-2026', 'Jan-2026'),
        ('Feb-2026', 'Feb-2026'),
        ('Mar-2026', 'Mar-2026'),
        ('Apr-2026', 'Apr-2026'),
        ('May-2026', 'May-2026'),
        ('Jun-2026', 'Jun-2026'),
        ('Jul-2026', 'Jul-2026'),
        ('Aug-2026', 'Aug-2026'),
        ('Sep-2026', 'Sep-2026'),
        ('Oct-2026', 'Oct-2026'),
        ('Nov-2026', 'Nov-2026'),
        ('Dec-2026', 'Dec-2026'),
    )
    
    # Period Information
    tax_period = models.CharField(max_length=20, verbose_name='Tax Period')
    return_due_date = models.DateField(null=True, blank=True, verbose_name='Return Due Date')
    return_filing_date = models.DateField(null=True, blank=True, verbose_name='Return Filing Date')
    filing_delay_days = models.IntegerField(default=0, null=True, blank=True, verbose_name='Filing Delay (Days)')
    
    # Taxpayer Information
    gstin = models.CharField(max_length=15, verbose_name='GSTIN')
    taxpayer_name = models.CharField(max_length=200, null=True, blank=True, verbose_name='Taxpayer Name')
    dzongkhag = models.CharField(max_length=100, choices=DZONGKHAG_CHOICES, null=True, blank=True, verbose_name='Dzongkhag')
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
    payment_status = models.CharField(max_length=30, choices=PAYMENT_STATUS_CHOICES, null=True, blank=True, verbose_name='Payment Status')
    compliance_status = models.CharField(max_length=30, choices=COMPLIANCE_STATUS_CHOICES, null=True, blank=True, verbose_name='Compliance Status')
    
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
    
    def save(self, *args, **kwargs):
        """Override save to auto-calculate certain fields"""
        from decimal import Decimal
        from datetime import datetime, date, timedelta
        
        # Auto-calculate return_due_date from tax_period if not set
        if self.tax_period and not self.return_due_date:
            try:
                from datetime import datetime, date, timedelta
                import calendar
                
                # Parse tax_period from Jan-2026 format
                tax_date = datetime.strptime(str(self.tax_period), '%b-%Y').date()
                
                # Due date = End of tax period + 30 days
                # For monthly, end of month is last day of the month
                if self.frequency == 'Monthly':
                    # Get last day of the month
                    last_day = calendar.monthrange(tax_date.year, tax_date.month)[1]
                    end_of_month = date(tax_date.year, tax_date.month, last_day)
                elif self.frequency == 'Quarterly':
                    # For quarterly, end is 3 months from start
                    end_date = tax_date + timedelta(days=90)
                    last_day = calendar.monthrange(end_date.year, end_date.month)[1]
                    end_of_month = date(end_date.year, end_date.month, last_day)
                else:
                    end_of_month = tax_date
                
                self.return_due_date = end_of_month + timedelta(days=30)
            except:
                pass
        
        # Auto-calculate declared_import_gst
        if self.declared_import_value:
            import_value = Decimal(str(self.declared_import_value)) if not isinstance(self.declared_import_value, Decimal) else self.declared_import_value
            self.declared_import_gst = round(import_value * Decimal('0.05'), 2)
        
        # Auto-calculate domestic_purchase_itc_claimed
        if self.declared_domestic_purchase:
            domestic_purchase = Decimal(str(self.declared_domestic_purchase)) if not isinstance(self.declared_domestic_purchase, Decimal) else self.declared_domestic_purchase
            self.domestic_purchase_itc_claimed = round(domestic_purchase * Decimal('0.05'), 2)
        
        # Auto-calculate declared_output_gst
        if self.declared_sales:
            sales = Decimal(str(self.declared_sales)) if not isinstance(self.declared_sales, Decimal) else self.declared_sales
            self.declared_output_gst = round(sales * Decimal('0.05'), 2)
        
        # Auto-calculate filing_delay_days
        if self.return_due_date and self.return_filing_date:
            due_date = self.return_due_date
            filing_date = self.return_filing_date
            # Ensure both are date objects (not datetime)
            if hasattr(due_date, 'date'):
                due_date = due_date.date()
            if hasattr(filing_date, 'date'):
                filing_date = filing_date.date()
            delay = (filing_date - due_date).days
            self.filing_delay_days = max(0, delay)
        
        # Auto-calculate filing_status
        if self.return_due_date:
            today = date.today()
            # Ensure return_due_date is a date object
            due_date = self.return_due_date
            if hasattr(due_date, 'date'):
                due_date = due_date.date()
            
            if not self.return_filing_date:
                # No filing date
                if today <= due_date:
                    self.filing_status = 'Due'
                else:
                    self.filing_status = 'Overdue / Non-Filer'
            else:
                # Has filing date - ensure it's a date object
                filing_date = self.return_filing_date
                if hasattr(filing_date, 'date'):
                    filing_date = filing_date.date()
                
                if filing_date <= due_date:
                    self.filing_status = 'Filed On Time'
                else:
                    self.filing_status = 'Late Filer'
        
        # Auto-calculate compliance_status based on Taxpayer Master and filing status
        try:
            taxpayer = TaxpayerMaster.objects.get(gstin=self.gstin)
            if taxpayer.status != 'Active':
                self.compliance_status = 'Inactive Taxpayer'
            elif self.filing_status == 'Overdue / Non-Filer':
                self.compliance_status = 'Non-Filer'
            elif self.filing_status == 'Late Filer':
                self.compliance_status = 'Late Filer'
            elif self.filing_status == 'Filed On Time':
                self.compliance_status = 'Compliant'
            elif self.filing_status == 'Due':
                self.compliance_status = 'Pending'
            else:
                self.compliance_status = 'Compliant'
        except TaxpayerMaster.DoesNotExist:
            self.compliance_status = 'Unknown Taxpayer'
        
        super().save(*args, **kwargs)
    
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
        ('', '---------'),
        ('Sole Proprietorship', 'Sole Proprietorship'),
        ('Private Company', 'Private Company'),
        ('Public Company', 'Public Company'),
        ('Partnership', 'Partnership'),
        ('State Owned Company', 'State Owned Company'),
        ('Joint Venture', 'Joint Venture'),
        ('Foreign Company', 'Foreign Company'),
    )
    
    DZONGKHAG_CHOICES = (
        ('', '---------'),
        ('Mongar', 'Mongar'),
        ('Trashigang', 'Trashigang'),
        ('Trashiyangtse', 'Trashiyangtse'),
        ('Lhuentse', 'Lhuentse'),
    )
    
    FILING_STATUS_CHOICES = (
        ('', '---------'),
        ('Filed On Time', 'Filed On Time'),
        ('Late Filer', 'Late Filer'),
        ('Due', 'Due'),
        ('Overdue / Non-Filer', 'Overdue / Non-Filer'),
        ('Extension', 'Extension'),
    )
    
    PAYMENT_STATUS_CHOICES = (
        ('', '---------'),
        ('Paid', 'Paid'),
        ('Credit', 'Credit'),
        ('Pending', 'Pending'),
        ('Partial Payment', 'Partial Payment'),
    )
    
    FILING_STATUS_CHOICES = (
        ('Filed On Time', 'Filed On Time'),
        ('Late Filer', 'Late Filer'),
        ('Due', 'Due'),
        ('Overdue / Non-Filer', 'Overdue / Non-Filer'),
        ('Extension', 'Extension'),
    )
    
    COMPLIANCE_STATUS_CHOICES = (
        ('Compliant', 'Compliant'),
        ('Late Filer', 'Late Filer'),
        ('Non-Filer', 'Non-Filer'),
        ('Pending', 'Pending'),
        ('Inactive Taxpayer', 'Inactive Taxpayer'),
        ('Unknown Taxpayer', 'Unknown Taxpayer'),
    )
    
    # Taxpayer Information
    gstin = models.CharField(max_length=15, verbose_name='GSTIN')
    taxpayer_name = models.CharField(max_length=200, verbose_name='Taxpayer Name')
    organisation_type = models.CharField(max_length=30, choices=ORGANISATION_TYPES, verbose_name='Organisation Type')
    dzongkhag = models.CharField(max_length=100, choices=DZONGKHAG_CHOICES, null=True, blank=True, verbose_name='Dzongkhag')
    
    # Return Period
    return_period = models.CharField(max_length=20, verbose_name='Return Period')
    
    # Status Information
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending', verbose_name='Payment Status')
    filing_status = models.CharField(max_length=20, choices=FILING_STATUS_CHOICES, default='Overdue / Non-Filer', verbose_name='Filing Status')
    compliance_status = models.CharField(max_length=30, choices=COMPLIANCE_STATUS_CHOICES, null=True, blank=True, verbose_name='Compliance Status')
    
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
            models.Index(fields=['compliance_status']),
        ]
        unique_together = ['gstin', 'return_period']
    
    def __str__(self):
        return f"{self.taxpayer_name} - {self.return_period} ({self.filing_status})"
    
    def save(self, *args, **kwargs):
        """Override save to auto-calculate compliance status"""
        try:
            taxpayer = TaxpayerMaster.objects.get(gstin=self.gstin)
            if taxpayer.status != 'Active':
                self.compliance_status = 'Inactive Taxpayer'
            elif self.filing_status == 'Overdue / Non-Filer':
                self.compliance_status = 'Non-Filer'
            elif self.filing_status == 'Late Filer':
                self.compliance_status = 'Late Filer'
            elif self.filing_status == 'Filed On Time':
                self.compliance_status = 'Compliant'
            elif self.filing_status == 'Due':
                self.compliance_status = 'Pending'
            else:
                self.compliance_status = 'Compliant'
        except TaxpayerMaster.DoesNotExist:
            self.compliance_status = 'Unknown Taxpayer'
        
        super().save(*args, **kwargs)