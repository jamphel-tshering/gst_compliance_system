from import_export import fields, resources, widgets
from .models import GSTReturn, NotFile
from datetime import datetime
from decimal import Decimal

class DecimalWidget(widgets.Widget):
    """Custom widget to handle float to Decimal conversion"""
    def clean(self, value, row=None, **kwargs):
        if value is None or value == '':
            return Decimal('0')
        try:
            return Decimal(str(value))
        except:
            return Decimal('0')

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
    declared_sales = fields.Field(attribute='declared_sales', column_name='Declared Sales', widget=DecimalWidget())
    declared_domestic_purchase = fields.Field(attribute='declared_domestic_purchase', column_name='Declared Domestic Purchase/Taxable Expenses', widget=DecimalWidget())
    declared_import_value = fields.Field(attribute='declared_import_value', column_name='Declared Import Value', widget=DecimalWidget())
    ecms_import_value = fields.Field(attribute='ecms_import_value', column_name='eCMS Import Value', widget=DecimalWidget())
    declared_import_gst = fields.Field(attribute='declared_import_gst', column_name='Declared Import GST', widget=DecimalWidget())
    domestic_purchase_itc_claimed = fields.Field(attribute='domestic_purchase_itc_claimed', column_name='Domestic Purchase ITC  Claimed', widget=DecimalWidget())
    total_itc_claimed = fields.Field(attribute='total_itc_claimed', column_name='Total ITC Claimed', widget=DecimalWidget())
    declared_output_gst = fields.Field(attribute='declared_output_gst', column_name='Declared Output GST', widget=DecimalWidget())
    gst_payable_refundable = fields.Field(attribute='gst_payable_refundable', column_name='GST Payable / Refundable (GST Return)', widget=DecimalWidget())
    actual_gst_payment_received = fields.Field(attribute='actual_gst_payment_received', column_name='Actual GST Payment Received', widget=DecimalWidget())
    bank_deposits = fields.Field(attribute='bank_deposits', column_name='Bank Deposits', widget=DecimalWidget())
    filing_status = fields.Field(attribute='filing_status', column_name='Filing Status')
    payment_status = fields.Field(attribute='payment_status', column_name='Payment Status')
    compliance_status = fields.Field(attribute='compliance_status', column_name='Compliance Status')
    remarks = fields.Field(attribute='remarks', column_name='Remarks')
    
    def before_import_row(self, row, **kwargs):
        # Handle empty filing_delay_days values
        if not row.get('Filing Delay (Days)'):
            row['Filing Delay (Days)'] = 0
        
        # Handle empty numeric fields - set to 0
        numeric_fields = [
            'Declared Sales', 'Declared Domestic Purchase/Taxable Expenses', 
            'Declared Import Value', 'eCMS Import Value', 'Declared Import GST',
            'Domestic Purchase ITC  Claimed', 'Total ITC Claimed', 
            'Declared Output GST', 'GST Payable / Refundable (GST Return)',
            'Actual GST Payment Received', 'Bank Deposits'
        ]
        
        for field in numeric_fields:
            if not row.get(field):
                row[field] = 0
        
        # Handle tax_period format - keep as Jan-2026 format
        tax_period = row.get('Tax Period')
        if tax_period:
            try:
                # If already in Jan-2026 format, keep as is
                date_str = str(tax_period).strip()
                if '-' in date_str and len(date_str.split('-')) == 2:
                    # Check if it's already in month-year format
                    month, year = date_str.split('-')
                    # Validate it's a month name
                    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                    if month in month_names:
                        row['Tax Period'] = date_str  # Keep as Jan-2026 format
                    else:
                        # Try to convert from date format
                        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                        row['Tax Period'] = date_obj.strftime('%b-%Y')
                else:
                    # Try to parse as date and convert to Jan-2026 format
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    row['Tax Period'] = date_obj.strftime('%b-%Y')
            except:
                # If not a date, keep as is
                pass
        
        return row
    
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