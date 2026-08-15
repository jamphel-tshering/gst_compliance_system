from django.contrib import admin
from django.db.models import Count, Q, Sum
from django.utils import timezone
from django.shortcuts import render, redirect
from django.urls import reverse
from django.forms import DateInput, ModelChoiceField, CharField, ChoiceField
from django import forms
from datetime import datetime
from .models import AuditCase, AuditAssessment, AuditFinding, RefundRegister
from core.models import User
from core.form_widgets import CustomDateInput, TaxPeriodSelect
from taxpayers.models import TaxpayerMaster





# Custom form for AuditAssessment with tax period dropdown
class AuditAssessmentForm(forms.ModelForm):
    class Meta:
        model = AuditAssessment
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
        ]
        
        if 'tax_period' in self.fields:
            self.fields['tax_period'].widget = TaxPeriodSelect()
            self.fields['tax_period'].required = True
            self.fields['tax_period'].empty_label = None
        
        # Add date widgets with text input to avoid Django validation
        date_fields = ['assessment_date', 'case_closed_date', 'assigned_date', 'due_date']
        for field in date_fields:
            if field in self.fields:
                self.fields[field].widget = forms.TextInput(attrs={
                    'type': 'text',
                    'placeholder': 'DD-MM-YYYY',
                    'pattern': r'\d{2}-\d{2}-\d{4}'
                })
        
        # Filter officer dropdown to show only staff users
        if 'assigned_officer' in self.fields:
            self.fields['assigned_officer'].queryset = User.objects.filter(is_staff=True)
            self.fields['assigned_officer'].required = False
            self.fields['assigned_officer'].empty_label = "Select Officer"
        
        if 'assigned_by' in self.fields:
            self.fields['assigned_by'].queryset = User.objects.filter(is_staff=True)
            self.fields['assigned_by'].required = False
            self.fields['assigned_by'].empty_label = "Select Assigner"
        
        if 'assessor' in self.fields:
            self.fields['assessor'].queryset = User.objects.filter(is_staff=True)
            self.fields['assessor'].required = False
            self.fields['assessor'].empty_label = "Select Assessor"
    
    def clean_assessment_date(self):
        """Validate DD-MM-YYYY format"""
        date_str = self.cleaned_data.get('assessment_date')
        if date_str:
            try:
                datetime.strptime(date_str, '%d-%m-%Y')
            except ValueError:
                raise forms.ValidationError('Enter a valid date in DD-MM-YYYY format (e.g., 15-08-2026)')
        return date_str
    
    def clean_case_closed_date(self):
        """Validate DD-MM-YYYY format"""
        date_str = self.cleaned_data.get('case_closed_date')
        if date_str:
            try:
                datetime.strptime(date_str, '%d-%m-%Y')
            except ValueError:
                raise forms.ValidationError('Enter a valid date in DD-MM-YYYY format (e.g., 15-08-2026)')
        return date_str
    
    def clean_assigned_date(self):
        """Validate DD-MM-YYYY format"""
        date_str = self.cleaned_data.get('assigned_date')
        if date_str:
            try:
                datetime.strptime(date_str, '%d-%m-%Y')
            except ValueError:
                raise forms.ValidationError('Enter a valid date in DD-MM-YYYY format (e.g., 15-08-2026)')
        return date_str
    
    def clean_due_date(self):
        """Validate DD-MM-YYYY format"""
        date_str = self.cleaned_data.get('due_date')
        if date_str:
            try:
                datetime.strptime(date_str, '%d-%m-%Y')
            except ValueError:
                raise forms.ValidationError('Enter a valid date in DD-MM-YYYY format (e.g., 15-08-2026)')
        return date_str


