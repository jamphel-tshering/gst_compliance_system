from django.contrib import admin
from django import forms
from django.forms import DateInput
from django.contrib.admin import SimpleListFilter
from datetime import datetime, date
from import_export.admin import ImportExportModelAdmin
from .models import GSTReturn
from .resources import GSTReturnResource


# Custom date input widget for dd-mm-yyyy format
class CustomDateInput(DateInput):
    input_type = 'date'
    def __init__(self, attrs=None):
        default_attrs = {'type': 'date'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)



class TaxPeriodFilter(SimpleListFilter):
    """Custom filter for tax period to display in Jan-2026 format"""
    title = 'Tax Period'
    parameter_name = 'tax_period'
    
    def lookups(self, request, model_admin):
        # Get unique tax periods in Jan-2026 format
        tax_periods = set()
        for obj in GSTReturn.objects.all():
            if obj.tax_period:
                tax_periods.add((obj.tax_period, obj.tax_period))
        
        # Sort by month-year (parse and sort)
        def sort_key(period):
            try:
                from datetime import datetime
                return datetime.strptime(period[0], '%b-%Y')
            except:
                return datetime.min
        
        sorted_periods = sorted(tax_periods, key=sort_key, reverse=True)
        return sorted_periods
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(tax_period=self.value())
        return queryset


class GSTReturnForm(forms.ModelForm):
    """Custom form with tax period dropdown"""
    class Meta:
        model = GSTReturn
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set tax period choices
        TAX_PERIOD_CHOICES = [
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
            ('Jan-2027', 'Jan-2027'),
            ('Feb-2027', 'Feb-2027'),
            ('Mar-2027', 'Mar-2027'),
            ('Apr-2027', 'Apr-2027'),
            ('May-2027', 'May-2027'),
            ('Jun-2027', 'Jun-2027'),
            ('Jul-2027', 'Jul-2027'),
            ('Aug-2027', 'Aug-2027'),
            ('Sep-2027', 'Sep-2027'),
            ('Oct-2027', 'Oct-2027'),
            ('Nov-2027', 'Nov-2027'),
            ('Dec-2027', 'Dec-2027'),
        ]
        
        if 'tax_period' in self.fields:
            self.fields['tax_period'].choices = TAX_PERIOD_CHOICES
            self.fields['tax_period'].required = True
        
        # Add date widgets for date fields
        from django.forms import DateInput
        if 'return_due_date' in self.fields:
            self.fields['return_due_date'].widget = DateInput(attrs={'type': 'date'})
        if 'return_filing_date' in self.fields:
            self.fields['return_filing_date'].widget = DateInput(attrs={'type': 'date'})

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
    form = GSTReturnForm
    list_display = ['display_tax_period', 'gstin', 'taxpayer_name', 'dzongkhag', 'display_organisation_type', 'display_frequency', 'declared_sales', 'declared_domestic_purchase', 'declared_import_value', 'declared_import_gst', 'domestic_purchase_itc_claimed', 'total_itc_claimed', 'declared_output_gst', 'gst_payable_refundable', 'actual_gst_payment_received', 'display_return_due_date', 'display_return_filing_date', 'display_filing_status', 'display_payment_status', 'display_compliance_status', 'remarks']
    list_filter = [TaxPeriodFilter, 'filing_status', 'payment_status', 'compliance_status', 'organisation_type', 'dzongkhag']
    search_fields = ['gstin', 'taxpayer_name']
    ordering = ['-tax_period', 'taxpayer_name']
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.__class__.__name__ in ['DateField', 'DateTimeField']:
            kwargs['widget'] = CustomDateInput()
        return super().formfield_for_dbfield(db_field, **kwargs)
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 100
    show_full_result_count = False
    
    class Media:
        css = {
            'all': ('static/admin/css/hide_filter_counts.css',)
        }
    
    class Media:
        css = {
            'all': ('admin/css/hide_filter_counts.css',)
        }
    
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
    
    def display_tax_period(self, obj):
        """Display tax period in Jan-2026 format"""
        if obj.tax_period:
            return obj.tax_period  # Already stored in Jan-2026 format
        return '-'
    display_tax_period.short_description = 'Tax Period'
    
    def display_return_due_date(self, obj):
        """Display return due date in dd-mm-yyyy format with leading zeros"""
        if obj.return_due_date:
            return obj.return_due_date.strftime('%d-%m-%Y')
        return '-'
    display_return_due_date.short_description = 'Return Due Date'
    
    def display_return_filing_date(self, obj):
        """Display return filing date in dd-mm-yyyy format with leading zeros"""
        if obj.return_filing_date:
            return obj.return_filing_date.strftime('%d-%m-%Y')
        return '-'
    display_return_filing_date.short_description = 'Return Filing Date'
    
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
            'fields': ('gst_payable_refundable', 'actual_gst_payment_received')
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