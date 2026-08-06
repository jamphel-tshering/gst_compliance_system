from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import AuditRegister, ComplianceRiskRegister, RiskFactorDetail, RiskAlert
from .resources import AuditRegisterResource, ComplianceRiskRegisterResource

class RiskFactorDetailInline(admin.TabularInline):
    model = RiskFactorDetail
    extra = 0
    fields = ['factor_type', 'factor_value', 'factor_score', 'max_score', 'severity', 'description']

@admin.register(AuditRegister)
class AuditRegisterAdmin(ImportExportModelAdmin):
    resource_class = AuditRegisterResource
    list_display = ['asc_no', 'assessment_date', 'tax_period', 'taxpayer_name', 'assessment_type', 'status', 'variation']
    list_filter = ['assessment_type', 'status', 'assessment_date']
    search_fields = ['asc_no', 'gstin', 'taxpayer_name']
    ordering = ['-assessment_date', 'taxpayer_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Assessment Information', {
            'fields': ('asc_no', 'assessment_date', 'tax_period')
        }),
        ('Taxpayer Information', {
            'fields': ('gstin', 'taxpayer_name', 'dzongkhag', 'organisation_type', 'frequency', 'assessment_type')
        }),
        ('GST Return Information (Declared)', {
            'fields': ('declared_sales', 'gst_on_declared_sales', 'declared_import_value', 'gst_on_declared_import', 'declared_domestic_purchase', 'gst_on_declared_domestic_purchase')
        }),
        ('Assessed Information (eCMS)', {
            'fields': ('assessed_sales_turnover', 'actual_import_value', 'assessed_import_value', 'gst_on_assessed_import_value', 'assessed_domestic_purchase', 'gst_on_assessed_domestic_purchase')
        }),
        ('GST Payable/Refundable', {
            'fields': ('gst_payable_refundable_return', 'gst_payable_refundable_assessed')
        }),
        ('Variation Analysis', {
            'fields': ('variation', 'variation_percentage')
        }),
        ('Assessment Details', {
            'fields': ('reason_code', 'discrepancy', 'assessment_audit_outcome', 'action_taken')
        }),
        ('Status and Timeline', {
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
    list_display = ['taxpayer', 'assessment_period', 'overall_risk_score', 'risk_category', 'assessment_status', 'requires_immediate_audit']
    list_filter = ['risk_category', 'assessment_status', 'requires_immediate_audit']
    search_fields = ['taxpayer__taxpayer_name', 'taxpayer__gstin']
    inlines = [RiskFactorDetailInline]
    ordering = ['-overall_risk_score', 'taxpayer']
    readonly_fields = ['overall_risk_score', 'risk_category', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Taxpayer Information', {
            'fields': ('taxpayer', 'assessment_period')
        }),
        ('Risk Scores (5 Dimensions)', {
            'fields': ('inherent_risk', 'control_risk', 'detection_risk', 'transaction_risk', 'behavior_risk')
        }),
        ('Overall Risk', {
            'fields': ('overall_risk_score', 'risk_category')
        }),
        ('Assessment Details', {
            'fields': ('assessment_status', 'assessment_date', 'assessed_by')
        }),
        ('Risk Factors', {
            'fields': ('import_sales_ratio', 'consecutive_negative_returns', 'import_zero_sales_periods', 'high_domestic_purchases', 'cash_sales_suppression', 'sales_variation')
        }),
        ('Recommendations', {
            'fields': ('recommendations', 'audit_priority', 'requires_immediate_audit', 'audit_reference')
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(RiskFactorDetail)
class RiskFactorDetailAdmin(admin.ModelAdmin):
    list_display = ['risk_register', 'factor_type', 'factor_score', 'max_score', 'severity']
    list_filter = ['factor_type', 'severity']
    search_fields = ['risk_register__taxpayer__taxpayer_name']


@admin.register(RiskAlert)
class RiskAlertAdmin(admin.ModelAdmin):
    list_display = ['taxpayer', 'alert_type', 'alert_status', 'title', 'created_at']
    list_filter = ['alert_type', 'alert_status', 'created_at']
    search_fields = ['taxpayer__taxpayer_name', 'title', 'message']
    ordering = ['-created_at']