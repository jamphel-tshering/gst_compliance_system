from import_export import resources, widgets
from .models import AuditRegister, ComplianceRiskRegister, AuditAllotment
from decimal import Decimal
from core.models import User
from datetime import datetime

class DecimalWidget(widgets.Widget):
    """Custom widget to handle float to Decimal conversion"""
    def clean(self, value, row=None, **kwargs):
        if value is None or value == '':
            return Decimal('0')
        try:
            return Decimal(str(value))
        except:
            return Decimal('0')

class AssessorWidget(widgets.Widget):
    """Custom widget to handle assessor by email/username"""
    def clean(self, value, row=None, **kwargs):
        if value is None or value == '':
            return None
        try:
            # Try to find user by email first, then by username
            user = User.objects.filter(email=value).first()
            if not user:
                user = User.objects.filter(username=value).first()
            return user
        except:
            return None

class TaxPeriodWidget(widgets.Widget):
    """Custom widget to handle tax period in Jan-2026 format"""
    def clean(self, value, row=None, **kwargs):
        if value is None or value == '':
            return None
        try:
            # Convert Jan-2026 to 2026-01-01
            if '-' in value and len(value.split('-')) == 2:
                parts = value.split('-')
                month_name = parts[0].strip()
                year = parts[1].strip()
                
                month_map = {
                    'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
                    'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
                    'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
                }
                
                month_num = month_map.get(month_name, '01')
                return f"{year}-{month_num}-01"
            return value
        except:
            return value

class AllotmentDateWidget(widgets.Widget):
    """Custom widget to handle allotment date in dd-mm-yyyy format"""
    def clean(self, value, row=None, **kwargs):
        if value is None or value == '':
            return None
        try:
            # Handle if already a date object
            if hasattr(value, 'strftime'):
                return value
            
            # Convert dd-mm-yyyy to yyyy-mm-dd
            if isinstance(value, str) and '-' in value:
                parts = value.split('-')
                if len(parts) == 3:
                    # Check if it's dd-mm-yyyy format (year is last)
                    if len(parts[2]) == 4:
                        return f"{parts[2]}-{parts[1]}-{parts[0]}"
                    # Check if it's yyyy-mm-dd format (year is first)
                    elif len(parts[0]) == 4:
                        return value
            return value
        except Exception as e:
            # If conversion fails, return a default date or None
            return None

