import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from taxpayers.models import TaxpayerMaster
from returns.models import GSTReturn

# Check Taxpayer Master data
print("=== Taxpayer Master Data Analysis ===")
taxpayer_count = TaxpayerMaster.objects.count()
print(f"Total Taxpayers: {taxpayer_count}")

# Check distinct values for choice fields
print("\n--- Organisation Type Values ---")
org_types = TaxpayerMaster.objects.values('organisation_type').distinct()
for org in org_types:
    count = TaxpayerMaster.objects.filter(organisation_type=org['organisation_type']).count()
    print(f"  {org['organisation_type']}: {count}")

print("\n--- Status Values ---")
statuses = TaxpayerMaster.objects.values('status').distinct()
for status in statuses:
    count = TaxpayerMaster.objects.filter(status=status['status']).count()
    print(f"  {status['status']}: {count}")

print("\n--- Frequency Values ---")
frequencies = TaxpayerMaster.objects.values('frequency').distinct()
for freq in frequencies:
    count = TaxpayerMaster.objects.filter(frequency=freq['frequency']).count()
    print(f"  {freq['frequency']}: {count}")

print("\n--- Dzongkhag Values ---")
dzongkhags = TaxpayerMaster.objects.values('dzongkhag').distinct()
for dz in dzongkhags:
    count = TaxpayerMaster.objects.filter(dzongkhag=dz['dzongkhag']).count()
    print(f"  {dz['dzongkhag']}: {count}")

# Sample records to see actual data
print("\n--- Sample Records (first 5) ---")
for i, taxpayer in enumerate(TaxpayerMaster.objects.all()[:5]):
    print(f"\nRecord {i+1}:")
    print(f"  GSTIN: {taxpayer.gstin}")
    print(f"  Organisation Type: '{taxpayer.organisation_type}'")
    print(f"  Status: '{taxpayer.status}'")
    print(f"  Frequency: '{taxpayer.frequency}'")
    print(f"  Dzongkhag: '{taxpayer.dzongkhag}'")
