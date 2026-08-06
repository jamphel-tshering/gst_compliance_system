from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import RefundRegister
from .resources import RefundRegisterResource

def get_display_value(obj, field_name):
    """Helper function to get display value for choice fields"""
    value = getattr(obj, field_name)
    if not value:
        return '-'
    
    # Try to get the display value from choices
    try:
        choices_dict = dict(getattr(obj.__class__, field_name).field.choices)
        display_value = choices_dict.get(value, value)
    except:
        display_value = value
    
    # If still not found in choices, capitalize for better display
    if display_value == value and isinstance(value, str):
        display_value = value.replace('_', ' ').title()
    
    return display_value or '-'

@admin.register(RefundRegister)
class RefundRegisterAdmin(ImportExportModelAdmin):
    resource_class = RefundRegisterResource
    list_display = ['refund_id', 'gst_tpn', 'taxpayer_name', 'tax_period', 'claimed_amount', 'refund_approved', 'display_status', 'claim_date']
    list_filter = ['status', 'claim_date', 'tax_period']
    search_fields = ['refund_id', 'gst_tpn', 'taxpayer_name']
    ordering = ['-claim_date']
    readonly_fields = ['created_at', 'updated_at']
    
    def display_status(self, obj):
        return get_display_value(obj, 'status')
    display_status.short_description = 'Status'
    
    fieldsets = (
        ('Identification', {
            'fields': ('refund_id', 'gst_tpn', 'taxpayer_name')
        }),
        ('Period and Claim Details', {
            'fields': ('tax_period', 'claim_date', 'claimed_amount')
        }),
        ('Adjustment and Approval Details', {
            'fields': ('adjustment', 'refund_disallowed', 'refund_approved', 'refund_adjustment_percentage')
        }),
        ('Processing Details', {
            'fields': ('processing_days', 'processed_date', 'processed_by')
        }),
        ('Status and Reason', {
            'fields': ('status', 'refund_reason', 'reason_code', 'remarks')
        }),
        ('System Information', {
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )