from django.contrib import admin
from django.db.models import Count
from import_export.admin import ImportExportModelAdmin
from .models import TaxpayerMaster, AdditionalLicense
from .resources import TaxpayerMasterResource

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

class AdditionalLicenseInline(admin.TabularInline):
    """Inline admin for additional licenses under primary taxpayer"""
    model = TaxpayerMaster
    extra = 0
    can_delete = True
    verbose_name = "Additional License"
    verbose_name_plural = "Additional Licenses"
    fields = ['cid_company_reg_no', 'ramis_tpn', 'business_name', 'sector', 'sub_sector', 'business_activity', 'organisation_type', 'dzongkhag', 'status', 'registration_date', 'commencement_date', 'deregistration_date', 'email_address', 'mobile_number', 'business_address', 'remarks']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_primary_license=False)

@admin.register(TaxpayerMaster)
class TaxpayerMasterAdmin(ImportExportModelAdmin):
    resource_class = TaxpayerMasterResource
    list_display = ['gstin', 'taxpayer_name', 'business_name', 'cid_company_reg_no', 'ramis_tpn', 'sector', 'sub_sector', 'business_activity', 'display_organisation_type', 'display_frequency', 'dzongkhag', 'display_status', 'registration_date', 'commencement_date', 'deregistration_date', 'email_address', 'mobile_number', 'business_address', 'remarks']
    list_display_links = ['gstin', 'taxpayer_name']  # Allow clicking on GSTIN or name to edit
    list_filter = [
        'organisation_type', 
        'dzongkhag', 
        'status', 
        'frequency',
        'registration_date'
    ]
    
    # Enable filter counts
    show_full_result_count = True
    
    # Enable sidebar filter counts
    list_per_page = 100
    
    # Enable related object counts
    list_select_related = False
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Only show primary licenses - additional licenses are completely hidden
        return qs.filter(is_primary_license=True)
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # For primary licenses, set is_primary_license to True by default
        if 'is_primary_license' in form.base_fields:
            form.base_fields['is_primary_license'].initial = True
        return form
    
    # inlines = [AdditionalLicenseInline]  # Commented out for now
    search_fields = ['gstin', 'taxpayer_name', 'business_name', 'cid_company_reg_no']
    ordering = ['gstin', '-is_primary_license']  # Primary licenses first, grouped by GSTIN
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 100
    show_full_result_count = True
    
    def display_organisation_type(self, obj):
        return get_display_value(obj, 'organisation_type')
    display_organisation_type.short_description = 'Organisation Type'
    
    def display_frequency(self, obj):
        return get_display_value(obj, 'frequency')
    display_frequency.short_description = 'Frequency'
    
    def display_status(self, obj):
        return get_display_value(obj, 'status')
    display_status.short_description = 'Status'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Only show primary licenses by default
        # If user is searching for a specific GSTIN, show all licenses for that GSTIN
        if request.GET.get('q'):  # If there's a search query
            # Show all results when searching
            return qs
        else:
            # Default: show only primary licenses
            return qs.filter(is_primary_license=True)
    
    def get_search_results(self, request, queryset, search_term):
        """Custom search to show all licenses when searching by GSTIN"""
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        
        # If searching for a GSTIN, show all licenses for that GSTIN
        if search_term:
            # Check if search term might be a GSTIN
            gstin_matches = queryset.filter(gstin__icontains=search_term)
            if gstin_matches.exists():
                # Show all licenses for matching GSTINs
                matching_gstins = gstin_matches.values_list('gstin', flat=True).distinct()
                queryset = queryset.filter(gstin__in=matching_gstins)
        
        return queryset, use_distinct
    
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        """Handle choice fields to show both stored and display values for editing"""
        if db_field.name in ['organisation_type', 'frequency', 'status']:
            # Get all possible values from the database
            existing_values = TaxpayerMaster.objects.values_list(db_field.name, flat=True).distinct()
            existing_values = [v for v in existing_values if v]  # Remove None values
            
            # Get model choices
            model_choices = db_field.choices
            
            # Combine model choices with existing values not in choices for editing
            combined_choices = list(model_choices)
            for value in existing_values:
                if value not in [c[0] for c in combined_choices]:
                    # Add the existing value with a formatted display name
                    display_name = value.replace('_', ' ').title()
                    combined_choices.append((value, display_name))
            
            kwargs['choices'] = combined_choices
        return super().formfield_for_choice_field(db_field, request, **kwargs)
    
    def get_readonly_fields(self, request, obj=None):
        """Make primary_taxpayer readonly if this is a primary license"""
        if obj and obj.is_primary_license:
            return self.readonly_fields + ['primary_taxpayer']
        return self.readonly_fields


