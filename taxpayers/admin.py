from django.contrib import admin, messages
from django.db.models import Count, Q
from django import forms
from django.forms import DateInput
from django.http import JsonResponse
from django.urls import path
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import TaxpayerMaster, MultipleLicenseReference, TaxpayerEnquiry
from core.form_widgets import CustomDateInput


class AllStatusFilter(admin.SimpleListFilter):
    """Custom filter that shows all status counts regardless of queryset filtering"""
    title = 'Status'
    parameter_name = 'status'
    
    def lookups(self, request, model_admin):
        # Get all statuses with counts from all primary licenses
        statuses = ['Active', 'Inactive', 'Suspended', 'Cancelled', 'Deregistered', 'Region Transferred']
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
            ('Region Transferred', 'Region Transferred'),
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
        
        # Use native date picker
        date_fields = ['registration_date', 'commencement_date', 'deregistration_date']
        for field in date_fields:
            if field in self.fields:
                self.fields[field].widget = forms.DateInput(attrs={'type': 'date'})
                
                # Set initial value if instance exists and has date
                if self.instance and getattr(self.instance, field):
                    from datetime import datetime
                    date_value = getattr(self.instance, field)
                    if date_value:
                        # Store in YYYY-MM-DD for date picker
                        formatted_date = date_value.strftime('%Y-%m-%d')
                        self.fields[field].initial = formatted_date
    
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


class TaxpayerMasterResource(resources.ModelResource):
    class Meta:
        model = TaxpayerMaster
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ['gstin']