# Custom form for AuditCase with tax period dropdowns
class AuditCaseForm(forms.ModelForm):
    class Meta:
        model = AuditCase
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
        ]
        
        period_fields = ['from_tax_period', 'to_tax_period']
        for field in period_fields:
            if field in self.fields:
                self.fields[field].widget = TaxPeriodSelect()
                self.fields[field].required = True
                self.fields[field].empty_label = '---'
        
        # Add date widgets with text input to avoid Django validation
        date_fields = ['assessment_date', 'case_closed_date', 'assigned_date', 'due_date']
        for field in date_fields:
            if field in self.fields:
                self.fields[field].widget = forms.TextInput(attrs={
                    'type': 'text',
                    'placeholder': 'DD-MM-YYYY',
                    'pattern': r'\d{2}-\d{2}-\d{4}'
                })
        
        # Filter officer dropdown to show only staff users
        if 'assigned_officer' in self.fields:
            self.fields['assigned_officer'].queryset = User.objects.filter(is_staff=True)
            self.fields['assigned_officer'].required = False
            self.fields['assigned_officer'].empty_label = "Select Officer"
        
        if 'assigned_by' in self.fields:
            self.fields['assigned_by'].queryset = User.objects.filter(is_staff=True)
            self.fields['assigned_by'].required = False
            self.fields['assigned_by'].empty_label = "Select Assigner"
        
        if 'assessor' in self.fields:
            self.fields['assessor'].queryset = User.objects.filter(is_staff=True)
            self.fields['assessor'].required = False
            self.fields['assessor'].empty_label = "Select Assessor"
    
    def clean_assessment_date(self):
        """Validate DD-MM-YYYY format"""
        date_str = self.cleaned_data.get('assessment_date')
        if date_str:
            try:
                datetime.strptime(date_str, '%d-%m-%Y')
            except ValueError:
                raise forms.ValidationError('Enter a valid date in DD-MM-YYYY format (e.g., 15-08-2026)')
        return date_str
    
    def clean_case_closed_date(self):
        """Validate DD-MM-YYYY format"""
        date_str = self.cleaned_data.get('case_closed_date')
        if date_str:
            try:
                datetime.strptime(date_str, '%d-%m-%Y')
            except ValueError:
                raise forms.ValidationError('Enter a valid date in DD-MM-YYYY format (e.g., 15-08-2026)')
        return date_str
    
    def clean_assigned_date(self):
        """Validate DD-MM-YYYY format"""
        date_str = self.cleaned_data.get('assigned_date')
        if date_str:
            try:
                datetime.strptime(date_str, '%d-%m-%Y')
            except ValueError:
                raise forms.ValidationError('Enter a valid date in DD-MM-YYYY format (e.g., 15-08-2026)')
        return date_str
    
    def clean_due_date(self):
        """Validate DD-MM-YYYY format"""
        date_str = self.cleaned_data.get('due_date')
        if date_str:
            try:
                datetime.strptime(date_str, '%d-%m-%Y')
            except ValueError:
                raise forms.ValidationError('Enter a valid date in DD-MM-YYYY format (e.g., 15-08-2026)')
        return date_str


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


# Dashboard view for Audit & Refund module
def audit_refund_dashboard(request):
    """Main dashboard for Audit & Refund module"""
    
    # Import RefundRegister here to avoid circular import
    from .models import RefundRegister
    
    # Audit Statistics
    total_audit_cases = AuditCase.objects.count()
    pending_assignment = AuditCase.objects.filter(status='pending_assignment').count()
    assigned = AuditCase.objects.filter(status='assigned').count()
    in_progress = AuditCase.objects.filter(status='in_progress').count()
    completed = AuditCase.objects.filter(status='completed').count()
    closed = AuditCase.objects.filter(status='closed').count()
    
    # Refund Statistics
    total_refunds = RefundRegister.objects.count()
    pending_refunds = RefundRegister.objects.filter(status='submitted').count()
    under_review_refunds = RefundRegister.objects.filter(status='under_review').count()
    approved_refunds = RefundRegister.objects.filter(status='approved').count()
    rejected_refunds = RefundRegister.objects.filter(status='rejected').count()
    paid_refunds = RefundRegister.objects.filter(status='paid').count()
    
    context = {
        'title': 'Audit & Refund Module',
        'subtitle': 'Audit & Refund Management',
        # Audit statistics
        'total_audit_cases': total_audit_cases,
        'pending_assignment': pending_assignment,
        'assigned': assigned,
        'in_progress': in_progress,
        'completed': completed,
        'closed': closed,
        # Refund statistics
        'total_refunds': total_refunds,
        'pending_refunds': pending_refunds,
        'under_review_refunds': under_review_refunds,
        'approved_refunds': approved_refunds,
        'rejected_refunds': rejected_refunds,
        'paid_refunds': paid_refunds,
        # URLs
        'audit_cases_url': reverse('admin:audit_refund_auditcase_changelist'),
        'audit_assessments_url': reverse('admin:audit_refund_auditassessment_changelist'),
        'audit_findings_url': reverse('admin:audit_refund_auditfinding_changelist'),
        'refunds_url': reverse('admin:audit_refund_refundregister_changelist'),
    }
    
    return render(request, 'audit_refund/admin_dashboard.html', context)


