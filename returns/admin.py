from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import GSTReturn, NotFile
from .resources import GSTReturnResource, NotFileResource

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

@admin.register(GSTReturn)
class GSTReturnAdmin(ImportExportModelAdmin):
    resource_class = GSTReturnResource
    list_display = ['tax_period', 'gstin', 'taxpayer_name', 'dzongkhag', 'display_organisation_type', 'display_frequency', 'declared_sales', 'declared_domestic_purchase', 'declared_import_value', 'declared_import_gst', 'domestic_purchase_itc_claimed', 'total_itc_claimed', 'declared_output_gst', 'gst_payable_refundable', 'actual_gst_payment_received', 'display_filing_status', 'display_payment_status', 'display_compliance_status', 'remarks']
    list_filter = ['tax_period', 'filing_status', 'payment_status', 'compliance_status', 'organisation_type', 'dzongkhag']
    search_fields = ['gstin', 'taxpayer_name']
    ordering = ['-tax_period', 'taxpayer_name']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 100
    show_full_result_count = True
    
    def display_organisation_type(self, obj):
        return get_display_value(obj, 'organisation_type')
    display_organisation_type.short_description = 'Organisation Type'
    
    def display_frequency(self, obj):
        return get_display_value(obj, 'frequency')
    display_frequency.short_description = 'Frequency'
    
    def display_filing_status(self, obj):
        return get_display_value(obj, 'filing_status')
    display_filing_status.short_description = 'Filing Status'
    
    def display_payment_status(self, obj):
        return get_display_value(obj, 'payment_status')
    display_payment_status.short_description = 'Payment Status'
    
    def display_compliance_status(self, obj):
        return get_display_value(obj, 'compliance_status')
    display_compliance_status.short_description = 'Compliance Status'
    
    fieldsets = (
        ('Period Information', {
            'fields': ('tax_period', 'return_due_date', 'return_filing_date', 'filing_delay_days')
        }),
        ('Taxpayer Information', {
            'fields': ('gstin', 'taxpayer_name', 'dzongkhag', 'organisation_type', 'frequency')
        }),
        ('Financial Details - Declared', {
            'fields': ('declared_sales', 'declared_domestic_purchase', 'declared_import_value', 'ecms_import_value', 'declared_import_gst')
        }),
        ('ITC Details', {
            'fields': ('domestic_purchase_itc_claimed', 'total_itc_claimed')
        }),
        ('Output GST', {
            'fields': ('declared_output_gst',)
        }),
        ('GST Payable/Refundable', {
            'fields': ('gst_payable_refundable', 'actual_gst_payment_received', 'bank_deposits')
        }),
        ('Status Information', {
            'fields': ('filing_status', 'payment_status', 'compliance_status')
        }),
        ('Additional Information', {
            'fields': ('remarks',)
        }),
        ('System Information', {
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(NotFile)
class NotFileAdmin(ImportExportModelAdmin):
    resource_class = NotFileResource
    list_display = ['gstin', 'taxpayer_name', 'return_period', 'display_filing_status', 'display_payment_status']
    list_filter = ['filing_status', 'payment_status']
    search_fields = ['gstin', 'taxpayer_name']
    ordering = ['-return_period', 'taxpayer_name']
    readonly_fields = ['created_at', 'updated_at']
    
    def display_filing_status(self, obj):
        return get_display_value(obj, 'filing_status')
    display_filing_status.short_description = 'Filing Status'
    
    def display_payment_status(self, obj):
        return get_display_value(obj, 'payment_status')
    display_payment_status.short_description = 'Payment Status'
    
    fieldsets = (
        ('Taxpayer Information', {
            'fields': ('gstin', 'taxpayer_name', 'organisation_type')
        }),
        ('Return Period', {
            'fields': ('return_period',)
        }),
        ('Status Information', {
            'fields': ('payment_status', 'filing_status')
        }),
        ('System Information', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )