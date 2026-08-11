import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from returns.models import GSTReturn, NotFile

# Mapping for organization types
org_type_mapping = {
    'sole_proprietorship': 'Sole Proprietorship',
    'private_company': 'Private Company',
    'public_company': 'Public Company',
    'partnership': 'Partnership',
    'llp': 'Limited Liability Partnership',
    'trust': 'Trust',
    'government': 'Government Entity',
    'other': 'Other',
}

# Mapping for dzongkhag
dzongkhag_mapping = {
    'mongar': 'Mongar',
    'trashigang': 'Trashigang',
    'trashiyangtse': 'Trashiyangtse',
    'lhuntse': 'Lhuentse',
}

# Mapping for frequency
frequency_mapping = {
    'monthly': 'Monthly',
    'quarterly': 'Quarterly',
    'annual': 'Annual',
}

# Mapping for filing status
filing_status_mapping = {
    'filed': 'Filed',
    'not_filed': 'Not Filed',
    'extension': 'Extension',
    'due': 'Due',
    'over_due': 'Over Due',
}

# Mapping for payment status
payment_status_mapping = {
    'paid': 'Paid',
    'not_paid': 'Not paid',
    'credit': 'Credit',
    'zero_return': 'Zero Return',
    'reconciled': 'Reconciled Output Input',
    'pending': 'Pending',
    'partial': 'Partial Payment',
}

# Mapping for compliance status
compliance_status_mapping = {
    'compliant': 'Compliant',
    'late_filer': 'Late Filer',
    'late_payment': 'Late payment',
    'non_filer': 'Non-Filer',
    'return_amended': 'Return Amended',
    'under_review': 'Under Review',
}

print("Updating GSTReturn records...")
total = GSTReturn.objects.count()
updated = 0

for record in GSTReturn.objects.all():
    if record.organisation_type in org_type_mapping:
        record.organisation_type = org_type_mapping[record.organisation_type]
        updated += 1
    
    if record.dzongkhag in dzongkhag_mapping:
        record.dzongkhag = dzongkhag_mapping[record.dzongkhag]
        updated += 1
    
    if record.frequency in frequency_mapping:
        record.frequency = frequency_mapping[record.frequency]
        updated += 1
    
    if record.filing_status in filing_status_mapping:
        record.filing_status = filing_status_mapping[record.filing_status]
        updated += 1
    
    if record.payment_status in payment_status_mapping:
        record.payment_status = payment_status_mapping[record.payment_status]
        updated += 1
    
    if record.compliance_status in compliance_status_mapping:
        record.compliance_status = compliance_status_mapping[record.compliance_status]
        updated += 1
    
    record.save()

print(f"Updated {updated} fields in {total} GSTReturn records")

print("\nUpdating NotFile records...")
total = NotFile.objects.count()
updated = 0

for record in NotFile.objects.all():
    if record.organisation_type in org_type_mapping:
        record.organisation_type = org_type_mapping[record.organisation_type]
        updated += 1
    
    if record.dzongkhag in dzongkhag_mapping:
        record.dzongkhag = dzongkhag_mapping[record.dzongkhag]
        updated += 1
    
    if record.filing_status in filing_status_mapping:
        record.filing_status = filing_status_mapping[record.filing_status]
        updated += 1
    
    if record.payment_status in payment_status_mapping:
        record.payment_status = payment_status_mapping[record.payment_status]
        updated += 1
    
    record.save()

print(f"Updated {updated} fields in {total} NotFile records")

print("\n✅ Data update complete")