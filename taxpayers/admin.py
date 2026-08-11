from django.contrib import admin, messages
from django.db.models import Count
from django import forms
from django.forms import DateInput
from import_export.admin import ImportExportModelAdmin
from .models import TaxpayerMaster, MultipleLicenseReference
from .resources import TaxpayerMasterResource, MultipleLicenseResource
from risk_assessment.models import RiskAlert


class AllStatusFilter(admin.SimpleListFilter):
    """Custom filter that shows all status counts regardless of queryset filtering"""
    title = 'Status'
    parameter_name = 'status'
    
    def lookups(self, request, model_admin):
        # Get all statuses with counts from all primary licenses
        statuses = ['Active', 'Inactive', 'Suspended', 'Cancelled', 'Deregistered']
        choices = []
        for status in statuses:
            count = TaxpayerMaster.objects.filter(status=status, is_primary_license=True).count()
            if count > 0:
                choices.append((status, f"{status} ({count})"))
        return choices
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())
        return queryset


class ActiveOnlyOrgTypeFilter(admin.SimpleListFilter):
    """Custom filter that shows active-only counts for organization type"""
    title = 'Organisation Type'
    parameter_name = 'organisation_type'
    
    def lookups(self, request, model_admin):
        # Get all organization types with active-only counts
        org_types = ['Sole Proprietorship', 'Private Company', 'Public Company', 'Partnership', 'Government Entity', 'Foreign Company', 'Joint Venture', 'State Owned Company', 'Other']
        choices = []
        for org_type in org_types:
            active_count = TaxpayerMaster.objects.filter(organisation_type=org_type, status='Active', is_primary_license=True).count()
            if active_count > 0:
                choices.append((org_type, f"{org_type} ({active_count})"))
        return choices
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(organisation_type=self.value())
        return queryset


class ActiveOnlyDzongkhagFilter(admin.SimpleListFilter):
    """Custom filter that shows active-only counts for dzongkhag"""
    title = 'Dzongkhag'
    parameter_name = 'dzongkhag'
    
    def lookups(self, request, model_admin):
        # Get all dzongkhags with active-only counts
        dzongkhags = ['Mongar', 'Trashigang', 'Trashiyangtse', 'Lhuentse']
        choices = []
        for dzongkhag in dzongkhags:
            active_count = TaxpayerMaster.objects.filter(dzongkhag=dzongkhag, status='Active', is_primary_license=True).count()
            if active_count > 0:
                choices.append((dzongkhag, f"{dzongkhag} ({active_count})"))
        return choices
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(dzongkhag=self.value())
        return queryset


class ActiveOnlyFrequencyFilter(admin.SimpleListFilter):
    """Custom filter that shows active-only counts for frequency"""
    title = 'Frequency'
    parameter_name = 'frequency'
    
    def lookups(self, request, model_admin):
        # Get all frequencies with active-only counts
        frequencies = ['Monthly', 'Quarterly', 'Half Yearly']
        choices = []
        for frequency in frequencies:
            active_count = TaxpayerMaster.objects.filter(frequency=frequency, status='Active', is_primary_license=True).count()
            if active_count > 0:
                choices.append((frequency, f"{frequency} ({active_count})"))
        return choices
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(frequency=self.value())
        return queryset