@admin.register(AuditCase)
class AuditCaseAdmin(admin.ModelAdmin):
    """Admin for Audit Cases"""
    form = AuditCaseForm
    change_form_template = 'admin/audit_case_change_form.html'
    list_display = ['audit_case_id', 'risk_referral', 'gstin', 'taxpayer_name', 'assessment_type', 'assigned_officer', 'status', 'due_date']
    list_filter = ['status', 'assessment_type', 'audit_priority', 'assigned_officer', 'from_tax_period']
    search_fields = ['audit_case_id', 'gstin', 'taxpayer_name', 'risk_referral__risk_id', 'remarks', 'assigned_officer__username', 'assessor__username']
    
    # Remove raw_id_fields to enable regular dropdown lookups
    # raw_id_fields = ['risk_referral', 'assigned_officer', 'assigned_by', 'assessor']
    
    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(request, queryset, search_term)
        # Additional search logic if needed
        return queryset, may_have_duplicates
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.__class__.__name__ in ['DateField', 'DateTimeField']:
            kwargs['widget'] = CustomDateInput()
        return super().formfield_for_dbfield(db_field, **kwargs)
    
    def save_model(self, request, obj, form, change):
        # Convert date strings to display format if needed
        date_fields = ['assessment_date', 'case_closed_date', 'assigned_date', 'due_date']
        for field in date_fields:
            date_value = getattr(obj, field, None)
            if date_value and isinstance(date_value, str):
                try:
                    datetime.strptime(date_value, '%d-%m-%Y')
                except ValueError:
                    pass  # Keep as is if conversion fails
        
        # Auto-fetch taxpayer information if GSTIN provided
        if obj.gstin and not obj.taxpayer_name:
            taxpayer = TaxpayerMaster.objects.filter(gstin=obj.gstin, is_primary_license=True).first()
            if taxpayer:
                obj.taxpayer_name = taxpayer.taxpayer_name
                obj.dzongkhag = taxpayer.dzongkhag
                obj.organisation_type = taxpayer.organisation_type
                obj.frequency = taxpayer.frequency
        
        super().save_model(request, obj, form, change)
    

    
    # Use raw_id_fields to avoid dropdown decimal conversion issues
    raw_id_fields = ['risk_referral', 'assigned_officer', 'assigned_by', 'assessor']
    
    fieldsets = (
        ('Case Information', {
            'fields': ('audit_case_id', 'risk_referral', 'assessment_date', 'from_tax_period', 'to_tax_period', 'gstin', 'taxpayer_name', 'dzongkhag', 'organisation_type', 'frequency', 'assessment_type', 'audit_priority')
        }),
        ('Assignment', {
            'fields': ('assigned_officer', 'assigned_by', 'assigned_date', 'due_date')
        }),
        ('Status', {
            'fields': ('status', 'case_closed_date', 'assessment_duration')
        }),
        ('Assessor', {
            'fields': ('assessor',)
        }),
        ('Remarks', {
            'fields': ('remarks',)
        }),
    )
    
    readonly_fields = ['audit_case_id', 'assessment_date', 'from_tax_period', 'to_tax_period', 'gstin', 'taxpayer_name', 'dzongkhag', 'organisation_type', 'frequency', 'assessor']
    
    def save_model(self, request, obj, form, change):
        if not change:
            # Auto-generate audit case ID
            last_case = AuditCase.objects.order_by('-id').first()
            if last_case and last_case.audit_case_id:
                try:
                    last_num = int(last_case.audit_case_id.split('-')[-1])
                    obj.audit_case_id = f"AC-{timezone.now().year}-{last_num + 1:04d}"
                except:
                    obj.audit_case_id = f"AC-{timezone.now().year}-0001"
            else:
                obj.audit_case_id = f"AC-{timezone.now().year}-0001"
            
            # Auto-set assessor from risk referral
            if obj.risk_referral and obj.risk_referral.assessor:
                obj.assessor = obj.risk_referral.assessor
            
            # Auto-set assignment date if officer is assigned
            if obj.assigned_officer and not obj.assigned_date:
                obj.assigned_date = timezone.now()
                obj.assigned_by = request.user
                obj.status = 'assigned'
        
        super().save_model(request, obj, form, change)


