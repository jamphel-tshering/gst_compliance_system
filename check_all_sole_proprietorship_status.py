import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from taxpayers.models import TaxpayerMaster

# Check all Sole Proprietorship records by status
print("Sole Proprietorship records by status:")
sole_proprietorship = TaxpayerMaster.objects.filter(organisation_type='Sole Proprietorship')

from django.db.models import Count
status_counts = sole_proprietorship.values('status').annotate(count=Count('id')).order_by('-count')
for item in status_counts:
    status = item['status'] if item['status'] else 'NULL'
    print(f"{status}: {item['count']}")

# Show all non-active records
print("\nNon-active Sole Proprietorship records:")
non_active = sole_proprietorship.exclude(status='Active')
for record in non_active:
    print(f"GSTIN: {record.gstin}, Name: {record.taxpayer_name}, Status: {record.status}, Dzongkhag: {record.dzongkhag}")

# Check if there are any records with NULL status
null_status = sole_proprietorship.filter(status__isnull=True)
print(f"\nSole Proprietorship with NULL status: {null_status.count()}")

# Check for empty string status
empty_status = sole_proprietorship.filter(status='')
print(f"Sole Proprietorship with empty status: {empty_status.count()}")

# Show the first 10 active records to verify they look correct
print("\nFirst 10 active Sole Proprietorship records:")
active_records = sole_proprietorship.filter(status='Active')[:10]
for record in active_records:
    print(f"GSTIN: {record.gstin}, Name: {record.taxpayer_name}, Status: {record.status}")