from django.db import models
from taxpayers.models import TaxpayerMaster
from core.models import User

class RefundRegister(models.Model):
    """
    Refund Register Model - Exact field specifications
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
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_refunds')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_refunds')
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