@admin.register(AuditAssessment)
class AuditAssessmentAdmin(admin.ModelAdmin):
    """Admin for Audit Assessments"""
    form = AuditAssessmentForm
    change_form_template = 'admin/audit_assessment_change_form.html'
    list_display = ['asc_no', 'audit_case', 'gstin', 'taxpayer_name', 'assessment_type', 'assessment_outcome', 'status', 'assessor']
    list_filter = ['assessment_type', 'assessment_outcome', 'status']
    search_fields = ['asc_no', 'gstin', 'taxpayer_name', 'audit_case__audit_case_id']
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.__class__.__name__ in ['DateField', 'DateTimeField']:
            kwargs['widget'] = CustomDateInput()
        return super().formfield_for_dbfield(db_field, **kwargs)
    
    def save_model(self, request, obj, form, change):
        # Convert date strings to display format if needed
        date_fields = ['assessment_date', 'case_closed_date']
        for field in date_fields:
            date_value = getattr(obj, field, None)
            if date_value and isinstance(date_value, str):
                try:
                    datetime.strptime(date_value, '%d-%m-%Y')
                except ValueError:
                    pass  # Keep as is if conversion fails
        
        # Auto-fetch taxpayer information if GSTIN provided
        if obj.gstin and not obj.taxpayer_name:
            taxpayer = TaxpayerMaster.objects.filter(gstin=obj.gstin, is_primary_license=True).first()
            if taxpayer:
                obj.taxpayer_name = taxpayer.taxpayer_name
                obj.dzongkhag = taxpayer.dzongkhag
                obj.organisation_type = taxpayer.organisation_type
                obj.frequency = taxpayer.frequency
        
        super().save_model(request, obj, form, change)
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        # Auto-populate taxpayer information from Audit Case when editing
        if obj and obj.audit_case:
            # Pre-fill fields from audit case if they're empty
            if not obj.gstin:
                form.base_fields['gstin'].initial = obj.audit_case.gstin
            if not obj.taxpayer_name:
                form.base_fields['taxpayer_name'].initial = obj.audit_case.taxpayer_name
            if not obj.dzongkhag:
                form.base_fields['dzongkhag'].initial = obj.audit_case.dzongkhag
            if not obj.organisation_type:
                form.base_fields['organisation_type'].initial = obj.audit_case.organisation_type
            if not obj.frequency:
                form.base_fields['frequency'].initial = obj.audit_case.frequency
            if not obj.assessment_type:
                form.base_fields['assessment_type'].initial = obj.audit_case.assessment_type
            if not obj.tax_period:
                form.base_fields['tax_period'].initial = obj.audit_case.from_tax_period
        
        return form
    
    def save_model(self, request, obj, form, change):
        # Convert date strings to display format if needed
        date_fields = ['assessment_date', 'case_closed_date']
        for field in date_fields:
            date_value = getattr(obj, field, None)
            if date_value and isinstance(date_value, str):
                try:
                    datetime.strptime(date_value, '%d-%m-%Y')
                except ValueError:
                    pass  # Keep as is if conversion fails
        
        if not change:
            # Auto-populate from Audit Case when creating new assessment
            if obj.audit_case:
                # Only populate if fields are empty
                if not obj.gstin:
                    obj.gstin = obj.audit_case.gstin
                if not obj.taxpayer_name:
                    obj.taxpayer_name = obj.audit_case.taxpayer_name
                if not obj.dzongkhag:
                    obj.dzongkhag = obj.audit_case.dzongkhag
                if not obj.organisation_type:
                    obj.organisation_type = obj.audit_case.organisation_type
                if not obj.frequency:
                    obj.frequency = obj.audit_case.frequency
                if not obj.assessment_type:
                    obj.assessment_type = obj.audit_case.assessment_type
                if not obj.tax_period:
                    obj.tax_period = obj.audit_case.from_tax_period
                
                # Auto-set assessor from audit case
                if obj.audit_case.assessor:
                    obj.assessor = obj.audit_case.assessor
            
            # Auto-generate ASC number
            last_assessment = AuditAssessment.objects.order_by('-id').first()
            if last_assessment and last_assessment.asc_no:
                last_num = int(last_assessment.asc_no.split('-')[-1])
                obj.asc_no = f"ASC-{timezone.now().year}-{last_num + 1:04d}"
            else:
                obj.asc_no = f"ASC-{timezone.now().year}-0001"
        
        # Auto-fetch taxpayer information if GSTIN provided
        if obj.gstin and not obj.taxpayer_name:
            taxpayer = TaxpayerMaster.objects.filter(gstin=obj.gstin, is_primary_license=True).first()
            if taxpayer:
                obj.taxpayer_name = taxpayer.taxpayer_name
                obj.dzongkhag = taxpayer.dzongkhag
                obj.organisation_type = taxpayer.organisation_type
                obj.frequency = taxpayer.frequency
        
        # Calculate variation if both values are present
        if obj.gst_payable_refundable_assessed and obj.gst_payable_refundable_return:
            obj.variation = obj.gst_payable_refundable_assessed - obj.gst_payable_refundable_return
            if obj.gst_payable_refundable_return != 0:
                obj.variation_percentage = (obj.variation / obj.gst_payable_refundable_return) * 100
        
        super().save_model(request, obj, form, change)
    
    fieldsets = (
        ('Case Information', {
            'fields': ('audit_case', 'asc_no', 'assessment_date', 'tax_period', 'gstin', 'taxpayer_name', 'dzongkhag', 'organisation_type', 'frequency', 'assessment_type')
        }),
        ('GST Return Information (Read-Only)', {
            'fields': ('gst_return', 'declared_sales', 'gst_on_declared_sales', 'declared_import_value', 'gst_on_declared_import', 'declared_domestic_purchase', 'gst_on_declared_domestic_purchase', 'itc', 'gst_payable_refundable_return', 'actual_payment'),
            'classes': ('collapse',)
        }),
        ('Assessed Information', {
            'fields': ('assessed_sales_turnover', 'actual_import_value_ecms', 'assessed_import_value', 'gst_on_assessed_import', 'assessed_domestic_purchase', 'gst_on_assessed_domestic_purchase', 'gst_payable_refundable_assessed')
        }),
        ('Calculations', {
            'fields': ('variation', 'variation_percentage')
        }),
        ('Findings', {
            'fields': ('reason_code', 'discrepancy')
        }),
        ('Outcome', {
            'fields': ('assessment_outcome', 'action_taken')
        }),
        ('Status', {
            'fields': ('status', 'case_closed_date', 'assessment_duration')
        }),
        ('Assessor', {
            'fields': ('assessor',)
        }),
    )
    
    readonly_fields = ['gst_return', 'declared_sales', 'gst_on_declared_sales', 'declared_import_value', 'gst_on_declared_import', 'declared_domestic_purchase', 'gst_on_declared_domestic_purchase', 'itc', 'gst_payable_refundable_return', 'actual_payment', 'variation', 'variation_percentage']


