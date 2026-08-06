from import_export import fields, resources, widgets
from .models import TaxpayerMaster

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
    registration_date = fields.Field(attribute='registration_date', column_name='Registration Date', widget=widgets.DateWidget('%Y-%m-%d'))
    commencement_date = fields.Field(attribute='commencement_date', column_name='Commencement Date', widget=widgets.DateWidget('%Y-%m-%d'))
    deregistration_date = fields.Field(attribute='deregistration_date', column_name='Deregistration Date', widget=widgets.DateWidget('%Y-%m-%d'))
    email_address = fields.Field(attribute='email_address', column_name='Email Address')
    mobile_number = fields.Field(attribute='mobile_number', column_name='Mobile Number')
    business_address = fields.Field(attribute='business_address', column_name='Business Address')
    remarks = fields.Field(attribute='remarks', column_name='Remarks')
    
    class Meta:
        model = TaxpayerMaster
        skip_unchanged = False
        report_skipped = True
        import_id_fields = []