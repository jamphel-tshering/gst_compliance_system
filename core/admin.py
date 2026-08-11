from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, AuditLog, SystemSettings

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
        ('Role & Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
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