@admin.register(TaxpayerMaster)
class TaxpayerMasterAdmin(ImportExportModelAdmin):
    form = TaxpayerMasterForm
    list_display = ['gstin', 'taxpayer_name', 'business_name', 'organisation_type', 'status', 'display_dzongkhag', 'frequency', 'display_registration_date']
    list_display_links = ['gstin', 'taxpayer_name']  # Allow clicking on GSTIN or name to edit
    list_per_page = 20  # Show 20 records per page with pagination
    list_filter = [
        ActiveOnlyOrgTypeFilter,
        ActiveOnlyDzongkhagFilter,
        AllStatusFilter,
        ActiveOnlyFrequencyFilter,
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
        """Display registration date in dd-mm-yyyy format with leading zeros"""
        if obj.registration_date:
            return obj.registration_date.strftime('%d-%m-%Y')
        return '-'
    display_registration_date.short_description = 'Registration Date'
    
    def display_commencement_date(self, obj):
        """Display commencement date in dd-mm-yyyy format with leading zeros"""
        if obj.commencement_date:
            return obj.commencement_date.strftime('%d-%m-%Y')
        return '-'
    display_commencement_date.short_description = 'Commencement Date'
    
    def display_deregistration_date(self, obj):
        """Display deregistration date in dd-mm-yyyy format with leading zeros"""
        if obj.deregistration_date:
            return obj.deregistration_date.strftime('%d-%m-%Y')
        return '-'
    display_deregistration_date.short_description = 'Deregistration/Region Transfer Date'
    
    def get_queryset(self, request):
        """Override to handle custom date range filtering"""
        qs = super().get_queryset(request)
        
        # Show all primary licenses for accurate status filter counts
        qs = qs.filter(is_primary_license=True)
        
        # Handle custom date range filtering
        start_date = request.GET.get('reg_start_date')
        end_date = request.GET.get('reg_end_date')
        
        if start_date:
            try:
                from datetime import datetime
                # Parse YYYY-MM-DD from date input
                start_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
                qs = qs.filter(registration_date__gte=start_obj)
            except:
                pass
        
        if end_date:
            try:
                from datetime import datetime
                # Parse YYYY-MM-DD from date input
                end_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
                qs = qs.filter(registration_date__lte=end_obj)
            except:
                pass
        
        return qs
    
    def save_model(self, request, obj, form, change):
        if not change:
            # Creating a new taxpayer - ensure it's marked as primary license
            obj.is_primary_license = True
        super().save_model(request, obj, form, change)


@admin.register(MultipleLicenseReference)
class MultipleLicenseAdmin(admin.ModelAdmin):
    """Admin for Secondary Licenses - separate section for reference purposes"""
    list_display = ['gstin', 'display_ramis_tpn', 'taxpayer_name', 'business_name', 'cid_company_reg_no', 'sector', 'sub_sector', 'business_activity', 'dzongkhag', 'status', 'display_registration_date', 'display_commencement_date', 'display_deregistration_date', 'email_address', 'mobile_number', 'display_business_address', 'remarks']
    list_display_links = ['gstin', 'taxpayer_name']
    list_filter = ['dzongkhag', 'status', 'registration_date']
    search_fields = ['gstin', 'license_number', 'taxpayer_name', 'business_name', 'cid_company_reg_no', 'ramis_tpn']
    list_per_page = 20  # Show 20 records per page with pagination
    show_full_result_count = False  # Hide filter counts
    
    search_help_text = 'Search by GSTIN to see all related licenses for that taxpayer.'
    
    def display_ramis_tpn(self, obj):
        """Display RAMIS TPN as the license number with proper heading"""
        return obj.license_number
    display_ramis_tpn.short_description = 'RAMIS TPN'
    
    def display_registration_date(self, obj):
        """Display registration date in dd-mm-yyyy format with leading zeros"""
        if obj.registration_date:
            return obj.registration_date.strftime('%d-%m-%Y')
        return '-'
    display_registration_date.short_description = 'Registration Date'
    
    def display_commencement_date(self, obj):
        """Display commencement date in dd-mm-yyyy format with leading zeros"""
        if obj.commencement_date:
            return obj.commencement_date.strftime('%d-%m-%Y')
        return '-'
    display_commencement_date.short_description = 'Commencement Date'
    
    def display_deregistration_date(self, obj):
        """Display deregistration date in dd-mm-yyyy format with leading zeros"""
        if obj.deregistration_date:
            return obj.deregistration_date.strftime('%d-%m-%Y')
        return '-'
    display_deregistration_date.short_description = 'Deregistration/Region Transfer Date'
    
    def display_business_address(self, obj):
        """Display full business address with proper formatting"""
        if obj.business_address:
            return obj.business_address
        return '-'
    display_business_address.short_description = 'Business Address'
    display_business_address.allow_tags = True


class TaxpayerEnquiryForm(forms.ModelForm):
    """Custom form for Taxpayer Enquiry with auto-fetch and conditional fields"""
    class Meta:
        model = TaxpayerEnquiry
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set initial values for dropdowns
        ENQUIRY_STATUS = [
            ('Pending Taxpayer', 'Pending Taxpayer'),
            ('Pending Officer', 'Pending Officer'),
            ('Referred', 'Referred'),
            ('Resolved', 'Resolved'),
            ('Closed', 'Closed'),
        ]
        
        ENQUIRY_TYPE = [
            ('Taxpayer Enquiry', 'Taxpayer Enquiry'),
            ('General Correspondence', 'General Correspondence'),
            ('Notice', 'Notice'),
            ('Assessment', 'Assessment'),
            ('Audit', 'Audit'),
            ('Refund', 'Refund'),
            ('ITC', 'ITC'),
            ('Registration', 'Registration'),
            ('Payment', 'Payment'),
            ('Return Filing', 'Return Filing'),
            ('Other', 'Other'),
        ]
        
        ENQUIRY_MODE = [
            ('Letter', 'Letter'),
            ('Email', 'Email'),
            ('Phone', 'Phone'),
            ('In Person', 'In Person'),
            ('BITs', 'BITs'),
            ('Official Letter', 'Official Letter'),
            ('Social Media', 'Social Media'),
            ('Other', 'Other'),
        ]
        
        if 'status' in self.fields:
            self.fields['status'].choices = ENQUIRY_STATUS
            self.fields['status'].required = False
            self.fields['status'].empty_label = None
        
        if 'enquiry_type' in self.fields:
            self.fields['enquiry_type'].choices = ENQUIRY_TYPE
            self.fields['enquiry_type'].required = False
            self.fields['enquiry_type'].empty_label = None
        
        if 'mode' in self.fields:
            self.fields['mode'].choices = ENQUIRY_MODE
            self.fields['mode'].required = False
            self.fields['mode'].empty_label = None
        
        # Make conditional fields optional initially
        if 'social_media_details' in self.fields:
            self.fields['social_media_details'].required = False
        if 'other_details' in self.fields:
            self.fields['other_details'].required = False
        
        # Add date widget for enquiry_date and resolved_date
        if 'enquiry_date' in self.fields:
            self.fields['enquiry_date'].widget = CustomDateInput()
            # Set initial value if instance exists and has date
            if self.instance and getattr(self.instance, 'enquiry_date'):
                from datetime import datetime
                date_value = getattr(self.instance, 'enquiry_date')
                if date_value:
                    formatted_date = date_value.strftime('%Y-%m-%d')
                    self.fields['enquiry_date'].initial = formatted_date
        if 'resolved_date' in self.fields:
            self.fields['resolved_date'].widget = CustomDateInput()
            # Set initial value if instance exists and has date
            if self.instance and getattr(self.instance, 'resolved_date'):
                from datetime import datetime
                date_value = getattr(self.instance, 'resolved_date')
                if date_value:
                    formatted_date = date_value.strftime('%Y-%m-%d')
                    self.fields['resolved_date'].initial = formatted_date
        
        # Fix officer dropdown to show only name instead of email
        if 'assigned_to' in self.fields:
            self.fields['assigned_to'].queryset = self.fields['assigned_to'].queryset
            self.fields['assigned_to'].label_from_instance = lambda obj: obj.get_full_name() if obj else ''


@admin.register(TaxpayerEnquiry)
class TaxpayerEnquiryAdmin(admin.ModelAdmin):
    """Admin for Taxpayer Enquiries - independent section"""
    form = TaxpayerEnquiryForm
    change_form_template = 'taxpayers/taxpayer_enquiry_change_form.html'
    list_display = ['enquiry_id', 'display_enquiry_date', 'gstin', 'taxpayer_name', 'enquiry_type', 'subject', 'received_from_sent_to', 'action_response', 'status', 'assigned_to', 'remarks']
    list_display_links = ['enquiry_id', 'subject']
    list_filter = ['enquiry_type', 'status', 'mode', 'enquiry_date', 'assigned_to']
    search_fields = ['enquiry_id', 'subject', 'gstin', 'taxpayer_name', 'received_from_sent_to']
    list_per_page = 20  # Show 20 records per page with pagination
    date_hierarchy = 'enquiry_date'
    
    fieldsets = (
        ('Enquiry Details', {
            'fields': ('enquiry_id', 'enquiry_date', 'enquiry_type', 'subject', 'mode', 'social_media_details', 'other_details')
        }),
        ('Taxpayer Information', {
            'fields': ('gstin', 'taxpayer_name', 'cid_company_reg_no')
        }),
        ('Contact Information', {
            'fields': ('received_from_sent_to', 'contact_person', 'email_address', 'mobile_number')
        }),
        ('Status & Assignment', {
            'fields': ('status', 'assigned_to', 'priority')
        }),
        ('Action & Resolution', {
            'fields': ('action_response', 'resolution_notes', 'resolved_date', 'remarks')
        }),
    )
    
    readonly_fields = []  # No readonly fields, enquiry_id and dates are now editable
    
    def display_enquiry_date(self, obj):
        """Display enquiry date in dd-mm-yyyy format with leading zeros"""
        if obj.enquiry_date:
            return obj.enquiry_date.strftime('%d-%m-%Y')
        return '-'
    display_enquiry_date.short_description = 'Date'
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.assigned_to = request.user
        super().save_model(request, obj, form, change)