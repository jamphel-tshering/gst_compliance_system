from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Extended User model for GST Compliance System
    """
    USER_ROLES = (
        ('admin', 'Administrator'),
        ('auditor', 'Auditor'),
        ('viewer', 'Viewer'),
        ('data_entry', 'Data Entry Operator'),
    )
    
    email = models.EmailField(unique=True)  # Make email unique
    role = models.CharField(max_length=20, choices=USER_ROLES, default='viewer')
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
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_auditor(self):
        return self.role in ['admin', 'auditor']
    
    def can_edit_data(self):
        return self.role in ['admin', 'data_entry']
    
    def can_view_all(self):
        return self.role in ['admin', 'auditor', 'viewer']


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
    System-wide configuration settings
    """
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    description = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = 'System Setting'
        verbose_name_plural = 'System Settings'
    
    def __str__(self):
        return f"{self.key}: {self.value}"