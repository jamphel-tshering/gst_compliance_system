from django.contrib import admin, messages
from django.db.models import Count, Q, Sum
from django import forms
from django.forms import DateInput, ModelChoiceField
from django.utils import timezone
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import ComplianceMonitoring, ComplianceRiskReferral, EnforcementRecovery
from returns.models import GSTReturn
from taxpayers.models import TaxpayerMaster
from core.models import User


# Custom date input widget for dd-mm-yyyy format
class CustomDateInput(DateInput):
    input_type = 'date'
    def __init__(self, attrs=None):
        default_attrs = {'type': 'date'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)


# Dashboard view for Compliance & Enforcement module
def compliance_enforcement_dashboard(request):
    """Main dashboard for Compliance & Enforcement module"""
    
    # Compliance Monitoring Statistics
    total_monitored = ComplianceMonitoring.objects.count()
    compliant_count = ComplianceMonitoring.objects.filter(compliance_status='Compliant').count()
    late_filer_count = ComplianceMonitoring.objects.filter(compliance_status='Late Filer').count()
    non_filer_count = ComplianceMonitoring.objects.filter(compliance_status='Non-Filer').count()
    payment_default_count = ComplianceMonitoring.objects.filter(compliance_status='Payment Default').count()
    
    # Compliance Risk & Referral Statistics
    total_risk_assessments = ComplianceRiskReferral.objects.count()
    audit_selected = ComplianceRiskReferral.objects.filter(system_decision='AUDIT').count()
    review_selected = ComplianceRiskReferral.objects.filter(system_decision='REVIEW').count()
    monitor_selected = ComplianceRiskReferral.objects.filter(system_decision='MONITOR').count()
    
    # Enforcement & Recovery Statistics
    total_enforcement_cases = EnforcementRecovery.objects.count()
    open_cases = EnforcementRecovery.objects.filter(status='Open').count()
    recovered_cases = EnforcementRecovery.objects.filter(status='Recovered').count()
    
    context = {
        'title': 'Compliance & Enforcement Module',
        'subtitle': 'Compliance & Enforcement Management',
        # Compliance Monitoring statistics
        'total_monitored': total_monitored,
        'compliant_count': compliant_count,
        'late_filer_count': late_filer_count,
        'non_filer_count': non_filer_count,
        'payment_default_count': payment_default_count,
        # Compliance Risk & Referral statistics
        'total_risk_assessments': total_risk_assessments,
        'audit_selected': audit_selected,
        'review_selected': review_selected,
        'monitor_selected': monitor_selected,
        # Enforcement & Recovery statistics
        'total_enforcement_cases': total_enforcement_cases,
        'open_cases': open_cases,
        'recovered_cases': recovered_cases,
        # URLs
        'compliance_monitoring_url': reverse('admin:compliance_compliancemonitoring_changelist'),
        'compliance_risk_referral_url': reverse('admin:compliance_complianceriskreferral_changelist'),
        'enforcement_recovery_url': reverse('admin:compliance_enforcementrecovery_changelist'),
        'risk_assessment_dashboard_url': '/compliance/compliance_risk_dashboard/',
    }
    
    return render(request, 'compliance/admin_dashboard.html', context)


class CustomDateInput(DateInput):
    """Custom date input with calendar picker"""
    input_type = 'date'
    
    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        attrs.update({
            'class': 'vDateField',
            'type': 'date',
        })
        super().__init__(attrs=attrs)


class ComplianceMonitoringForm(forms.ModelForm):
    """Custom form with date pickers"""
    class Meta:
        model = ComplianceMonitoring
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
            self.fields['tax_period'].empty_label = None