@admin.register(AdditionalLicense)
class AdditionalLicenseAdmin(ImportExportModelAdmin):
    """Separate admin for additional licenses only"""
    resource_class = TaxpayerMasterResource
    list_display = ['gstin', 'primary_taxpayer_link', 'taxpayer_name', 'business_name', 'cid_company_reg_no', 'ramis_tpn', 'sector', 'sub_sector', 'business_activity', 'display_organisation_type', 'display_frequency', 'dzongkhag', 'display_status', 'registration_date', 'commencement_date', 'deregistration_date', 'email_address', 'mobile_number', 'business_address', 'remarks']
    list_display_links = ['gstin', 'taxpayer_name']
    list_filter = [
        'organisation_type', 
        'dzongkhag', 
        'status', 
        'frequency',
        'registration_date',
        'primary_taxpayer'
    ]
    search_fields = ['gstin', 'taxpayer_name', 'business_name', 'cid_company_reg_no', 'primary_taxpayer__taxpayer_name']
    ordering = ['gstin', 'taxpayer_name']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 100
    show_full_result_count = True
    
    def primary_taxpayer_link(self, obj):
        if obj.primary_taxpayer:
            return obj.primary_taxpayer.taxpayer_name
        return "No Primary Linked"
    primary_taxpayer_link.short_description = 'Primary Taxpayer'
    
    def display_organisation_type(self, obj):
        return get_display_value(obj, 'organisation_type')
    display_organisation_type.short_description = 'Organisation Type'
    
    def display_frequency(self, obj):
        return get_display_value(obj, 'frequency')
    display_frequency.short_description = 'Frequency'
    
    def display_status(self, obj):
        return get_display_value(obj, 'status')
    display_status.short_description = 'Status'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Only show additional licenses
        return qs.filter(is_primary_license=False)
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Hide is_primary_license field for additional licenses
        if 'is_primary_license' in form.base_fields:
            form.base_fields['is_primary_license'].widget.attrs['readonly'] = True
            form.base_fields['is_primary_license'].widget.attrs['value'] = 'False'
        return form
    
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        """Handle choice fields to show both stored and display values for editing"""
        if db_field.name in ['organisation_type', 'frequency', 'status']:
            # Get all possible values from the database
            existing_values = TaxpayerMaster.objects.values_list(db_field.name, flat=True).distinct()
            existing_values = [v for v in existing_values if v]  # Remove None values
            
            # Get model choices
            model_choices = db_field.choices
            
            # Combine model choices with existing values not in choices for editing
            combined_choices = list(model_choices)
            for value in existing_values:
                if value not in [c[0] for c in combined_choices]:
                    # Add the existing value with a formatted display name
                    display_name = value.replace('_', ' ').title()
                    combined_choices.append((value, display_name))
            
            kwargs['choices'] = combined_choices
        return super().formfield_for_choice_field(db_field, request, **kwargs)
    
    fieldsets = (
        ('Identification Numbers', {
            'fields': ('cid_company_reg_no', 'gstin', 'ramis_tpn', 'is_primary_license', 'primary_taxpayer')
        }),
        ('Basic Information', {
            'fields': ('taxpayer_name', 'business_name')
        }),
        ('Classification', {
            'fields': ('sector', 'sub_sector', 'business_activity', 'organisation_type', 'frequency', 'dzongkhag', 'status')
        }),
        ('Important Dates', {
            'fields': ('registration_date', 'commencement_date', 'deregistration_date')
        }),
        ('Contact Information', {
            'fields': ('email_address', 'mobile_number', 'business_address')
        }),
        ('Additional Information', {
            'fields': ('remarks',)
        }),
        ('System Information', {
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        obj.full_clean()  # Call model's clean() method for validation
        super().save_model(request, obj, form, change)


@admin.register(TaxpayerMaster, site=admin.AdminSite(name='additional_licenses_admin'))
class AdditionalLicenseAdmin(ImportExportModelAdmin):
    """Separate admin for additional licenses only"""
    resource_class = TaxpayerMasterResource
    list_display = ['gstin', 'primary_taxpayer_link', 'taxpayer_name', 'business_name', 'cid_company_reg_no', 'ramis_tpn', 'sector', 'sub_sector', 'business_activity', 'display_organisation_type', 'display_frequency', 'dzongkhag', 'display_status', 'registration_date', 'commencement_date', 'deregistration_date', 'email_address', 'mobile_number', 'business_address', 'remarks']
    list_display_links = ['gstin', 'taxpayer_name']
    list_filter = [
        'organisation_type', 
        'dzongkhag', 
        'status', 
        'frequency',
        'registration_date',
        'primary_taxpayer'
    ]
    search_fields = ['gstin', 'taxpayer_name', 'business_name', 'cid_company_reg_no', 'primary_taxpayer__taxpayer_name']
    ordering = ['gstin', 'taxpayer_name']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 100
    show_full_result_count = True
    
    def primary_taxpayer_link(self, obj):
        if obj.primary_taxpayer:
            return obj.primary_taxpayer.taxpayer_name
        return "No Primary Linked"
    primary_taxpayer_link.short_description = 'Primary Taxpayer'
    
    def display_organisation_type(self, obj):
        return get_display_value(obj, 'organisation_type')
    display_organisation_type.short_description = 'Organisation Type'
    
    def display_frequency(self, obj):
        return get_display_value(obj, 'frequency')
    display_frequency.short_description = 'Frequency'
    
    def display_status(self, obj):
        return get_display_value(obj, 'status')
    display_status.short_description = 'Status'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Only show additional licenses
        return qs.filter(is_primary_license=False)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Only show additional licenses
        return qs.filter(is_primary_license=False)
    
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        """Handle choice fields to show both stored and display values for editing"""
        if db_field.name in ['organisation_type', 'frequency', 'status']:
            # Get all possible values from the database
            existing_values = TaxpayerMaster.objects.values_list(db_field.name, flat=True).distinct()
            existing_values = [v for v in existing_values if v]  # Remove None values
            
            # Get model choices
            model_choices = db_field.choices
            
            # Combine model choices with existing values not in choices for editing
            combined_choices = list(model_choices)
            for value in existing_values:
                if value not in [c[0] for c in combined_choices]:
                    # Add the existing value with a formatted display name
                    display_name = value.replace('_', ' ').title()
                    combined_choices.append((value, display_name))
            
            kwargs['choices'] = combined_choices
        return super().formfield_for_choice_field(db_field, request, **kwargs)
    
    fieldsets = (
        ('Identification Numbers', {
            'fields': ('cid_company_reg_no', 'gstin', 'ramis_tpn', 'is_primary_license', 'primary_taxpayer')
        }),
        ('Basic Information', {
            'fields': ('taxpayer_name', 'business_name')
        }),
        ('Classification', {
            'fields': ('sector', 'sub_sector', 'business_activity', 'organisation_type', 'frequency', 'dzongkhag', 'status')
        }),
        ('Important Dates', {
            'fields': ('registration_date', 'commencement_date', 'deregistration_date')
        }),
        ('Contact Information', {
            'fields': ('email_address', 'mobile_number', 'business_address')
        }),
        ('Additional Information', {
            'fields': ('remarks',)
        }),
        ('System Information', {
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        obj.full_clean()  # Call model's clean() method for validation
        super().save_model(request, obj, form, change)
    
    fieldsets = (
        ('Identification Numbers', {
            'fields': ('cid_company_reg_no', 'gstin', 'ramis_tpn', 'is_primary_license', 'primary_taxpayer')
        }),
        ('Basic Information', {
            'fields': ('taxpayer_name', 'business_name')
        }),
        ('Classification', {
            'fields': ('sector', 'sub_sector', 'business_activity', 'organisation_type', 'frequency', 'dzongkhag', 'status')
        }),
        ('Important Dates', {
            'fields': ('registration_date', 'commencement_date', 'deregistration_date')
        }),
        ('Contact Information', {
            'fields': ('email_address', 'mobile_number', 'business_address')
        }),
        ('Additional Information', {
            'fields': ('remarks',)
        }),
        ('System Information', {
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        obj.full_clean()  # Call model's clean() method for validation
        super().save_model(request, obj, form, change)
    
    # Statistics in admin dashboard
    def changelist_view(self, request, extra_context=None):
        # Get the current queryset (respecting filters)
        cl = self.get_changelist_instance(request)
        queryset = cl.get_queryset(request)
        
        # Get statistics based on current view
        total_registered = queryset.count()
        deregistered_taxpayers = queryset.filter(status='deregistered').count()
        active_taxpayers = queryset.filter(status='active').count()
        
        # Primary licenses = total registered - deregistered
        primary_licenses = total_registered - deregistered_taxpayers
        additional_licenses = queryset.filter(is_primary_license=False).count()
        
        extra_context = extra_context or {}
        extra_context.update({
            'total_registered': total_registered,
            'active_taxpayers': active_taxpayers,
            'deregistered_taxpayers': deregistered_taxpayers,
            'primary_licenses': primary_licenses,
            'additional_licenses': additional_licenses,
        })
        
        return super().changelist_view(request, extra_context=extra_context)