from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Extended User model for GST Compliance System
    """
    USER_ROLES = (
        ('administrator', 'Administrator'),
        ('section_head', 'Section Head'),
        ('audit_refund', 'Audit and Refund'),
        ('registration_enquiry', 'Registration Taxpayer Enquiry'),
        ('compliance', 'Compliance'),
    )
    
    email = models.EmailField(unique=True)  # Make email unique
    role = models.CharField(max_length=50, choices=USER_ROLES, default='compliance')
    phone = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)
    employee_id = models.CharField(max_length=20, unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_password_change = models.DateTimeField(null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    def is_administrator(self):
        return self.role == 'administrator'
    
    def is_admin(self):
        """Backward compatibility method"""
        return self.is_administrator()
    
    def is_section_head(self):
        return self.role == 'section_head'
    
    def is_audit_refund(self):
        return self.role == 'audit_refund'
    
    def is_registration_enquiry(self):
        return self.role == 'registration_enquiry'
    
    def is_compliance(self):
        return self.role == 'compliance'
    
    def can_edit_taxpayers(self):
        """Can edit taxpayer data"""
        return self.role in ['administrator', 'registration_enquiry', 'compliance']
    
    def can_edit_returns(self):
        """Can edit GST returns"""
        return self.role in ['administrator', 'compliance']
    
    def can_edit_refunds(self):
        """Can edit refund data"""
        return self.role in ['administrator', 'audit_refund']
    
    def can_view_all(self):
        """Can view all data"""
        return self.role in ['administrator', 'section_head', 'audit_refund']
    
    def can_manage_users(self):
        """Can manage users"""
        return self.role in ['administrator', 'section_head']


class AuditLog(models.Model):
    """
    Track user activities for security and auditing
    """
    ACTION_TYPES = (
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('view', 'View'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('export', 'Export'),
        ('import', 'Import'),
    )
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='audit_logs')
    action = models.CharField(max_length=20, choices=ACTION_TYPES)
    model_name = models.CharField(max_length=100, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'
    
    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp}"


class SystemSettings(models.Model):
    """
    System-wide configuration settings - simplified with specific fields
    """
    # General Settings
    system_name = models.CharField(max_length=200, default='GST Compliance System', verbose_name='System Name')
    organization_name = models.CharField(max_length=200, default='Revenue and Customs Division', verbose_name='Organization Name')
    
    # Contact Information
    contact_email = models.EmailField(default='info@gst.gov.bt', verbose_name='Contact Email')
    contact_phone = models.CharField(max_length=20, default='+975-2-322525', verbose_name='Contact Phone')
    contact_address = models.TextField(default='Thimphu, Bhutan', verbose_name='Contact Address')
    
    # Notification Settings
    send_email_notifications = models.BooleanField(default=True, verbose_name='Send Email Notifications')
    email_smtp_server = models.CharField(max_length=200, blank=True, verbose_name='SMTP Server')
    email_smtp_port = models.IntegerField(default=587, blank=True, null=True, verbose_name='SMTP Port')
    
    # Report Settings
    report_logo_url = models.URLField(blank=True, verbose_name='Report Logo URL')
    report_footer_text = models.CharField(max_length=500, default='GST Compliance Report', verbose_name='Report Footer Text')
    
    # System Information
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Last Updated By')
    
    class Meta:
        verbose_name = 'System Setting'
        verbose_name_plural = 'System Settings'
    
    def __str__(self):
        return f"{self.system_name} - {self.organization_name}"