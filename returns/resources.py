from import_export import fields, resources, widgets
from .models import GSTReturn, NotFile

class GSTReturnResource(resources.ModelResource):
    tax_period = fields.Field(attribute='tax_period', column_name='Tax Period')
    return_due_date = fields.Field(attribute='return_due_date', column_name='Return Due Date', widget=widgets.DateWidget('%Y-%m-%d'))
    return_filing_date = fields.Field(attribute='return_filing_date', column_name='Return Filing Date', widget=widgets.DateWidget('%Y-%m-%d'))
    filing_delay_days = fields.Field(attribute='filing_delay_days', column_name='Filing Delay (Days)')
    gstin = fields.Field(attribute='gstin', column_name='GSTIN')
    taxpayer_name = fields.Field(attribute='taxpayer_name', column_name='Taxpayer Name')
    dzongkhag = fields.Field(attribute='dzongkhag', column_name='Dzongkhag')
    organisation_type = fields.Field(attribute='organisation_type', column_name='Organisation Type')
    frequency = fields.Field(attribute='frequency', column_name='Frequency')
    declared_sales = fields.Field(attribute='declared_sales', column_name='Declared Sales')
    declared_domestic_purchase = fields.Field(attribute='declared_domestic_purchase', column_name='Declared Domestic Purchase/Taxable Expenses')
    declared_import_value = fields.Field(attribute='declared_import_value', column_name='Declared Import Value')
    ecms_import_value = fields.Field(attribute='ecms_import_value', column_name='eCMS Import Value')
    declared_import_gst = fields.Field(attribute='declared_import_gst', column_name='Declared Import GST')
    domestic_purchase_itc_claimed = fields.Field(attribute='domestic_purchase_itc_claimed', column_name='Domestic Purchase ITC  Claimed')
    total_itc_claimed = fields.Field(attribute='total_itc_claimed', column_name='Total ITC Claimed')
    declared_output_gst = fields.Field(attribute='declared_output_gst', column_name='Declared Output GST')
    gst_payable_refundable = fields.Field(attribute='gst_payable_refundable', column_name='GST Payable / Refundable (GST Return)')
    actual_gst_payment_received = fields.Field(attribute='actual_gst_payment_received', column_name='Actual GST Payment Received')
    bank_deposits = fields.Field(attribute='bank_deposits', column_name='Bank Deposits')
    filing_status = fields.Field(attribute='filing_status', column_name='Filing Status')
    payment_status = fields.Field(attribute='payment_status', column_name='Payment Status')
    compliance_status = fields.Field(attribute='compliance_status', column_name='Compliance Status')
    remarks = fields.Field(attribute='remarks', column_name='Remarks')
    
    class Meta:
        model = GSTReturn
        skip_unchanged = False
        report_skipped = True
        import_id_fields = []

class NotFileResource(resources.ModelResource):
    class Meta:
        model = NotFile
        skip_unchanged = False
        report_skipped = True