class TaxpayerMasterForm(forms.ModelForm):
    """Custom form to fix date format and ensure no duplicates"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Define valid choices explicitly to avoid duplicates
        FREQUENCY_CHOICES = [
            ('Monthly', 'Monthly'),
            ('Quarterly', 'Quarterly'),
            ('Half Yearly', 'Half Yearly'),
        ]
        STATUS_CHOICES = [
            ('Active', 'Active'),
            ('Inactive', 'Inactive'),
            ('Suspended', 'Suspended'),
            ('Cancelled', 'Cancelled'),
            ('Deregistered', 'Deregistered'),
        ]
        ORGANISATION_TYPES = [
            ('Sole Proprietorship', 'Sole Proprietorship'),
            ('Private Company', 'Private Company'),
            ('Public Company', 'Public Company'),
            ('Partnership', 'Partnership'),
            ('Government Entity', 'Government Entity'),
            ('Foreign Company', 'Foreign Company'),
            ('Joint Venture', 'Joint Venture'),
            ('State Owned Company', 'State Owned Company'),
            ('Other', 'Other'),
        ]
        DZONGKHAG_CHOICES = [
            ('Mongar', 'Mongar'),
            ('Trashigang', 'Trashigang'),
            ('Trashiyangtse', 'Trashiyangtse'),
            ('Lhuentse', 'Lhuentse'),
        ]
        
        if 'frequency' in self.fields:
            self.fields['frequency'].choices = FREQUENCY_CHOICES
            self.fields['frequency'].required = False
            self.fields['frequency'].empty_label = None
        
        if 'status' in self.fields:
            self.fields['status'].choices = STATUS_CHOICES
            self.fields['status'].required = False
            self.fields['status'].empty_label = None
        
        if 'organisation_type' in self.fields:
            self.fields['organisation_type'].choices = ORGANISATION_TYPES
            self.fields['organisation_type'].required = False
            self.fields['organisation_type'].empty_label = None
        
        if 'dzongkhag' in self.fields:
            self.fields['dzongkhag'].choices = DZONGKHAG_CHOICES
            self.fields['dzongkhag'].required = False
            self.fields['dzongkhag'].empty_label = None
    
    class Meta:
        model = TaxpayerMaster
        fields = '__all__'

def get_display_value(obj, field_name):
    """Helper function to get display value for choice fields"""
    value = getattr(obj, field_name)
    if not value:
        return '-'
    
    # Return value as-is since database values are now capitalized
    return str(value)


@admin.register(TaxpayerMaster)
class TaxpayerMasterAdmin(ImportExportModelAdmin):
    resource_class = TaxpayerMasterResource
    form = TaxpayerMasterForm
    change_list_template = 'admin/taxpayers/change_list.html'
    list_display = ['gstin', 'taxpayer_name', 'business_name', 'cid_company_reg_no', 'ramis_tpn', 'sector', 'sub_sector', 'business_activity', 'organisation_type', 'frequency', 'display_dzongkhag', 'status', 'display_registration_date', 'display_commencement_date', 'display_deregistration_date', 'email_address', 'mobile_number', 'business_address', 'remarks']
    list_display_links = ['gstin', 'taxpayer_name']  # Allow clicking on GSTIN or name to edit
    list_filter = [
        ActiveOnlyOrgTypeFilter,
        ActiveOnlyDzongkhagFilter,
        AllStatusFilter,
        ActiveOnlyFrequencyFilter,
        'registration_date'
    ]
    
    search_fields = ['gstin', 'taxpayer_name', 'business_name', 'cid_company_reg_no', 'ramis_tpn']
    
    # Enhanced search to show all related records
    search_help_text = 'Search by GSTIN, Taxpayer Name, Business Name, CID/Company Reg No, or RAMIS TPN. All matching records will be shown.'
    
    def get_search_results(self, request, queryset, search_term):
        """Override to ensure all related records are shown when searching"""
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        # Don't apply any additional filtering - show all matching records
        return queryset, use_distinct
    
    def display_dzongkhag(self, obj):
        return get_display_value(obj, 'dzongkhag')
    display_dzongkhag.short_description = 'Dzongkhag'
    
    def display_registration_date(self, obj):
        return get_display_value(obj, 'registration_date')
    display_registration_date.short_description = 'Registration Date'
    
    def display_commencement_date(self, obj):
        return get_display_value(obj, 'commencement_date')
    display_commencement_date.short_description = 'Commencement Date'
    
    def display_deregistration_date(self, obj):
        return get_display_value(obj, 'deregistration_date')
    display_deregistration_date.short_description = 'Deregistration Date'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Show all primary licenses for accurate status filter counts
        qs = qs.filter(is_primary_license=True)
        return qs
    
    def save_model(self, request, obj, form, change):
        if not change:
            # Creating a new taxpayer - ensure it's marked as primary license
            obj.is_primary_license = True
        super().save_model(request, obj, form, change)
    
    def changelist_view(self, request, extra_context=None):
        """Add summary statistics to the changelist view"""
        extra_context = extra_context or {}
        
        # Get summary statistics (primary licenses only)
        total_active = TaxpayerMaster.objects.filter(status='Active', is_primary_license=True).count()
        total_deregistered = TaxpayerMaster.objects.filter(status='Deregistered', is_primary_license=True).count()
        
        # Organisation type breakdown with both active and deregistered counts
        org_type_counts = {}
        for org_type in ['Sole Proprietorship', 'Private Company', 'Public Company', 'Partnership', 'Government Entity', 'Foreign Company', 'Joint Venture', 'State Owned Company', 'Other']:
            active_count = TaxpayerMaster.objects.filter(organisation_type=org_type, status='Active', is_primary_license=True).count()
            dereg_count = TaxpayerMaster.objects.filter(organisation_type=org_type, status='Deregistered', is_primary_license=True).count()
            if active_count > 0 or dereg_count > 0:
                org_type_counts[org_type] = {'active': active_count, 'deregistered': dereg_count}
        
        # Dzongkhag breakdown with both active and deregistered counts
        dzongkhag_counts = {}
        for dzongkhag in ['Mongar', 'Trashigang', 'Trashiyangtse', 'Lhuentse']:
            active_count = TaxpayerMaster.objects.filter(dzongkhag=dzongkhag, status='Active', is_primary_license=True).count()
            dereg_count = TaxpayerMaster.objects.filter(dzongkhag=dzongkhag, status='Deregistered', is_primary_license=True).count()
            if active_count > 0 or dereg_count > 0:
                dzongkhag_counts[dzongkhag] = {'active': active_count, 'deregistered': dereg_count}
        
        # Frequency breakdown with both active and deregistered counts
        frequency_counts = {}
        for frequency in ['Monthly', 'Quarterly', 'Half Yearly']:
            active_count = TaxpayerMaster.objects.filter(frequency=frequency, status='Active', is_primary_license=True).count()
            dereg_count = TaxpayerMaster.objects.filter(frequency=frequency, status='Deregistered', is_primary_license=True).count()
            if active_count > 0 or dereg_count > 0:
                frequency_counts[frequency] = {'active': active_count, 'deregistered': dereg_count}
        
        # Create HTML for summary panel
        summary_html = f"""
        <div style="background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="font-size: 18px; font-weight: bold; color: #333; margin-bottom: 15px; border-bottom: 2px solid #007bff; padding-bottom: 10px;">
                Taxpayers Summary (Active vs Deregistered)
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px;">
                <div style="background: white; padding: 15px; border-radius: 6px; border-left: 4px solid #007bff; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                    <div style="font-size: 12px; color: #666; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 5px;">Total Active</div>
                    <div style="font-size: 24px; font-weight: bold; color: #28a745;">{total_active}</div>
                </div>
                <div style="background: white; padding: 15px; border-radius: 6px; border-left: 4px solid #007bff; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                    <div style="font-size: 12px; color: #666; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 5px;">Total Deregistered</div>
                    <div style="font-size: 24px; font-weight: bold; color: #dc3545;">{total_deregistered}</div>
                </div>
                <div style="background: white; padding: 15px; border-radius: 6px; border-left: 4px solid #007bff; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                    <div style="font-size: 12px; color: #666; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 5px;">By Organisation Type</div>
        """
        
        for org_type, counts in org_type_counts.items():
            dereg_display = f"| {counts['deregistered']}" if counts['deregistered'] > 0 else ""
            summary_html += f"""
                    <div style="font-size: 14px; color: #555; margin: 5px 0; display: flex; justify-content: space-between;">
                        <span>{org_type}</span>
                        <span style="font-weight: bold; color: #007bff;"><span style="color: #28a745;">{counts['active']}</span> {dereg_display}</span>
                    </div>
            """
        
        summary_html += """
                </div>
                <div style="background: white; padding: 15px; border-radius: 6px; border-left: 4px solid #007bff; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                    <div style="font-size: 12px; color: #666; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 5px;">By Dzongkhag</div>
        """
        
        for dzongkhag, counts in dzongkhag_counts.items():
            dereg_display = f"| {counts['deregistered']}" if counts['deregistered'] > 0 else ""
            summary_html += f"""
                    <div style="font-size: 14px; color: #555; margin: 5px 0; display: flex; justify-content: space-between;">
                        <span>{dzongkhag}</span>
                        <span style="font-weight: bold; color: #007bff;"><span style="color: #28a745;">{counts['active']}</span> {dereg_display}</span>
                    </div>
            """
        
        summary_html += """
                </div>
                <div style="background: white; padding: 15px; border-radius: 6px; border-left: 4px solid #007bff; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                    <div style="font-size: 12px; color: #666; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 5px;">By Frequency</div>
        """
        
        for frequency, counts in frequency_counts.items():
            dereg_display = f"| {counts['deregistered']}" if counts['deregistered'] > 0 else ""
            summary_html += f"""
                    <div style="font-size: 14px; color: #555; margin: 5px 0; display: flex; justify-content: space-between;">
                        <span>{frequency}</span>
                        <span style="font-weight: bold; color: #007bff;"><span style="color: #28a745;">{counts['active']}</span> {dereg_display}</span>
                    </div>
            """
        
        summary_html += """
                </div>
            </div>
        </div>
        """
        
        extra_context.update({
            'summary_html': summary_html,
        })
        
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(MultipleLicenseReference)
class MultipleLicenseAdmin(ImportExportModelAdmin):
    """Admin for Multiple License References - separate section for reference purposes"""
    resource_class = MultipleLicenseResource
    change_list_template = 'admin/taxpayers/multiple_license_change_list.html'
    list_display = ['gstin', 'display_ramis_tpn', 'taxpayer_name', 'business_name', 'cid_company_reg_no', 'sector', 'sub_sector', 'business_activity', 'organisation_type', 'frequency', 'dzongkhag', 'status', 'registration_date', 'commencement_date', 'deregistration_date', 'email_address', 'mobile_number', 'display_business_address', 'remarks']
    list_display_links = ['gstin', 'taxpayer_name']
    list_filter = ['organisation_type', 'dzongkhag', 'status', 'frequency', 'registration_date']
    search_fields = ['gstin', 'license_number', 'taxpayer_name', 'business_name', 'cid_company_reg_no', 'ramis_tpn']
    list_per_page = 100  # Show more records per page
    show_full_result_count = False  # Hide filter counts
    
    search_help_text = 'Search by GSTIN to see all related licenses for that taxpayer.'
    
    def display_ramis_tpn(self, obj):
        """Display RAMIS TPN as the license number with proper heading"""
        return obj.license_number
    display_ramis_tpn.short_description = 'RAMIS TPN'
    
    def display_business_address(self, obj):
        """Display full business address with proper formatting"""
        if obj.business_address:
            return obj.business_address
        return '-'
    display_business_address.short_description = 'Business Address'
    display_business_address.allow_tags = True