from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, AuditLog, SystemSettings
from django.shortcuts import render
from django.urls import reverse
from django.contrib.admin import AdminSite


# Main Dashboard View
def main_dashboard(request):
    """Main dashboard with links to all module dashboards"""
    dashboard_links = [
        {
            'title': 'Taxpayer Management',
            'url': '/taxpayers/',
            'description': 'Manage taxpayer registration and profiles',
            'icon': '👥'
        },
        {
            'title': 'GST Returns',
            'url': '/returns/',
            'description': 'Process and monitor GST returns',
            'icon': '📋'
        },
        {
            'title': 'Compliance Monitoring',
            'url': '/compliance/',
            'description': 'Compliance monitoring, risk assessment, and enforcement',
            'icon': '✅'
        },
        {
            'title': 'Audit & Refund',
            'url': '/audit_refund/',
            'description': 'Audit case management and refund processing',
            'icon': '🔍'
        },
        {
            'title': 'Reporting',
            'url': '/reporting/',
            'description': 'Centralized Reporting and Analytics Layer',
            'icon': '📊'
        },
    ]
    
    context = {
        'title': 'RRCO/GST Mongar Administration',
        'subtitle': 'Main Dashboard',
        'dashboard_links': dashboard_links,
    }
    
    return render(request, 'core/main_dashboard.html', context)


# Use default admin site for core to avoid circular import
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'get_role_display', 'is_active', 'created_at']
    list_filter = ['role', 'is_active', 'created_at']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone', 'department', 'employee_id')}),
        ('Role & Status', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Taxpayer Module Access', {
            'fields': ('can_view_taxpayers', 'can_add_taxpayers', 'can_edit_taxpayers', 'can_delete_taxpayers'),
            'classes': ('collapse',)
        }),
        ('GST Returns Module Access', {
            'fields': ('can_view_returns', 'can_add_returns', 'can_edit_returns', 'can_delete_returns'),
            'classes': ('collapse',)
        }),
        ('Refunds Module Access', {
            'fields': ('can_view_refunds', 'can_add_refunds', 'can_edit_refunds', 'can_delete_refunds'),
            'classes': ('collapse',)
        }),
        ('Compliance Module Access', {
            'fields': ('can_view_compliance', 'can_add_compliance', 'can_edit_compliance', 'can_delete_compliance'),
            'classes': ('collapse',)
        }),
        ('Risk Assessment Module Access', {
            'fields': ('can_view_risk_assessment', 'can_run_risk_assessment', 'can_edit_risk_assessment', 'can_approve_risk_assessment'),
            'classes': ('collapse',)
        }),
        ('Enforcement & Recovery Module Access', {
            'fields': ('can_view_enforcement', 'can_add_enforcement', 'can_edit_enforcement', 'can_delete_enforcement'),
            'classes': ('collapse',)
        }),
        ('Audit Module Access', {
            'fields': ('can_view_audit', 'can_create_audit', 'can_edit_audit', 'can_approve_audit'),
            'classes': ('collapse',)
        }),
        ('Reports Module Access', {
            'fields': ('can_view_reports', 'can_generate_reports', 'can_export_reports'),
            'classes': ('collapse',)
        }),
        ('User Management Access', {
            'fields': ('can_view_users', 'can_add_users', 'can_edit_users', 'can_delete_users', 'can_manage_permissions'),
            'classes': ('collapse',)
        }),
        ('System Settings Access', {
            'fields': ('can_view_settings', 'can_edit_settings'),
            'classes': ('collapse',)
        }),
        ('Data Import/Export Access', {
            'fields': ('can_import_data', 'can_export_data'),
            'classes': ('collapse',)
        }),
        ('Important Dates', {'fields': ('last_login', 'date_joined', 'last_password_change')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1', 'password2'),
        }),
    )


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'model_name', 'timestamp', 'ip_address']
    list_filter = ['action', 'timestamp']
    search_fields = ['user__email', 'description']
    readonly_fields = ['user', 'action', 'model_name', 'object_id', 'description', 'ip_address', 'timestamp']
    ordering = ['-timestamp']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ['system_name', 'organization_name', 'contact_email', 'updated_at', 'updated_by']
    search_fields = ['system_name', 'organization_name', 'contact_email']
    fieldsets = (
        ('General Information', {
            'fields': ('system_name', 'organization_name')
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone', 'contact_address')
        }),
        ('Notification Settings', {
            'fields': ('send_email_notifications', 'email_smtp_server', 'email_smtp_port')
        }),
        ('Report Settings', {
            'fields': ('report_logo_url', 'report_footer_text')
        }),
        ('System Information', {
            'fields': ('updated_at', 'updated_by'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['updated_at', 'updated_by']
    
    def has_add_permission(self, request):
        # Only allow one system settings record
        if SystemSettings.objects.exists():
            return False
        return request.user.is_superuser or request.user.is_administrator()
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_administrator()