@admin.register(AuditFinding)
class AuditFindingAdmin(admin.ModelAdmin):
    """Admin for Audit Findings"""
    change_form_template = 'admin/audit_finding_change_form.html'
    list_display = ['finding_id', 'audit_case', 'finding_type', 'amount_involved', 'action_taken']
    list_filter = ['finding_type', 'audit_case']
    search_fields = ['finding_id', 'audit_case__audit_case_id', 'discrepancy']
    
    # Use raw_id_fields to avoid dropdown decimal conversion issues
    raw_id_fields = ['audit_case']
    
    fieldsets = (
        ('Finding Information', {
            'fields': ('finding_id', 'audit_case', 'reason_code', 'finding_type', 'discrepancy', 'amount_involved', 'description', 'action_taken', 'auditor_remarks')
        }),
    )
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.__class__.__name__ in ['DateField', 'DateTimeField']:
            kwargs['widget'] = CustomDateInput()
        return super().formfield_for_dbfield(db_field, **kwargs)
    
    def save_model(self, request, obj, form, change):
        if not change:
            # Auto-generate finding ID
            last_finding = AuditFinding.objects.order_by('-id').first()
            if last_finding and last_finding.finding_id:
                last_num = int(last_finding.finding_id.split('-')[-1])
                obj.finding_id = f"FD-{timezone.now().year}-{last_num + 1:04d}"
            else:
                obj.finding_id = f"FD-{timezone.now().year}-0001"
        
        super().save_model(request, obj, form, change)


