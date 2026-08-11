from import_export import fields, resources, widgets
from .models import TaxpayerMaster, MultipleLicenseReference
from datetime import datetime

class TaxpayerMasterResource(resources.ModelResource):
    cid_company_reg_no = fields.Field(attribute='cid_company_reg_no', column_name='CID No/Co. Reg No')
    gstin = fields.Field(attribute='gstin', column_name='GSTIN')
    ramis_tpn = fields.Field(attribute='ramis_tpn', column_name='RAMIS TPN')
    taxpayer_name = fields.Field(attribute='taxpayer_name', column_name='Taxpayer Name')
    business_name = fields.Field(attribute='business_name', column_name='Business Name')
    sector = fields.Field(attribute='sector', column_name='Sector')
    sub_sector = fields.Field(attribute='sub_sector', column_name='Sub-Sector')
    business_activity = fields.Field(attribute='business_activity', column_name='Business Activity')
    organisation_type = fields.Field(attribute='organisation_type', column_name='Organisation Type')
    frequency = fields.Field(attribute='frequency', column_name='Frequency')
    dzongkhag = fields.Field(attribute='dzongkhag', column_name='Dzongkhag')
    status = fields.Field(attribute='status', column_name='Status')
    registration_date = fields.Field(attribute='registration_date', column_name='Registration Date')
    commencement_date = fields.Field(attribute='commencement_date', column_name='Commencement Date')
    deregistration_date = fields.Field(attribute='deregistration_date', column_name='Deregistration Date')
    email_address = fields.Field(attribute='email_address', column_name='Email Address')
    mobile_number = fields.Field(attribute='mobile_number', column_name='Mobile Number')
    business_address = fields.Field(attribute='business_address', column_name='Business Address')
    remarks = fields.Field(attribute='remarks', column_name='Remarks')
    
    def parse_date_safely(self, date_value):
        """Safely parse date in multiple formats, return None if invalid"""
        if not date_value:
            return None
        
        # If already a date object, return it
        if isinstance(date_value, datetime):
            return date_value
        
        date_str = str(date_value).strip()
        
        # Try multiple date formats
        date_formats = [
            '%Y-%m-%d',    # 2026-01-15
            '%d-%m-%Y',    # 15-01-2026
            '%m/%d/%Y',    # 01/15/2026
            '%d/%m/%Y',    # 15/01/2026
            '%Y/%m/%d',    # 2026/01/15
        ]
        
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        
        # If all formats fail, return None
        return None
    
    def before_import_row(self, row, **kwargs):
        # Handle empty GSTIN values
        if not row.get('GSTIN'):
            row['GSTIN'] = ''  # Set to empty string instead of None
        
        # Handle empty taxpayer_name values - set to placeholder if missing
        if not row.get('Taxpayer Name'):
            row['Taxpayer Name'] = 'Unknown Taxpayer'
        
        # Handle empty business_name values - set to taxpayer_name as fallback or placeholder
        if not row.get('Business Name'):
            taxpayer_name = row.get('Taxpayer Name', '')
            if taxpayer_name and taxpayer_name != 'Unknown Taxpayer':
                row['Business Name'] = taxpayer_name  # Use taxpayer name as business name
            else:
                row['Business Name'] = 'Unknown Business'  # Fallback placeholder
        
        # Handle date fields - parse safely and set to None if invalid
        for date_field in ['Registration Date', 'Commencement Date', 'Deregistration Date']:
            date_value = row.get(date_field)
            parsed_date = self.parse_date_safely(date_value)
            row[date_field] = parsed_date
        
        return row
    
    class Meta:
        model = TaxpayerMaster
        skip_unchanged = False
        report_skipped = True
        import_id_fields = ['gstin']


class MultipleLicenseResource(resources.ModelResource):
    """Resource for Multiple License References - used for reference purposes"""
    cid_company_reg_no = fields.Field(attribute='cid_company_reg_no', column_name='CID No/Co. Reg No')
    gstin = fields.Field(attribute='gstin', column_name='GSTIN')
    ramis_tpn = fields.Field(attribute='ramis_tpn', column_name='RAMIS TPN')
    license_number = fields.Field(attribute='license_number', column_name='RAMIS TPN')  # Map RAMIS TPN to license_number
    taxpayer_name = fields.Field(attribute='taxpayer_name', column_name='Taxpayer Name')
    business_name = fields.Field(attribute='business_name', column_name='Business Name')
    sector = fields.Field(attribute='sector', column_name='Sector')
    sub_sector = fields.Field(attribute='sub_sector', column_name='Sub-Sector')
    business_activity = fields.Field(attribute='business_activity', column_name='Business Activity')
    organisation_type = fields.Field(attribute='organisation_type', column_name='Organisation Type')
    frequency = fields.Field(attribute='frequency', column_name='Frequency')
    dzongkhag = fields.Field(attribute='dzongkhag', column_name='Dzongkhag')
    status = fields.Field(attribute='status', column_name='Status')
    registration_date = fields.Field(attribute='registration_date', column_name='Registration Date', widget=widgets.DateWidget('%Y-%m-%d'))
    commencement_date = fields.Field(attribute='commencement_date', column_name='Commencement Date', widget=widgets.DateWidget('%Y-%m-%d'))
    deregistration_date = fields.Field(attribute='deregistration_date', column_name='Deregistration Date', widget=widgets.DateWidget('%Y-%m-%d'))
    email_address = fields.Field(attribute='email_address', column_name='Email Address')
    mobile_number = fields.Field(attribute='mobile_number', column_name='Mobile Number')
    business_address = fields.Field(attribute='business_address', column_name='Business Address')
    remarks = fields.Field(attribute='remarks', column_name='Remarks')
    
    def before_import_row(self, row, **kwargs):
        # Handle empty GSTIN values
        if not row.get('GSTIN'):
            row['GSTIN'] = ''  # Set to empty string instead of None
        
        # Handle empty taxpayer_name values - set to placeholder if missing
        if not row.get('Taxpayer Name'):
            row['Taxpayer Name'] = 'Unknown Taxpayer'
        
        # Handle empty business_name values - set to placeholder if missing
        if not row.get('Business Name'):
            row['Business Name'] = ''
        
        # License number is now mapped from RAMIS TPN column
        # No auto-generation needed - will use RAMIS TPN directly
        
        return row
    
    class Meta:
        model = MultipleLicenseReference
        skip_unchanged = False
        report_skipped = True
        # No import_id_fields - allow multiple records with same GSTIN