from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.urls import reverse
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from .models import AuditRegister, ComplianceRiskRegister, RiskFactorDetail, RiskAlert, AuditAllotment
from .resources import AuditRegisterResource, ComplianceRiskRegisterResource, AuditAllotmentResource
from datetime import datetime


class AssessmentFrequencyFilter(SimpleListFilter):
    """Custom filter for assessment frequency (Monthly, Quarterly, Annual) based on taxpayer frequency"""
    title = 'Taxpayer Frequency'
    parameter_name = 'taxpayer_frequency'
    
    def lookups(self, request, model_admin):
        return [
            ('annual', 'Annual'),
            ('quarterly', 'Quarterly'),
            ('monthly', 'Monthly'),
        ]
    
    def queryset(self, request, queryset):
        if self.value() == 'annual':
            # Filter for annual taxpayers
            return queryset.filter(frequency='Annual')
        elif self.value() == 'quarterly':
            # Filter for quarterly taxpayers
            return queryset.filter(frequency='Quarterly')
        elif self.value() == 'monthly':
            # Filter for monthly taxpayers
            return queryset.filter(frequency='Monthly')
        return queryset


class TaxPeriodFilter(SimpleListFilter):
    """Custom filter for tax period to display in Jan-2026 format"""
    title = 'Tax Period'
    parameter_name = 'tax_period'
    
    def lookups(self, request, model_admin):
        # Get unique assessment periods from ComplianceRiskRegister
        from risk_assessment.models import ComplianceRiskRegister
        periods = set()
        
        for obj in ComplianceRiskRegister.objects.all():
            period_field = getattr(obj, 'assessment_period', None)
            if period_field:
                try:
                    date_obj = datetime.strptime(str(period_field), '%Y-%m-%d')
                    formatted = date_obj.strftime('%b-%Y')
                    periods.add((period_field, formatted))
                except:
                    # Handle quarterly format like "Jan-Mar 2026"
                    try:
                        if '-' in str(period_field) and ' ' in str(period_field):
                            formatted = str(period_field)  # Keep original format
                            periods.add((period_field, formatted))
                        else:
                            periods.add((period_field, period_field))
                    except:
                        periods.add((period_field, period_field))
        
        # Sort by date (most recent first)
        def sort_key(x):
            try:
                date_obj = datetime.strptime(str(x[0]), '%Y-%m-%d')
                return date_obj.timestamp()
            except:
                # For quarterly periods, try to extract year
                try:
                    year = int(str(x[0]).split()[-1])
                    return year
                except:
                    return 0
        
        sorted_periods = sorted(periods, key=sort_key, reverse=True)
        return sorted_periods
    
    def queryset(self, request, queryset):
        if self.value():
            # Filter by assessment_period field
            return queryset.filter(assessment_period=self.value())
        return queryset


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

# class RiskFactorDetailInline(admin.TabularInline):
#     model = RiskFactorDetail
#     extra = 0
#     fields = ['factor_type', 'factor_value', 'factor_score', 'max_score', 'severity', 'description']


