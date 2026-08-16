from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Extended User model for GST Compliance System with granular access control
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
    employee_id = models.CharField(max_length=20, unique=True, null=True, blank=True)  # Allow NULL for unique constraint
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_password_change = models.DateTimeField(null=True, blank=True)
    
    # GRANULAR ACCESS CONTROL FIELDS - All optional for individual access grant
    # Taxpayer Module Access
    can_view_taxpayers = models.BooleanField(default=False, verbose_name='View Taxpayers')
    can_add_taxpayers = models.BooleanField(default=False, verbose_name='Add Taxpayers')
    can_edit_taxpayers = models.BooleanField(default=False, verbose_name='Edit Taxpayers')
    can_delete_taxpayers = models.BooleanField(default=False, verbose_name='Delete Taxpayers')
    
    # GST Returns Module Access
    can_view_returns = models.BooleanField(default=False, verbose_name='View GST Returns')
    can_add_returns = models.BooleanField(default=False, verbose_name='Add GST Returns')
    can_edit_returns = models.BooleanField(default=False, verbose_name='Edit GST Returns')
    can_delete_returns = models.BooleanField(default=False, verbose_name='Delete GST Returns')
    
    # Refunds Module Access
    can_view_refunds = models.BooleanField(default=False, verbose_name='View Refunds')
    can_add_refunds = models.BooleanField(default=False, verbose_name='Add Refunds')
    can_edit_refunds = models.BooleanField(default=False, verbose_name='Edit Refunds')
    can_delete_refunds = models.BooleanField(default=False, verbose_name='Delete Refunds')
    
    # Compliance Module Access
    can_view_compliance = models.BooleanField(default=False, verbose_name='View Compliance')
    can_add_compliance = models.BooleanField(default=False, verbose_name='Add Compliance')
    can_edit_compliance = models.BooleanField(default=False, verbose_name='Edit Compliance')
    can_delete_compliance = models.BooleanField(default=False, verbose_name='Delete Compliance')
    
    # Risk Assessment Module Access
    can_view_risk_assessment = models.BooleanField(default=False, verbose_name='View Risk Assessment')
    can_run_risk_assessment = models.BooleanField(default=False, verbose_name='Run Risk Assessment')
    can_edit_risk_assessment = models.BooleanField(default=False, verbose_name='Edit Risk Assessment')
    can_approve_risk_assessment = models.BooleanField(default=False, verbose_name='Approve Risk Assessment')
    
    # Enforcement & Recovery Module Access
    can_view_enforcement = models.BooleanField(default=False, verbose_name='View Enforcement')
    can_add_enforcement = models.BooleanField(default=False, verbose_name='Add Enforcement')
    can_edit_enforcement = models.BooleanField(default=False, verbose_name='Edit Enforcement')
    can_delete_enforcement = models.BooleanField(default=False, verbose_name='Delete Enforcement')
    
    # Audit Module Access
    can_view_audit = models.BooleanField(default=False, verbose_name='View Audit')
    can_create_audit = models.BooleanField(default=False, verbose_name='Create Audit')
    can_edit_audit = models.BooleanField(default=False, verbose_name='Edit Audit')
    can_approve_audit = models.BooleanField(default=False, verbose_name='Approve Audit')
    
    # Reports Module Access
    can_view_reports = models.BooleanField(default=False, verbose_name='View Reports')
    can_generate_reports = models.BooleanField(default=False, verbose_name='Generate Reports')
    can_export_reports = models.BooleanField(default=False, verbose_name='Export Reports')
    
    # User Management Access
    can_view_users = models.BooleanField(default=False, verbose_name='View Users')
    can_add_users = models.BooleanField(default=False, verbose_name='Add Users')
    can_edit_users = models.BooleanField(default=False, verbose_name='Edit Users')
    can_delete_users = models.BooleanField(default=False, verbose_name='Delete Users')
    can_manage_permissions = models.BooleanField(default=False, verbose_name='Manage Permissions')
    
    # System Settings Access
    can_view_settings = models.BooleanField(default=False, verbose_name='View Settings')
    can_edit_settings = models.BooleanField(default=False, verbose_name='Edit Settings')
    
    # Import/Export Access
    can_import_data = models.BooleanField(default=False, verbose_name='Import Data')
    can_export_data = models.BooleanField(default=False, verbose_name='Export Data')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.get_full_name() or self.username
    
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
    
    # Granular permission methods - using the new permission fields
    def has_module_access(self, module):
        """Check if user has any access to a module"""
        module_permissions = {
            'taxpayers': self.can_view_taxpayers or self.can_add_taxpayers or self.can_edit_taxpayers or self.can_delete_taxpayers,
            'returns': self.can_view_returns or self.can_add_returns or self.can_edit_returns or self.can_delete_returns,
            'refunds': self.can_view_refunds or self.can_add_refunds or self.can_edit_refunds or self.can_delete_refunds,
            'compliance': self.can_view_compliance or self.can_add_compliance or self.can_edit_compliance or self.can_delete_compliance,
            'risk_assessment': self.can_view_risk_assessment or self.can_run_risk_assessment or self.can_edit_risk_assessment or self.can_approve_risk_assessment,
            'enforcement': self.can_view_enforcement or self.can_add_enforcement or self.can_edit_enforcement or self.can_delete_enforcement,
            'audit': self.can_view_audit or self.can_create_audit or self.can_edit_audit or self.can_approve_audit,
            'reports': self.can_view_reports or self.can_generate_reports or self.can_export_reports,
            'users': self.can_view_users or self.can_add_users or self.can_edit_users or self.can_delete_users or self.can_manage_permissions,
            'settings': self.can_view_settings or self.can_edit_settings,
        }
        return module_permissions.get(module, False)
    
    def grant_all_permissions(self):
        """Grant all permissions to the user (for administrators)"""
        # Taxpayer Module Access
        self.can_view_taxpayers = True
        self.can_add_taxpayers = True
        self.can_edit_taxpayers = True
        self.can_delete_taxpayers = True
        
        # GST Returns Module Access
        self.can_view_returns = True
        self.can_add_returns = True
        self.can_edit_returns = True
        self.can_delete_returns = True
        
        # Refunds Module Access
        self.can_view_refunds = True
        self.can_add_refunds = True
        self.can_edit_refunds = True
        self.can_delete_refunds = True
        
        # Compliance Module Access
        self.can_view_compliance = True
        self.can_add_compliance = True
        self.can_edit_compliance = True
        self.can_delete_compliance = True
        
        # Risk Assessment Module Access
        self.can_view_risk_assessment = True
        self.can_run_risk_assessment = True
        self.can_edit_risk_assessment = True
        self.can_approve_risk_assessment = True
        
        # Enforcement & Recovery Module Access
        self.can_view_enforcement = True
        self.can_add_enforcement = True
        self.can_edit_enforcement = True
        self.can_delete_enforcement = True
        
        # Audit Module Access
        self.can_view_audit = True
        self.can_create_audit = True
        self.can_edit_audit = True
        self.can_approve_audit = True
        
        # Reports Module Access
        self.can_view_reports = True
        self.can_generate_reports = True
        self.can_export_reports = True
        
        # User Management Access
        self.can_view_users = True
        self.can_add_users = True
        self.can_edit_users = True
        self.can_delete_users = True
        self.can_manage_permissions = True
        
        # System Settings Access
        self.can_view_settings = True
        self.can_edit_settings = True
        
        # Import/Export Access
        self.can_import_data = True
        self.can_export_data = True

    def save(self, *args, **kwargs):
        """Override save to automatically grant all permissions to administrators"""
        if self.role == 'administrator':
            self.grant_all_permissions()
            # Also ensure Django superuser status
            self.is_superuser = True
            self.is_staff = True
        super().save(*args, **kwargs)

    def get_access_summary(self):
        """Get summary of user's access permissions"""
        access_summary = {
            'taxpayers': {
                'view': self.can_view_taxpayers,
                'add': self.can_add_taxpayers,
                'edit': self.can_edit_taxpayers,
                'delete': self.can_delete_taxpayers
            },
            'returns': {
                'view': self.can_view_returns,
                'add': self.can_add_returns,
                'edit': self.can_edit_returns,
                'delete': self.can_delete_returns
            },
            'refunds': {
                'view': self.can_view_refunds,
                'add': self.can_add_refunds,
                'edit': self.can_edit_refunds,
                'delete': self.can_delete_refunds
            },
            'compliance': {
                'view': self.can_view_compliance,
                'add': self.can_add_compliance,
                'edit': self.can_edit_compliance,
                'delete': self.can_delete_compliance
            },
            'risk_assessment': {
                'view': self.can_view_risk_assessment,
                'run': self.can_run_risk_assessment,
                'edit': self.can_edit_risk_assessment,
                'approve': self.can_approve_risk_assessment
            },
            'enforcement': {
                'view': self.can_view_enforcement,
                'add': self.can_add_enforcement,
                'edit': self.can_edit_enforcement,
                'delete': self.can_delete_enforcement
            },
            'audit': {
                'view': self.can_view_audit,
                'create': self.can_create_audit,
                'edit': self.can_edit_audit,
                'approve': self.can_approve_audit
            },
            'reports': {
                'view': self.can_view_reports,
                'generate': self.can_generate_reports,
                'export': self.can_export_reports
            },
            'users': {
                'view': self.can_view_users,
                'add': self.can_add_users,
                'edit': self.can_edit_users,
                'delete': self.can_delete_users,
                'manage_permissions': self.can_manage_permissions
            },
            'settings': {
                'view': self.can_view_settings,
                'edit': self.can_edit_settings
            },
            'data': {
                'import': self.can_import_data,
                'export': self.can_export_data
            }
        }
        return access_summary


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
    system_name = models.CharField(max_length=200, default='RRCO/GST Mongar Administration', verbose_name='System Name')
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