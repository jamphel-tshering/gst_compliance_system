from django.db import models
from taxpayers.models import TaxpayerMaster
from returns.models import GSTReturn
from core.models import User


class ComplianceMonitoring(models.Model):
    """
    Simple Compliance Monitoring Model - Tracks taxpayer compliance
    """
    TRUST_LEVEL_CHOICES = (
        ('highly_trustworthy', 'Highly Trustworthy'),
        ('trustworthy', 'Trustworthy'),
        ('moderate', 'Moderate'),
        ('low_trust', 'Low Trust'),
        ('untrustworthy', 'Untrustworthy'),
    )
    
    COMPLIANCE_STATUS_CHOICES = (
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('critical', 'Critical'),
    )
    
    # Link to Taxpayer
    taxpayer = models.ForeignKey(TaxpayerMaster, on_delete=models.SET_NULL, null=True, blank=True, related_name='compliance_records')
    gst_return = models.ForeignKey(GSTReturn, on_delete=models.SET_NULL, null=True, blank=True, related_name='compliance_records')
    
    # Assessment Period (Date Range)
    assessment_from = models.DateField(null=True, blank=True, verbose_name='Assessment From Date')
    assessment_to = models.DateField(null=True, blank=True, verbose_name='Assessment To Date')
    assessment_date = models.DateField(auto_now_add=True, verbose_name='Assessment Date')
    
    # Compliance Metrics (Simple yes/no or scores)
    filing_on_time = models.BooleanField(default=False, verbose_name='Filing On Time')
    payment_on_time = models.BooleanField(default=False, verbose_name='Payment On Time')
    notification_compliance = models.BooleanField(default=False, verbose_name='Notification Compliance')
    
    # Trustworthiness
    trust_level = models.CharField(max_length=30, choices=TRUST_LEVEL_CHOICES, default='moderate', verbose_name='Trust Level')
    trust_score = models.IntegerField(default=0, verbose_name='Trust Score (0-100)')
    
    # Overall Compliance Status
    compliance_status = models.CharField(max_length=20, choices=COMPLIANCE_STATUS_CHOICES, default='fair', verbose_name='Compliance Status')
    compliance_score = models.IntegerField(default=0, verbose_name='Compliance Score (0-100)')
    
    # Notes
    compliance_notes = models.TextField(blank=True, verbose_name='Compliance Notes')
    
    # System Fields
    assessed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='compliance_assessments', verbose_name='Assessed By')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-assessment_date', 'taxpayer']
        verbose_name = 'Compliance Monitoring'
        verbose_name_plural = 'Compliance Monitoring'
        indexes = [
            models.Index(fields=['taxpayer', 'assessment_from']),
            models.Index(fields=['compliance_status']),
            models.Index(fields=['trust_level']),
            models.Index(fields=['assessment_date']),
        ]
        unique_together = []
    
    def __str__(self):
        if self.taxpayer:
            return f"{self.taxpayer.taxpayer_name} - {self.assessment_from} to {self.assessment_to} ({self.compliance_status})"
        return f"Unknown Taxpayer - {self.assessment_from} to {self.assessment_to} ({self.compliance_status})"
    
    @property
    def assessment_period(self):
        """For backward compatibility"""
        return f"{self.assessment_from.strftime('%b-%Y')} to {self.assessment_to.strftime('%b-%Y')}"
    
    def calculate_compliance_score(self):
        """Calculate compliance score based on metrics"""
        score = 0  # Base score - no data = 0 score
        
        if self.filing_on_time:
            score += 25
        if self.payment_on_time:
            score += 25
        if self.notification_compliance:
            score += 20
        
        # Add trust score factor (weighted)
        score = (score + self.trust_score) // 2
        
        return min(100, max(0, score))
    
    def save(self, *args, **kwargs):
        """Auto-calculate compliance score before saving"""
        self.compliance_score = self.calculate_compliance_score()
        
        # Auto-set compliance status based on score
        if self.compliance_score >= 80:
            self.compliance_status = 'excellent'
        elif self.compliance_score >= 60:
            self.compliance_status = 'good'
        elif self.compliance_score >= 40:
            self.compliance_status = 'fair'
        elif self.compliance_score >= 20:
            self.compliance_status = 'poor'
        else:
            self.compliance_status = 'critical'
        
        super().save(*args, **kwargs)
