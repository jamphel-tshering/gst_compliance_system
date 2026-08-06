from import_export import resources
from .models import AuditRegister, ComplianceRiskRegister

class AuditRegisterResource(resources.ModelResource):
    class Meta:
        model = AuditRegister
        fields = (
            'asc_no', 'assessment_date', 'tax_period',
            'gstin', 'taxpayer_name', 'dzongkhag', 'organisation_type', 'frequency', 'assessment_type',
            'declared_sales', 'gst_on_declared_sales', 'declared_import_value', 'gst_on_declared_import', 'declared_domestic_purchase', 'gst_on_declared_domestic_purchase',
            'assessed_sales_turnover', 'actual_import_value', 'assessed_import_value', 'gst_on_assessed_import_value', 'assessed_domestic_purchase', 'gst_on_assessed_domestic_purchase',
            'gst_payable_refundable_return', 'gst_payable_refundable_assessed',
            'variation', 'variation_percentage',
            'reason_code', 'discrepancy', 'assessment_audit_outcome', 'action_taken',
            'status', 'case_closed_date', 'assessment_duration_days',
            'assessor'
        )
        export_order = (
            'asc_no', 'assessment_date', 'tax_period',
            'gstin', 'taxpayer_name', 'dzongkhag', 'organisation_type', 'frequency', 'assessment_type',
            'declared_sales', 'gst_on_declared_sales', 'declared_import_value', 'gst_on_declared_import', 'declared_domestic_purchase', 'gst_on_declared_domestic_purchase',
            'assessed_sales_turnover', 'actual_import_value', 'assessed_import_value', 'gst_on_assessed_import_value', 'assessed_domestic_purchase', 'gst_on_assessed_domestic_purchase',
            'gst_payable_refundable_return', 'gst_payable_refundable_assessed',
            'variation', 'variation_percentage',
            'reason_code', 'discrepancy', 'assessment_audit_outcome', 'action_taken',
            'status', 'case_closed_date', 'assessment_duration_days',
            'assessor'
        )
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ['asc_no']


class ComplianceRiskRegisterResource(resources.ModelResource):
    class Meta:
        model = ComplianceRiskRegister
        fields = (
            'taxpayer', 'assessment_period',
            'inherent_risk', 'control_risk', 'detection_risk', 'transaction_risk', 'behavior_risk',
            'overall_risk_score', 'risk_category',
            'assessment_status', 'assessment_date', 'assessed_by',
            'import_sales_ratio', 'consecutive_negative_returns', 'import_zero_sales_periods', 'high_domestic_purchases', 'cash_sales_suppression', 'sales_variation',
            'recommendations', 'audit_priority', 'requires_immediate_audit', 'audit_reference'
        )
        export_order = (
            'taxpayer', 'assessment_period',
            'inherent_risk', 'control_risk', 'detection_risk', 'transaction_risk', 'behavior_risk',
            'overall_risk_score', 'risk_category',
            'assessment_status', 'assessment_date', 'assessed_by',
            'import_sales_ratio', 'consecutive_negative_returns', 'import_zero_sales_periods', 'high_domestic_purchases', 'cash_sales_suppression', 'sales_variation',
            'recommendations', 'audit_priority', 'requires_immediate_audit', 'audit_reference'
        )
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ['taxpayer', 'assessment_period']