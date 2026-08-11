import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from taxpayers.models import TaxpayerMaster

# Check current state of data
total = TaxpayerMaster.objects.count()
primary_active = TaxpayerMaster.objects.filter(is_primary_license=True, status='Active').count()
primary_all = TaxpayerMaster.objects.filter(is_primary_license=True).count()

print(f"Total records: {total}")
print(f"Primary licenses (active): {primary_active}")
print(f"Primary licenses (all): {primary_all}")

# Check organisation type counts for primary active licenses
print("\nOrganisation Type Counts (Primary Active):")
for org_type in ['Sole Proprietorship', 'Private Company', 'Public Company', 'Partnership', 'Government Entity', 'Foreign Company', 'Joint Venture', 'State Owned Company', 'Other']:
    count = TaxpayerMaster.objects.filter(organisation_type=org_type, is_primary_license=True, status='Active').count()
    print(f"{org_type}: {count}")

# Check dzongkhag counts for primary active licenses
print("\nDzongkhag Counts (Primary Active):")
for dzongkhag in ['Mongar', 'Trashigang', 'Trashiyangtse', 'Lhuntse']:
    count = TaxpayerMaster.objects.filter(dzongkhag=dzongkhag, is_primary_license=True, status='Active').count()
    print(f"{dzongkhag}: {count}")

# Check for any Lhuntse records regardless of status
print("\nDzongkhag Counts (Primary All):")
for dzongkhag in ['Mongar', 'Trashigang', 'Trashiyangtse', 'Lhuntse']:
    count = TaxpayerMaster.objects.filter(dzongkhag=dzongkhag, is_primary_license=True).count()
    print(f"{dzongkhag}: {count}")

# Check for any Lhuntse records regardless of primary status
print("\nDzongkhag Counts (All Records):")
for dzongkhag in ['Mongar', 'Trashigang', 'Trashiyangtse', 'Lhuntse']:
    count = TaxpayerMaster.objects.filter(dzongkhag=dzongkhag).count()
    print(f"{dzongkhag}: {count}")

# Check for any additional licenses in Lhuntse
print("\nDzongkhag Counts (Additional Licenses):")
for dzongkhag in ['Mongar', 'Trashigang', 'Trashiyangtse', 'Lhuntse']:
    count = TaxpayerMaster.objects.filter(dzongkhag=dzongkhag, is_primary_license=False).count()
    print(f"{dzongkhag}: {count}")