@admin.register(ComplianceMonitoring)
class ComplianceMonitoringAdmin(admin.ModelAdmin):
    """Admin for Compliance Monitoring"""
    list_display = ['monitoring_id', 'gstin', 'taxpayer_name', 'tax_period', 'filing_status', 'payment_status', 'risk_level', 'created_at']
    list_filter = ['filing_status', 'payment_status', 'risk_level', 'tax_period', 'created_at']
    search_fields = ['monitoring_id', 'gstin', 'taxpayer_name']
    date_hierarchy = 'created_at'
    
    def changelist_view(self, request, extra_context=None):
        # Add dashboard link to changelist view
        extra_context = extra_context or {}
        extra_context['show_dashboard_link'] = True
        extra_context['dashboard_url'] = '/admin/dashboard/'
        extra_context['dashboard_title'] = 'Main Dashboard'
        return super().changelist_view(request, extra_context)
    """Admin for Compliance & Enforcement - Simple table based on GST Returns"""
    form = ComplianceMonitoringForm
    list_display = ['compliance_id', 'tax_period', 'gstin', 'taxpayer_name', 'filing_status', 'filing_delay', 'payment_status', 'compliance_status', 'compliance_flag', 'remarks']
    list_display_links = ['compliance_id', 'gstin']
    list_filter = ['tax_period', 'filing_status', 'payment_status', 'compliance_status', 'compliance_flag']
    search_fields = ['compliance_id', 'gstin', 'taxpayer_name']
    list_per_page = 20
    date_hierarchy = 'assessment_date'
    
    def changelist_view(self, request, extra_context=None):
        # Redirect to dashboard when accessing the root of compliance
        if request.path == '/admin/compliance/':
            return compliance_enforcement_dashboard(request)
        return super().changelist_view(request, extra_context)
    
    fieldsets = (
        ('Assessment Information', {
            'fields': ('compliance_id', 'tax_period', 'assessment_date')
        }),
        ('Taxpayer Information', {
            'fields': ('gstin', 'taxpayer_name')
        }),
        ('Compliance Details', {
            'fields': ('filing_status', 'filing_delay', 'payment_status', 'compliance_status', 'compliance_flag')
        }),
        ('Additional Information', {
            'fields': ('remarks',)
        }),
    )
    
    readonly_fields = ['compliance_id', 'assessment_date']
    
    actions = ['auto_populate_from_returns', 'recalculate_compliance_status']
    
    def changelist_view(self, request, extra_context=None):
        """Override to show Compliance & Enforcement dashboard"""
        response = super().changelist_view(request, extra_context)
        
        # Calculate compliance statistics
        queryset = self.get_queryset(request)
        total_monitored = queryset.count()
        compliant_count = queryset.filter(compliance_status='Compliant').count()
        late_filer_count = queryset.filter(compliance_status='Late Filer').count()
        non_filer_count = queryset.filter(compliance_status='Non-Filer').count()
        payment_default_count = queryset.filter(compliance_status='Payment Default').count()
        other_non_compliance_count = queryset.filter(compliance_status='Other Non-Compliance').count()
        
        # Compliance flag breakdown
        green_count = queryset.filter(compliance_flag='Green').count()
        yellow_count = queryset.filter(compliance_flag='Yellow').count()
        red_count = queryset.filter(compliance_flag='Red').count()
        
        # Add to context
        extra_context = extra_context or {}
        extra_context.update({
            'total_monitored': total_monitored,
            'compliant_count': compliant_count,
            'late_filer_count': late_filer_count,
            'non_filer_count': non_filer_count,
            'payment_default_count': payment_default_count,
            'other_non_compliance_count': other_non_compliance_count,
            'green_count': green_count,
            'yellow_count': yellow_count,
            'red_count': red_count,
        })
        
        return response
    
    def auto_populate_from_returns(self, request, queryset):
        """Auto-populate compliance from GST Returns"""
        count = 0
        for gst_return in GSTReturn.objects.all():
            # Check if compliance record already exists
            existing = ComplianceMonitoring.objects.filter(
                gstin=gst_return.gstin,
                tax_period=gst_return.tax_period
            ).first()
            
            if not existing:
                # Determine compliance status based on GST return
                compliance_status = 'Compliant'
                compliance_flag = 'Green'
                
                if gst_return.filing_status == 'Overdue / Non-Filer':
                    compliance_status = 'Non-Filer'
                    compliance_flag = 'Red'
                elif gst_return.filing_status == 'Late Filer':
                    compliance_status = 'Late Filer'
                    compliance_flag = 'Yellow'
                elif gst_return.payment_status == 'Not paid':
                    compliance_status = 'Payment Default'
                    compliance_flag = 'Red'
                elif gst_return.compliance_status in ['Late Filer', 'Non-Filer']:
                    compliance_status = gst_return.compliance_status
                    compliance_flag = 'Yellow'
                
                # Create compliance record
                compliance = ComplianceMonitoring.objects.create(
                    gstin=gst_return.gstin,
                    taxpayer_name=gst_return.taxpayer_name,
                    tax_period=gst_return.tax_period,
                    filing_status=gst_return.filing_status,
                    filing_delay=gst_return.filing_delay_days,
                    payment_status=gst_return.payment_status,
                    compliance_status=compliance_status,
                    compliance_flag=compliance_flag,
                    remarks=f'Auto-populated from GST Return on {gst_return.return_filing_date}'
                )
                count += 1
        
        self.message_user(request, f'Auto-populated {count} compliance records from GST Returns.')
    
    auto_populate_from_returns.short_description = 'Auto-populate from GST Returns'
    
    def recalculate_compliance_status(self, request, queryset):
        """Recalculate compliance status based on filing and payment status"""
        count = 0
        for compliance in queryset:
            # Determine compliance status
            compliance_status = 'Compliant'
            compliance_flag = 'Green'
            
            if compliance.filing_status == 'Overdue / Non-Filer':
                compliance_status = 'Non-Filer'
                compliance_flag = 'Red'
            elif compliance.filing_status == 'Late Filer':
                compliance_status = 'Late Filer'
                compliance_flag = 'Yellow'
            elif compliance.payment_status == 'Not paid':
                compliance_status = 'Payment Default'
                compliance_flag = 'Red'
            
            compliance.compliance_status = compliance_status
            compliance.compliance_flag = compliance_flag
            compliance.save()
            count += 1
        
        self.message_user(request, f'Recalculated compliance status for {count} records.')
    
    recalculate_compliance_status.short_description = 'Recalculate Compliance Status'
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new record
            # Auto-fetch taxpayer information if GSTIN provided
            if obj.gstin and not obj.taxpayer_name:
                taxpayer = TaxpayerMaster.objects.filter(gstin=obj.gstin, is_primary_license=True).first()
                if taxpayer:
                    obj.taxpayer_name = taxpayer.taxpayer_name
            
            # Auto-fetch from GST return if available
            if obj.gstin and obj.tax_period:
                gst_return = GSTReturn.objects.filter(
                    gstin=obj.gstin,
                    tax_period=obj.tax_period
                ).first()
                if gst_return:
                    obj.filing_status = gst_return.filing_status
                    obj.filing_delay = gst_return.filing_delay_days
                    obj.payment_status = gst_return.payment_status
                    
                    # Determine compliance status
                    if gst_return.filing_status == 'Overdue / Non-Filer':
                        obj.compliance_status = 'Non-Filer'
                        obj.compliance_flag = 'Red'
                    elif gst_return.filing_status == 'Late Filer':
                        obj.compliance_status = 'Late Filer'
                        obj.compliance_flag = 'Yellow'
                    elif gst_return.payment_status == 'Not paid':
                        obj.compliance_status = 'Payment Default'
                        obj.compliance_flag = 'Red'
                    else:
                        obj.compliance_status = 'Compliant'
                        obj.compliance_flag = 'Green'
        
        super().save_model(request, obj, form, change)


