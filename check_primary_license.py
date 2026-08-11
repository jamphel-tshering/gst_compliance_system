import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from taxpayers.models import TaxpayerMaster

# Check current state of is_primary_license field
total = TaxpayerMaster.objects.count()
primary_count = TaxpayerMaster.objects.filter(is_primary_license=True).count()
additional_count = TaxpayerMaster.objects.filter(is_primary_license=False).count()
null_count = TaxpayerMaster.objects.filter(is_primary_license__isnull=True).count()

print(f"Total records: {total}")
print(f"Primary licenses (is_primary_license=True): {primary_count}")
print(f"Additional licenses (is_primary_license=False): {additional_count}")
print(f"Null is_primary_license: {null_count}")

# Check if there are duplicate GSTINs
from django.db.models import Count
duplicates = TaxpayerMaster.objects.values('gstin').annotate(count=Count('gstin')).filter(count__gt=1)
print(f"\nDuplicate GSTINs: {duplicates.count()}")

if duplicates.exists():
    print("\nFirst 10 duplicate GSTINs:")
    for dup in duplicates[:10]:
        print(f"GSTIN: {dup['gstin']}, Count: {dup['count']}")