class AuditRegisterResource(resources.ModelResource):
    declared_sales = resources.Field(attribute='declared_sales', widget=DecimalWidget())
    gst_on_declared_sales = resources.Field(attribute='gst_on_declared_sales', widget=DecimalWidget())
    declared_import_value = resources.Field(attribute='declared_import_value', widget=DecimalWidget())
    gst_on_declared_import = resources.Field(attribute='gst_on_declared_import', widget=DecimalWidget())
    declared_domestic_purchase = resources.Field(attribute='declared_domestic_purchase', widget=DecimalWidget())
    gst_on_declared_domestic_purchase = resources.Field(attribute='gst_on_declared_domestic_purchase', widget=DecimalWidget())
    assessed_sales_turnover = resources.Field(attribute='assessed_sales_turnover', widget=DecimalWidget())
    actual_import_value = resources.Field(attribute='actual_import_value', widget=DecimalWidget())
    assessed_import_value = resources.Field(attribute='assessed_import_value', widget=DecimalWidget())
    gst_on_assessed_import_value = resources.Field(attribute='gst_on_assessed_import_value', widget=DecimalWidget())
    assessed_domestic_purchase = resources.Field(attribute='assessed_domestic_purchase', widget=DecimalWidget())
    gst_on_assessed_domestic_purchase = resources.Field(attribute='gst_on_assessed_domestic_purchase', widget=DecimalWidget())
    gst_payable_refundable_return = resources.Field(attribute='gst_payable_refundable_return', widget=DecimalWidget())
    gst_payable_refundable_assessed = resources.Field(attribute='gst_payable_refundable_assessed', widget=DecimalWidget())
    variation = resources.Field(attribute='variation', widget=DecimalWidget())
    variation_percentage = resources.Field(attribute='variation_percentage', widget=DecimalWidget())
    
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
    inherent_risk = resources.Field(attribute='inherent_risk', widget=DecimalWidget())
    control_risk = resources.Field(attribute='control_risk', widget=DecimalWidget())
    detection_risk = resources.Field(attribute='detection_risk', widget=DecimalWidget())
    gst_behaviour_risk = resources.Field(attribute='gst_behaviour_risk', widget=DecimalWidget())
    transaction_risk = resources.Field(attribute='transaction_risk', widget=DecimalWidget())
    overall_risk_score = resources.Field(attribute='overall_risk_score', widget=DecimalWidget())
    import_sales_ratio = resources.Field(attribute='import_sales_ratio', widget=DecimalWidget())
    sales_variation = resources.Field(attribute='sales_variation', widget=DecimalWidget())
    
    class Meta:
        model = ComplianceRiskRegister
        fields = (
            'risk_id', 'taxpayer', 'assessment_period',
            'gstin', 'taxpayer_name', 'business_name', 'activity', 'sector', 'sub_sector', 'organisation_type', 'frequency', 'dzongkhag',
            'registration_date', 'taxpayer_status',
            'inherent_risk', 'control_risk', 'detection_risk', 'gst_behaviour_risk', 'transaction_risk',
            'overall_risk_score', 'overall_risk_level', 'risk_rank',
            'gst_behaviour_reason', 'transaction_risk_reason', 'overall_risk_reason',
            'primary_assertion', 'secondary_assertion', 'assertion_reason', 'audit_focus',
            'audit_priority', 'audit_selection', 'assigned_assessor', 'remarks',
            'assessment_status', 'assessment_date', 'assessed_by',
            'import_sales_ratio', 'consecutive_negative_returns', 'import_zero_sales_periods', 'high_domestic_purchases', 'cash_sales_suppression', 'sales_variation',
            'recommendations', 'requires_immediate_audit', 'audit_reference'
        )
        export_order = (
            'risk_id', 'taxpayer', 'assessment_period',
            'gstin', 'taxpayer_name', 'business_name', 'activity', 'sector', 'sub_sector', 'organisation_type', 'frequency', 'dzongkhag',
            'registration_date', 'taxpayer_status',
            'inherent_risk', 'control_risk', 'detection_risk', 'gst_behaviour_risk', 'transaction_risk',
            'overall_risk_score', 'overall_risk_level', 'risk_rank',
            'gst_behaviour_reason', 'transaction_risk_reason', 'overall_risk_reason',
            'primary_assertion', 'secondary_assertion', 'assertion_reason', 'audit_focus',
            'audit_priority', 'audit_selection', 'assigned_assessor', 'remarks',
            'assessment_status', 'assessment_date', 'assessed_by',
            'import_sales_ratio', 'consecutive_negative_returns', 'import_zero_sales_periods', 'high_domestic_purchases', 'cash_sales_suppression', 'sales_variation',
            'recommendations', 'requires_immediate_audit', 'audit_reference'
        )
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ['risk_id']


class AuditAllotmentResource(resources.ModelResource):
    """Resource for Audit Allotment with Excel import/export"""
    tax_period = resources.Field(attribute='tax_period', column_name='Tax Period', widget=TaxPeriodWidget())
    gstin = resources.Field(attribute='gstin', column_name='GSTIN')
    taxpayer_name = resources.Field(attribute='taxpayer_name', column_name='Taxpayer Name')
    dzongkhag = resources.Field(attribute='dzongkhag', column_name='Dzongkhag')
    # Use American spelling "Organization Type" as primary
    organisation_type = resources.Field(attribute='organisation_type', column_name='Organization Type')
    # Keep British spelling as fallback
    organization_type = resources.Field(attribute='organisation_type', column_name='Organisation Type')
    frequency = resources.Field(attribute='frequency', column_name='Frequency')
    assessor = resources.Field(attribute='assessor', column_name='Assessor', widget=AssessorWidget())
    allotment_date = resources.Field(attribute='allotment_date', column_name='Allotment Date', widget=AllotmentDateWidget())
    remarks = resources.Field(attribute='remarks', column_name='Remarks')
    audit_register = resources.Field(attribute='audit_register', column_name='Audit Register', readonly=True)
    
    def skip_row(self, instance, original):
        """Skip rows with missing required fields"""
        # Skip rows without GSTIN or tax_period (these are required)
        if not instance.gstin or not instance.tax_period:
            return True
        # Skip rows with empty taxpayer_name
        if not instance.taxpayer_name:
            return True
        return False
    
    def get_instance(self, instance_loader, row):
        """Always create new instances instead of updating existing ones"""
        return None
    
    class Meta:
        model = AuditAllotment
        skip_unchanged = True
        report_skipped = True
        # Explicitly specify fields to import/export, excluding 'id'
        fields = (
            'tax_period', 'gstin', 'taxpayer_name', 'dzongkhag', 
            'organisation_type', 'organization_type', 'frequency', 'assessor', 
            'allotment_date', 'remarks', 'audit_register'
        )
        export_order = (
            'tax_period', 'gstin', 'taxpayer_name', 'dzongkhag',
            'organisation_type', 'frequency', 'assessor',
            'allotment_date', 'remarks', 'audit_register'
        )
        # Use exclude to skip the 'id' field if it exists in the import
        exclude = ('id',)