class ComplianceRiskReferralForm(forms.ModelForm):
    """Custom form for Compliance Risk & Referral - System Decision Only"""
    class Meta:
        model = ComplianceRiskReferral
        fields = '__all__'
        # Explicitly include assessor field
        exclude = []
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Ensure assessor field is included
        if 'assessor' not in self.fields:
            self.fields['assessor'] = ModelChoiceField(
                queryset=User.objects.filter(is_staff=True),
                required=False,
                empty_label="Select Assessor"
            )
        
        # Filter officer dropdown to show only staff users
        if 'assigned_officer' in self.fields:
            self.fields['assigned_officer'].queryset = User.objects.filter(is_staff=True)
            self.fields['assigned_officer'].required = False
            self.fields['assigned_officer'].empty_label = "Select Officer"
        
        # Filter section head dropdown to show only staff users  
        if 'section_head' in self.fields:
            self.fields['section_head'].queryset = User.objects.filter(is_staff=True)
            self.fields['section_head'].required = False
            self.fields['section_head'].empty_label = "Select Section Head"
        
        # Filter assessor dropdown to show only staff users
        if 'assessor' in self.fields:
            self.fields['assessor'].queryset = User.objects.filter(is_staff=True)
            self.fields['assessor'].required = False
            self.fields['assessor'].empty_label = "Select Assessor"
        
        # Set tax period choices for assessment periods
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
        
        # Apply dropdowns to assessment period fields
        if 'assessment_from_period' in self.fields:
            self.fields['assessment_from_period'] = forms.ChoiceField(
                choices=TAX_PERIOD_CHOICES,
                required=True,
                label='Assessment From Period'
            )
            # Set initial value if instance exists
            if self.instance and self.instance.assessment_from_period:
                # Convert database format to Jan-2026 format if needed
                from .views import convert_date_to_month_year
                converted = convert_date_to_month_year(self.instance.assessment_from_period)
                if converted in [choice[0] for choice in TAX_PERIOD_CHOICES]:
                    self.initial['assessment_from_period'] = converted
                else:
                    self.initial['assessment_from_period'] = self.instance.assessment_from_period
        
        if 'assessment_to_period' in self.fields:
            self.fields['assessment_to_period'] = forms.ChoiceField(
                choices=TAX_PERIOD_CHOICES,
                required=True,
                label='Assessment To Period'
            )
            # Set initial value if instance exists
            if self.instance and self.instance.assessment_to_period:
                # Convert database format to Jan-2026 format if needed
                from .views import convert_date_to_month_year
                converted = convert_date_to_month_year(self.instance.assessment_to_period)
                if converted in [choice[0] for choice in TAX_PERIOD_CHOICES]:
                    self.initial['assessment_to_period'] = converted
                else:
                    self.initial['assessment_to_period'] = self.instance.assessment_to_period
        
        if 'tax_period' in self.fields:
            self.fields['tax_period'].choices = TAX_PERIOD_CHOICES
            self.fields['tax_period'].required = True
            self.fields['tax_period'].empty_label = None
        
        # Make system-generated fields readonly
        if 'system_decision' in self.fields:
            self.fields['system_decision'].widget.attrs['readonly'] = True
        if 'selection' in self.fields:
            self.fields['selection'].widget.attrs['readonly'] = True
        if 'referred_to' in self.fields:
            self.fields['referred_to'].widget.attrs['readonly'] = True
        if 'prescribed_officer_action' in self.fields:
            self.fields['prescribed_officer_action'].widget.attrs['readonly'] = True
    
    def clean_assessment_from_period(self):
        # Convert from Jan-2026 format back to database format (2026-01-01)
        value = self.cleaned_data.get('assessment_from_period')
        if value:
            # Convert Jan-2026 to 2026-01-01
            month_map = {
                'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
                'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
                'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
            }
            if '-' in value:
                parts = value.split('-')
                if len(parts) == 2:
                    month_name, year = parts
                    if month_name in month_map:
                        return f"{year}-{month_map[month_name]}-01"
        return value
    
    def clean_assessment_to_period(self):
        # Convert from Jan-2026 format back to database format (2026-01-01)
        value = self.cleaned_data.get('assessment_to_period')
        if value:
            # Convert Jan-2026 to 2026-01-01
            month_map = {
                'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
                'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
                'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
            }
            if '-' in value:
                parts = value.split('-')
                if len(parts) == 2:
                    month_name, year = parts
                    if month_name in month_map:
                        return f"{year}-{month_map[month_name]}-01"
        return value