@admin.register(RefundRegister)
class RefundRegisterAdmin(admin.ModelAdmin):
    """Admin for Refund Register - now under Audit & Refund Module"""
    list_display = ['refund_id', 'gst_tpn', 'taxpayer_name', 'tax_period', 'claimed_amount', 'refund_approved', 'display_status', 'claim_date']
    list_filter = ['status', 'claim_date', 'tax_period']
    search_fields = ['refund_id', 'gst_tpn', 'taxpayer_name']
    ordering = ['-claim_date']
    readonly_fields = ['created_at', 'updated_at', 'refund_adjustment_percentage', 'processing_days']
    
    # Use raw_id_fields to avoid dropdown decimal conversion issues
    raw_id_fields = ['gst_return', 'risk_referral', 'audit_case', 'created_by', 'updated_by']
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.__class__.__name__ in ['DateField', 'DateTimeField']:
            kwargs['widget'] = CustomDateInput()
        return super().formfield_for_dbfield(db_field, **kwargs)
    
    def save_model(self, request, obj, form, change):
        # Convert date strings to display format if needed
        date_fields = ['assessment_date', 'case_closed_date', 'assigned_date', 'due_date']
        for field in date_fields:
            date_value = getattr(obj, field, None)
            if date_value and isinstance(date_value, str):
                try:
                    datetime.strptime(date_value, '%d-%m-%Y')
                except ValueError:
                    pass  # Keep as is if conversion fails
        
        # Auto-fetch taxpayer information if GSTIN provided
        if obj.gstin and not obj.taxpayer_name:
            taxpayer = TaxpayerMaster.objects.filter(gstin=obj.gstin, is_primary_license=True).first()
            if taxpayer:
                obj.taxpayer_name = taxpayer.taxpayer_name
                obj.dzongkhag = taxpayer.dzongkhag
                obj.organisation_type = taxpayer.organisation_type
                obj.frequency = taxpayer.frequency
        
        super().save_model(request, obj, form, change)
    

    
    def display_status(self, obj):
        return get_display_value(obj, 'status')
    display_status.short_description = 'Status'
    
    def save_model(self, request, obj, form, change):
        # Calculate refund approved
        obj.refund_approved = obj.claimed_amount - obj.adjustment - obj.refund_disallowed
        
        # Calculate refund adjustment percentage
        if obj.claimed_amount and obj.claimed_amount > 0:
            obj.refund_adjustment_percentage = ((obj.adjustment + obj.refund_disallowed) / obj.claimed_amount) * 100
        
        # Calculate processing days
        if obj.processed_date and obj.claim_date:
            obj.processing_days = (obj.processed_date - obj.claim_date).days
        
        super().save_model(request, obj, form, change)
    
    fieldsets = (
        ('Identification', {
            'fields': ('refund_id', 'gst_tpn', 'taxpayer_name')
        }),
        ('Period and Claim Details', {
            'fields': ('tax_period', 'claim_date', 'claimed_amount')
        }),
        ('References', {
            'fields': ('gst_return', 'risk_referral', 'audit_case')
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