@admin.register(AuditRegister)
class AuditRegisterAdmin(ImportExportModelAdmin):
    resource_class = AuditRegisterResource
    list_display = ['asc_no', 'assessment_date', 'display_tax_period', 'taxpayer_name', 'assessment_type', 'status', 'variation', 'display_assessment_duration']
    list_filter = [TaxPeriodFilter, 'assessment_type', 'status', 'assessment_date']
    search_fields = ['asc_no', 'gstin', 'taxpayer_name']
    ordering = ['-assessment_date', 'taxpayer_name']
    readonly_fields = [
        'asc_no', 'assessment_date', 'tax_period',
        'gstin', 'taxpayer_name', 'dzongkhag', 'organisation_type', 'frequency', 'assessment_type',
        # GST Return Information (Declared) - Auto-pulled from GST Returns
        'declared_sales', 'gst_on_declared_sales', 'declared_import_value', 'gst_on_declared_import', 
        'declared_domestic_purchase', 'gst_on_declared_domestic_purchase',
        # Auto-calculated fields
        'gst_on_assessed_import_value', 'gst_on_assessed_domestic_purchase', 
        'gst_payable_refundable_assessed', 'variation', 'variation_percentage', 'assessment_duration_days',
        # System fields
        'created_at', 'updated_at'
    ]
    list_per_page = 100
    show_full_result_count = False
    actions = ['pull_from_gst_returns']
    
    class Media:
        css = {
            'all': ('admin/css/hide_filter_counts.css',)
        }
    
    def display_tax_period(self, obj):
        """Display tax period in Jan-2026 format"""
        if obj.tax_period:
            try:
                date_obj = datetime.strptime(str(obj.tax_period), '%Y-%m-%d')
                return date_obj.strftime('%b-%Y')
            except:
                return obj.tax_period
        return '-'
    display_tax_period.short_description = 'Tax Period'
    
    def display_assessment_duration(self, obj):
        """Display assessment duration in days"""
        if obj.assessment_duration_days:
            return f"{obj.assessment_duration_days} days"
        return '-'
    display_assessment_duration.short_description = 'Duration'
    
    def pull_from_gst_returns(self, request, queryset):
        """Bulk action to pull data from GST Returns"""
        from returns.models import GSTReturn
        from decimal import Decimal
        
        count = 0
        for audit_reg in queryset:
            # Find matching GST return for this taxpayer and period
            gst_return = GSTReturn.objects.filter(
                gstin=audit_reg.gstin,
                tax_period=audit_reg.tax_period
            ).first()
            
            if gst_return:
                # Pull declared values from GST Return
                audit_reg.declared_sales = gst_return.declared_sales
                audit_reg.gst_on_declared_sales = gst_return.gst_on_declared_sales
                audit_reg.declared_import_value = gst_return.declared_import_value
                audit_reg.gst_on_declared_import = gst_return.gst_on_declared_import
                audit_reg.declared_domestic_purchase = gst_return.declared_domestic_purchase
                audit_reg.gst_on_declared_domestic_purchase = gst_return.gst_on_declared_domestic_purchase
                audit_reg.gst_payable_refundable_return = gst_return.gst_payable_refundable
                
                audit_reg.save()
                count += 1
        
        self.message_user(request, f'Pulled GST return data for {count} audit registers.')
    
    fieldsets = (
        ('Assessment Information', {
            'fields': ('asc_no', 'assessment_date', 'tax_period')
        }),
        ('Taxpayer Information', {
            'fields': ('gstin', 'taxpayer_name', 'dzongkhag', 'organisation_type', 'frequency', 'assessment_type')
        }),
        ('GST Return Information (Declared - Auto-pulled from GST Returns)', {
            'fields': ('declared_sales', 'gst_on_declared_sales', 'declared_import_value', 'gst_on_declared_import', 'declared_domestic_purchase', 'gst_on_declared_domestic_purchase', 'gst_payable_refundable_return')
        }),
        ('Assessed Information (eCMS)', {
            'fields': ('assessed_sales_turnover', 'actual_import_value', 'assessed_import_value', 'gst_on_assessed_import_value', 'assessed_domestic_purchase', 'gst_on_assessed_domestic_purchase')
        }),
        ('GST Payable/Refundable (Auto-calculated)', {
            'fields': ('gst_payable_refundable_assessed',)
        }),
        ('Variation Analysis (Auto-calculated)', {
            'fields': ('variation', 'variation_percentage')
        }),
        ('Assessment Details', {
            'fields': ('reason_code', 'discrepancy', 'assessment_audit_outcome', 'action_taken')
        }),
        ('Status and Timeline (Auto-calculated)', {
            'fields': ('status', 'case_closed_date', 'assessment_duration_days')
        }),
        ('Assessor Information', {
            'fields': ('assessor',)
        }),
        ('System Information', {
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ComplianceRiskRegister)
class ComplianceRiskRegisterAdmin(ImportExportModelAdmin):
    resource_class = ComplianceRiskRegisterResource
    list_display = ['risk_id', 'taxpayer_name', 'display_tax_period', 'overall_risk_score', 'display_risk_level', 'assessment_status', 'audit_selection', 'audit_priority', 'display_audit_register', 'create_audit_link']
    list_filter = [TaxPeriodFilter, AssessmentFrequencyFilter, 'overall_risk_level', 'assessment_status', 'audit_selection']
    search_fields = ['risk_id', 'taxpayer__taxpayer_name', 'taxpayer__gstin', 'gstin']
    ordering = ['-overall_risk_score', 'taxpayer']
    readonly_fields = [
        'risk_id', 'taxpayer', 'gstin', 'taxpayer_name', 'business_name', 'activity', 'sector', 'sub_sector',
        'organisation_type', 'frequency', 'dzongkhag', 'registration_date', 'taxpayer_status',
        'inherent_risk', 'control_risk', 'detection_risk', 'gst_behaviour_risk', 'transaction_risk',
        'overall_risk_score', 'overall_risk_level', 'risk_rank',
        'gst_behaviour_reason', 'transaction_risk_reason', 'overall_risk_reason',
        'primary_assertion', 'secondary_assertion', 'assertion_reason', 'audit_focus',
        'import_sales_ratio', 'consecutive_negative_returns', 'consecutive_credit_filings', 'import_zero_sales_periods',
        'high_domestic_purchases', 'cash_sales_suppression', 'sales_variation', 'stock_analysis_indicators',
        'assessment_date', 'created_at', 'updated_at'
    ]
    list_per_page = 100
    show_full_result_count = False
    
    actions = ['create_audit_register']
    
    class Media:
        css = {
            'all': ('admin/css/hide_filter_counts.css',)
        }
    
    def display_risk_level(self, obj):
        return get_display_value(obj, 'overall_risk_level')
    display_risk_level.short_description = 'Risk Level'
    
    def display_tax_period(self, obj):
        """Display assessment period in readable format"""
        if obj.assessment_period:
            try:
                # Try to parse as date first
                date_obj = datetime.strptime(str(obj.assessment_period), '%Y-%m-%d')
                return date_obj.strftime('%b-%Y')
            except:
                # Handle quarterly format like "Jan-Mar 2026"
                return str(obj.assessment_period)
        return '-'
    display_tax_period.short_description = 'Tax Period'
    
    def display_assessment_status(self, obj):
        return get_display_value(obj, 'assessment_status')
    display_assessment_status.short_description = 'Assessment Status'
    
    def display_audit_register(self, obj):
        """Display linked audit register if exists"""
        if obj.audit_register:
            url = reverse('admin:risk_assessment_auditregister_change', args=[obj.audit_register.id])
            return format_html('<a href="{}">{}</a>', url, obj.audit_register.asc_no)
        return '-'
    display_audit_register.short_description = 'Audit Register'
    
    def create_audit_link(self, obj):
        """Display link to create audit register"""
        if obj.audit_selection == 'selected' and not obj.audit_register:
            url = reverse('admin:risk_assessment_auditregister_add') + f'?gstin={obj.gstin}&taxpayer_name={obj.taxpayer_name}'
            return format_html('<a href="{}" class="button">Create Audit Register</a>', url)
        return '-'
    create_audit_link.short_description = 'Create Audit'
    
    def create_audit_register(self, request, queryset):
        """Bulk action to create audit registers for selected risk registers"""
        from risk_assessment.models import AuditRegister
        from returns.models import GSTReturn
        
        count = 0
        for risk_register in queryset.filter(audit_selection='selected', audit_register__isnull=True):
            # Get the latest return for this taxpayer and period
            latest_return = GSTReturn.objects.filter(
                gstin=risk_register.gstin,
                tax_period=risk_register.assessment_period
            ).first()
            
            if latest_return:
                # Create audit register with GST return data auto-pulled
                audit_reg = AuditRegister.objects.create(
                    assessment_date=risk_register.assessment_date,
                    tax_period=risk_register.assessment_period,
                    gstin=risk_register.gstin,
                    taxpayer_name=risk_register.taxpayer_name,
                    dzongkhag=risk_register.dzongkhag,
                    organisation_type=risk_register.organisation_type,
                    frequency=risk_register.frequency,
                    assessment_type='comprehensive',
                    # GST Return Information (Declared) - Auto-pulled from GST Returns
                    declared_sales=latest_return.declared_sales,
                    gst_on_declared_sales=latest_return.gst_on_declared_sales,
                    declared_import_value=latest_return.declared_import_value,
                    gst_on_declared_import=latest_return.gst_on_declared_import,
                    declared_domestic_purchase=latest_return.declared_domestic_purchase,
                    gst_on_declared_domestic_purchase=latest_return.gst_on_declared_domestic_purchase,
                    gst_payable_refundable_return=latest_return.gst_payable_refundable,
                    status='pending'
                )
                
                # Link to risk register
                risk_register.audit_register = audit_reg
                risk_register.save()
                count += 1
        
        self.message_user(request, f'Created {count} audit registers with GST return data.')
    
    fieldsets = (
        ('Taxpayer Profile', {
            'fields': ('risk_id', 'taxpayer', 'gstin', 'taxpayer_name', 'business_name', 'activity', 'sector', 'sub_sector', 'organisation_type', 'frequency', 'dzongkhag')
        }),
        ('Taxpayer Status', {
            'fields': ('registration_date', 'taxpayer_status')
        }),
        ('Risk Scores (5 Dimensions - 0-5 Scale)', {
            'fields': ('inherent_risk', 'control_risk', 'detection_risk', 'gst_behaviour_risk', 'transaction_risk')
        }),
        ('Overall Risk Assessment', {
            'fields': ('overall_risk_score', 'overall_risk_level', 'risk_rank')
        }),
        ('Risk Explanation', {
            'fields': ('gst_behaviour_reason', 'transaction_risk_reason', 'overall_risk_reason')
        }),
        ('Audit Assertions', {
            'fields': ('primary_assertion', 'secondary_assertion', 'assertion_reason', 'audit_focus')
        }),
        ('Audit Decision', {
            'fields': ('audit_priority', 'audit_selection', 'audit_register', 'assigned_assessor', 'remarks')
        }),
        ('Assessment Details', {
            'fields': ('assessment_status', 'assessed_by')
        }),
        ('Risk Factors (Indicators)', {
            'fields': ('import_sales_ratio', 'consecutive_negative_returns', 'consecutive_credit_filings', 'import_zero_sales_periods', 'high_domestic_purchases', 'cash_sales_suppression', 'sales_variation', 'stock_analysis_indicators')
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AuditAllotment)
class AuditAllotmentAdmin(ImportExportModelAdmin):
    resource_class = AuditAllotmentResource
    list_display = ['display_tax_period', 'gstin', 'taxpayer_name', 'dzongkhag', 'organisation_type', 'frequency', 'assessor', 'display_allotment_date', 'display_audit_register', 'remarks']
    list_filter = ['tax_period', 'dzongkhag', 'organisation_type', 'frequency', 'assessor', 'allotment_date']
    search_fields = ['gstin', 'taxpayer_name', 'assessor__username', 'assessor__email']
    ordering = ['-allotment_date', 'taxpayer_name']
    list_per_page = 100
    show_full_result_count = False
    
    # Exclude fields from import/export
    skip_import_id_fields = True
    
    actions = ['create_audit_registers_from_allotment']
    
    def display_tax_period(self, obj):
        """Display tax period in Jan-2026 format"""
        if obj.tax_period:
            try:
                date_obj = datetime.strptime(str(obj.tax_period), '%Y-%m-%d')
                return date_obj.strftime('%b-%Y')
            except:
                return obj.tax_period
        return '-'
    display_tax_period.short_description = 'Tax Period'
    
    def display_allotment_date(self, obj):
        """Display allotment date in dd-mm-yyyy format"""
        if obj.allotment_date:
            return obj.allotment_date.strftime('%d-%m-%Y')
        return '-'
    display_allotment_date.short_description = 'Allotment Date'
    
    def display_audit_register(self, obj):
        """Display linked audit register if exists"""
        if obj.audit_register:
            url = reverse('admin:risk_assessment_auditregister_change', args=[obj.audit_register.id])
            return format_html('<a href="{}">{}</a>', url, obj.audit_register.asc_no)
        return '-'
    display_audit_register.short_description = 'Audit Register'
    
    def create_audit_registers_from_allotment(self, request, queryset):
        """Create audit registers from audit allotments"""
        from risk_assessment.models import AuditRegister
        from returns.models import GSTReturn
        from taxpayers.models import TaxpayerMaster
        
        count = 0
        for allotment in queryset.filter(audit_register__isnull=True):
            # Get taxpayer info
            try:
                taxpayer = TaxpayerMaster.objects.get(gstin=allotment.gstin)
                
                # Get the latest return for this taxpayer and period
                latest_return = GSTReturn.objects.filter(
                    gstin=allotment.gstin,
                    tax_period=allotment.tax_period
                ).first()
                
                if latest_return:
                    # Create audit register with GST return data auto-pulled
                    audit_reg = AuditRegister.objects.create(
                        assessment_date=allotment.allotment_date,
                        tax_period=allotment.tax_period,
                        gstin=allotment.gstin,
                        taxpayer_name=allotment.taxpayer_name,
                        dzongkhag=allotment.dzongkhag,
                        organisation_type=allotment.organisation_type,
                        frequency=allotment.frequency,
                        assessment_type='comprehensive',
                        # GST Return Information (Declared) - Auto-pulled from GST Returns
                        declared_sales=latest_return.declared_sales,
                        gst_on_declared_sales=latest_return.gst_on_declared_sales,
                        declared_import_value=latest_return.declared_import_value,
                        gst_on_declared_import=latest_return.gst_on_declared_import,
                        declared_domestic_purchase=latest_return.declared_domestic_purchase,
                        gst_on_declared_domestic_purchase=latest_return.gst_on_declared_domestic_purchase,
                        gst_payable_refundable_return=latest_return.gst_payable_refundable,
                        assessor=allotment.assessor,
                        status='pending'
                    )
                    
                    # Link to allotment
                    allotment.audit_register = audit_reg
                    allotment.save()
                    count += 1
                    
            except TaxpayerMaster.DoesNotExist:
                continue
        
        self.message_user(request, f'Created {count} audit registers from allotments with GST return data.')
    
    fieldsets = (
        ('Taxpayer Information', {
            'fields': ('tax_period', 'gstin', 'taxpayer_name', 'dzongkhag', 'organisation_type', 'frequency')
        }),
        ('Allotment Information', {
            'fields': ('assessor', 'allotment_date', 'audit_register', 'remarks')
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at', 'created_by'),
            'classes': ('collapse',)
        }),
    )


# Removed - Redundant with Compliance Risk Register
# @admin.register(RiskFactorDetail)
# class RiskFactorDetailAdmin(admin.ModelAdmin):
#     list_display = ['risk_register', 'factor_type', 'factor_score', 'max_score', 'severity']
#     list_filter = ['factor_type', 'severity']
#     search_fields = ['risk_register__taxpayer__taxpayer_name']


# Removed - Redundant with Compliance Risk Register  
# @admin.register(RiskAlert)
# class RiskAlertAdmin(admin.ModelAdmin):
#     list_display = ['taxpayer', 'alert_type', 'alert_status', 'title', 'created_at']
#     list_filter = ['alert_type', 'alert_status', 'created_at']
#     search_fields = ['taxpayer__taxpayer_name', 'title', 'message']
#     ordering = ['-created_at']