@admin.register(ComplianceRiskReferral)
class ComplianceRiskReferralAdmin(admin.ModelAdmin):
    """Admin for Compliance Risk & Referral - Period-based risk assessment with officer judgment"""
    form = ComplianceRiskReferralForm
    list_display = ['risk_id', 'formatted_assessment_from_period', 'gstin', 'taxpayer_name', 'risk_level', 'system_decision', 'assessor', 'assignment_status', 'final_selection']
    change_list_template = 'compliance/compliance_risk_referral_changelist.html'
    
    def changelist_view(self, request, extra_context=None):
        # Add dashboard link to changelist view
        extra_context = extra_context or {}
        extra_context['show_dashboard_link'] = True
        extra_context['dashboard_url'] = '/admin/dashboard/'
        extra_context['dashboard_title'] = 'Main Dashboard'
        return super().changelist_view(request, extra_context)
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.__class__.__name__ in ['DateField', 'DateTimeField']:
            kwargs['widget'] = CustomDateInput()
        return super().formfield_for_dbfield(db_field, **kwargs)
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.__class__.__name__ in ['DateField', 'DateTimeField']:
            kwargs['widget'] = CustomDateInput()
        return super().formfield_for_dbfield(db_field, **kwargs)
    
    def formatted_assessment_from_period(self, obj):
        return self.convert_date_to_month_year(obj.assessment_from_period)
    formatted_assessment_from_period.short_description = 'Assessment From Period'
    
    def formatted_assessment_to_period(self, obj):
        return self.convert_date_to_month_year(obj.assessment_to_period)
    formatted_assessment_to_period.short_description = 'Assessment To Period'
    
    def convert_date_to_month_year(self, date_str):
        """Convert date format '2026-01-01' to 'Jan-2026' format"""
        if not date_str:
            return date_str
        
        try:
            # Handle different date formats
            if '-' in date_str and len(date_str) >= 7:
                parts = date_str.split('-')
                if len(parts) >= 2:
                    year = parts[0]
                    month_part = parts[1]
                    
                    # Try to convert month number to name
                    try:
                        month_num = int(month_part)
                        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                        if 1 <= month_num <= 12:
                            return f"{month_names[month_num-1]}-{year}"
                    except ValueError:
                        pass
            
            # If conversion fails, return original
            return date_str
        except:
            return date_str
    list_display_links = ['risk_id', 'gstin']
    list_filter = ['assessment_from_period', 'assessment_to_period', 'risk_type', 'risk_level', 'system_decision', 'final_selection', 'assessment_status', 'action_status']
    search_fields = ['risk_id', 'gstin', 'taxpayer_name', 'risk_indicator']
    list_per_page = 20
    date_hierarchy = 'assessment_date'
    
    readonly_fields = ['risk_id', 'assessment_date', 'system_decision', 'selection', 'referred_to', 'prescribed_officer_action', 'original_risk_score', 'original_risk_level', 'original_selection', 'original_system_decision']
    
    def save_model(self, request, obj, form, change):
        # Auto-set assessor if creating new assessment
        if not change and not obj.assessor:
            obj.assessor = request.user
        
        # Auto-set section head if they're assigning an officer
        if obj.assigned_officer and not obj.section_head:
            obj.section_head = request.user
            obj.section_head_review_date = timezone.now()
            obj.assignment_date = timezone.now()
            obj.assignment_status = 'Assigned'
        
        # Auto-set assignment date if officer is assigned
        if obj.assigned_officer and not obj.assignment_date:
            obj.assignment_date = timezone.now()
            obj.assignment_status = 'Assigned'
        
        # Auto-set officer recommendation date if recommendation is provided
        if obj.officer_recommendation and not obj.officer_recommendation_date:
            obj.officer_recommendation_date = timezone.now()
        
        super().save_model(request, obj, form, change)
    
    def get_form(self, request, obj=None, **kwargs):
        """Customize form to hide system-generated fields"""
        form = super().get_form(request, obj, **kwargs)
        
        # Make system-generated fields readonly
        if 'system_decision' in form.base_fields:
            form.base_fields['system_decision'].widget.attrs['readonly'] = True
        if 'selection' in form.base_fields:
            form.base_fields['selection'].widget.attrs['readonly'] = True
        if 'referred_to' in form.base_fields:
            form.base_fields['referred_to'].widget.attrs['readonly'] = True
        if 'prescribed_officer_action' in form.base_fields:
            form.base_fields['prescribed_officer_action'].widget.attrs['readonly'] = True
        
        return form
    
    actions = ['open_risk_assessment_dashboard', 'approve_section_head', 'assign_to_officer']
    
    def approve_section_head(self, request, queryset):
        """Section head approves selected referrals for audit delegation"""
        count = 0
        for referral in queryset:
            if referral.system_decision == 'AUDIT' and referral.section_head_approval != 'Approved':
                referral.section_head_approval = 'Approved'
                referral.section_head = request.user
                referral.section_head_review_date = timezone.now()
                referral.save()
                count += 1
        
        self.message_user(request, f'Approved {count} referrals for officer assignment.')
    
    approve_section_head.short_description = 'Approve for Officer Assignment (Section Head)'
    
    def assign_to_officer(self, request, queryset):
        """Action to trigger officer assignment interface"""
        # This will be handled via custom interface
        self.message_user(request, f'Selected {queryset.count()} referrals for officer assignment. Use the change form to assign specific officers.')
    
    def open_risk_assessment_dashboard(self, request, queryset):
        """Redirect to the risk assessment dashboard"""
        from django.shortcuts import redirect
        return redirect('/compliance/compliance_risk_dashboard/')
    
    open_risk_assessment_dashboard.short_description = '🎯 Open Risk Assessment Dashboard'
    
    def changelist_view(self, request, extra_context=None):
        """Override to show Compliance Risk dashboard using raw queries to avoid decimal errors"""
        from django.db import connection
        
        # Calculate risk statistics using raw queries
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM compliance_complianceriskreferral")
            total_assessed = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM compliance_complianceriskreferral WHERE risk_level = 'Low'")
            low_risk_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM compliance_complianceriskreferral WHERE risk_level = 'Medium'")
            medium_risk_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM compliance_complianceriskreferral WHERE risk_level = 'High'")
            high_risk_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM compliance_complianceriskreferral WHERE risk_level = 'Critical'")
            critical_risk_count = cursor.fetchone()[0]
            
            # Selection statistics
            cursor.execute("SELECT COUNT(*) FROM compliance_complianceriskreferral WHERE system_decision = 'AUDIT'")
            audit_selected = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM compliance_complianceriskreferral WHERE system_decision = 'REVIEW'")
            review_selected = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM compliance_complianceriskreferral WHERE system_decision = 'MONITOR'")
            monitor_selected = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM compliance_complianceriskreferral WHERE system_decision = 'NOT SELECTED'")
            not_selected = cursor.fetchone()[0]
            
            # Action status
            cursor.execute("SELECT COUNT(*) FROM compliance_complianceriskreferral WHERE action_status = 'Pending'")
            pending_actions = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM compliance_complianceriskreferral WHERE action_status = 'Assigned'")
            assigned_actions = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM compliance_complianceriskreferral WHERE action_status = 'In Progress'")
            in_progress_actions = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM compliance_complianceriskreferral WHERE action_status = 'Completed'")
            completed_actions = cursor.fetchone()[0]
        
        # Add to context
        extra_context = extra_context or {}
        extra_context.update({
            'total_assessed': total_assessed,
            'low_risk_count': low_risk_count,
            'medium_risk_count': medium_risk_count,
            'high_risk_count': high_risk_count,
            'critical_risk_count': critical_risk_count,
            'audit_selected': audit_selected,
            'review_selected': review_selected,
            'monitor_selected': monitor_selected,
            'not_selected': not_selected,
            'pending_actions': pending_actions,
            'assigned_actions': assigned_actions,
            'in_progress_actions': in_progress_actions,
            'completed_actions': completed_actions,
        })
        
        return super().changelist_view(request, extra_context)
    
    fieldsets = (
        ('Risk Assessment Information', {
            'fields': (
                'risk_id',
                'assessment_from_period',
                'assessment_to_period',
                'assessment_date',
                'assessment_status',
                'assessor'
            )
        }),
        ('Taxpayer Information', {
            'fields': (
                'gstin',
                'taxpayer_name'
            )
        }),
        ('Risk Analysis', {
            'fields': (
                'risk_indicator',
                'risk_pattern',
                'risk_score',
                'risk_level',
                'risk_type',
                'risk_reason'
            )
        }),
        ('System Decision', {
            'fields': ('audit_assertion',)
        }),
        ('Officer Judgment', {
            'fields': (
                'officer_assessment',
                'additional_risk_factor',
                'officer_risk_rating',
                'officer_remarks',
                'override_reason'
            )
        }),
        ('Final Selection', {
            'fields': (
                'final_selection',
                'final_referred_to',
                'action_status'
            )
        }),
        ('Audit Trail', {
            'fields': (
                'original_system_decision',
                'original_risk_score',
                'original_risk_level',
                'original_selection'
            )
        }),
        ('Additional Information', {
            'fields': ('remarks',)
        }),
    )
    
    readonly_fields = ['risk_id', 'assessment_date']
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Make system-generated fields readonly
        if 'risk_score' in form.base_fields:
            form.base_fields['risk_score'].widget.attrs['readonly'] = True
        if 'risk_level' in form.base_fields:
            form.base_fields['risk_level'].widget.attrs['readonly'] = True
        if 'risk_indicator' in form.base_fields:
            form.base_fields['risk_indicator'].widget.attrs['readonly'] = True
        if 'audit_assertion' in form.base_fields:
            form.base_fields['audit_assertion'].widget.attrs['readonly'] = True
        
        return form
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new record
            # Auto-fetch taxpayer information if GSTIN provided
            if obj.gstin and not obj.taxpayer_name:
                taxpayer = TaxpayerMaster.objects.filter(gstin=obj.gstin, is_primary_license=True).first()
                if taxpayer:
                    obj.taxpayer_name = taxpayer.taxpayer_name
            
            # NOTE: System decision is generated by risk engine, not by officer
            # Officer can only execute the prescribed action, not override it
            if request.user and obj.override_reason:
                # Only allow override if override reason is provided (emergency use)
                obj.overridden_by = request.user
                from datetime import datetime
                obj.override_date = datetime.now()
        
        super().save_model(request, obj, form, change)


class EnforcementRecoveryForm(forms.ModelForm):
    """Custom form for Enforcement & Recovery"""
    class Meta:
        model = EnforcementRecovery
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
            self.fields['tax_period'].required = False
            self.fields['tax_period'].empty_label = '---'
        
        # Add date widget for notice_date
        from django.forms import DateInput
        if 'notice_date' in self.fields:
            self.fields['notice_date'].widget = DateInput(attrs={'type': 'date'})


@admin.register(EnforcementRecovery)
class EnforcementRecoveryAdmin(admin.ModelAdmin):
    """Admin for Enforcement & Recovery - Case management"""
    form = EnforcementRecoveryForm
    list_display = ['case_id', 'gstin', 'taxpayer_name', 'tax_period', 'case_type', 'amount_due', 'notice_date', 'action_taken', 'amount_recovered', 'status', 'remarks']
    list_display_links = ['case_id', 'gstin']
    list_filter = ['case_type', 'status', 'tax_period']
    search_fields = ['case_id', 'gstin', 'taxpayer_name']
    list_per_page = 20
    
    def changelist_view(self, request, extra_context=None):
        # Add dashboard link to changelist view
        extra_context = extra_context or {}
        extra_context['show_dashboard_link'] = True
        extra_context['dashboard_url'] = '/admin/dashboard/'
        extra_context['dashboard_title'] = 'Main Dashboard'
        return super().changelist_view(request, extra_context)
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.__class__.__name__ in ['DateField', 'DateTimeField']:
            kwargs['widget'] = CustomDateInput()
        return super().formfield_for_dbfield(db_field, **kwargs)
    
    fieldsets = (
        ('Case Information', {
            'fields': ('case_id', 'tax_period')
        }),
        ('Taxpayer Information', {
            'fields': ('gstin', 'taxpayer_name')
        }),
        ('Case Details', {
            'fields': ('case_type', 'amount_due', 'notice_date')
        }),
        ('Action & Recovery', {
            'fields': ('action_taken', 'amount_recovered', 'status')
        }),
        ('Additional Information', {
            'fields': ('remarks',)
        }),
    )
    
    readonly_fields = ['case_id']
    
    actions = ['auto_create_non_filing_cases', 'auto_create_non_payment_cases']
    
    def changelist_view(self, request, extra_context=None):
        """Override to show enforcement dashboard"""
        response = super().changelist_view(request, extra_context)
        
        # Calculate enforcement statistics
        queryset = self.get_queryset(request)
        total_cases = queryset.count()
        open_cases = queryset.filter(status='Open').count()
        follow_up_cases = queryset.filter(status='Follow-up').count()
        recovered_cases = queryset.filter(status='Recovered').count()
        closed_cases = queryset.filter(status='Closed').count()
        
        # Case type breakdown
        non_filing_cases = queryset.filter(case_type='Non-Filing').count()
        non_payment_cases = queryset.filter(case_type='Non-Payment').count()
        recovery_cases = queryset.filter(case_type='Recovery').count()
        other_cases = queryset.filter(case_type='Other').count()
        
        # Financial summary
        total_amount_due = queryset.aggregate(total=Sum('amount_due'))['total'] or 0
        total_amount_recovered = queryset.aggregate(total=Sum('amount_recovered'))['total'] or 0
        
        # Add to context
        extra_context = extra_context or {}
        extra_context.update({
            'total_cases': total_cases,
            'open_cases': open_cases,
            'follow_up_cases': follow_up_cases,
            'recovered_cases': recovered_cases,
            'closed_cases': closed_cases,
            'non_filing_cases': non_filing_cases,
            'non_payment_cases': non_payment_cases,
            'recovery_cases': recovery_cases,
            'other_cases': other_cases,
            'total_amount_due': total_amount_due,
            'total_amount_recovered': total_amount_recovered,
        })
        
        return response
    
    def auto_create_non_filing_cases(self, request, queryset):
        """Auto-create cases for non-filers from compliance monitoring"""
        from compliance.models import ComplianceMonitoring
        
        count = 0
        non_filers = ComplianceMonitoring.objects.filter(
            compliance_status='Non-Filer'
        )
        
        for non_filer in non_filers:
            # Check if case already exists
            existing = EnforcementRecovery.objects.filter(
                gstin=non_filer.gstin,
                tax_period=non_filer.tax_period,
                case_type='Non-Filing'
            ).first()
            
            if not existing:
                # Get GST return to determine amount due
                gst_return = GSTReturn.objects.filter(
                    gstin=non_filer.gstin,
                    tax_period=non_filer.tax_period
                ).first()
                
                amount_due = 0
                if gst_return:
                    amount_due = abs(gst_return.gst_payable_refundable) if gst_return.gst_payable_refundable < 0 else 0
                
                case = EnforcementRecovery.objects.create(
                    gstin=non_filer.gstin,
                    taxpayer_name=non_filer.taxpayer_name,
                    tax_period=non_filer.tax_period,
                    case_type='Non-Filing',
                    amount_due=amount_due,
                    status='Open',
                    remarks=f'Auto-created from Compliance Monitoring'
                )
                count += 1
        
        self.message_user(request, f'Created {count} non-filing cases.')
    
    auto_create_non_filing_cases.short_description = 'Auto-create Non-Filing Cases'
    
    def auto_create_non_payment_cases(self, request, queryset):
        """Auto-create cases for non-payment from compliance monitoring"""
        from compliance.models import ComplianceMonitoring
        
        count = 0
        non_payers = ComplianceMonitoring.objects.filter(
            compliance_status='Payment Default'
        )
        
        for non_payer in non_payers:
            # Check if case already exists
            existing = EnforcementRecovery.objects.filter(
                gstin=non_payer.gstin,
                tax_period=non_payer.tax_period,
                case_type='Non-Payment'
            ).first()
            
            if not existing:
                # Get GST return to determine amount due
                gst_return = GSTReturn.objects.filter(
                    gstin=non_payer.gstin,
                    tax_period=non_payer.tax_period
                ).first()
                
                amount_due = 0
                if gst_return:
                    amount_due = abs(gst_return.gst_payable_refundable) if gst_return.gst_payable_refundable < 0 else 0
                
                case = EnforcementRecovery.objects.create(
                    gstin=non_payer.gstin,
                    taxpayer_name=non_payer.taxpayer_name,
                    tax_period=non_payer.tax_period,
                    case_type='Non-Payment',
                    amount_due=amount_due,
                    status='Open',
                    remarks=f'Auto-created from Compliance Monitoring'
                )
                count += 1
        
        self.message_user(request, f'Created {count} non-payment cases.')
    
    auto_create_non_payment_cases.short_description = 'Auto-create Non-Payment Cases'
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new record
            # Auto-fetch taxpayer information if GSTIN provided
            if obj.gstin and not obj.taxpayer_name:
                taxpayer = TaxpayerMaster.objects.filter(gstin=obj.gstin, is_primary_license=True).first()
                if taxpayer:
                    obj.taxpayer_name = taxpayer.taxpayer_name
        
        super().save_model(request, obj, form, change)