import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from taxpayers.models import MultipleLicenseReference

# Check total records
total = MultipleLicenseReference.objects.count()
print(f"Total Multiple License Reference records: {total}")

# Check by organization type
print("\nOrganisation Type Counts:")
from django.db.models import Count
org_counts = MultipleLicenseReference.objects.values('organisation_type').annotate(count=Count('id')).order_by('-count')
for item in org_counts:
    org = item['organisation_type'] if item['organisation_type'] else 'NULL'
    print(f"{org}: {item['count']}")

# Check by dzongkhag
print("\nDzongkhag Counts:")
dzongkhag_counts = MultipleLicenseReference.objects.values('dzongkhag').annotate(count=Count('id')).order_by('-count')
for item in dzongkhag_counts:
    dzongkhag = item['dzongkhag'] if item['dzongkhag'] else 'NULL'
    print(f"{dzongkhag}: {item['count']}")

# Check by status
print("\nStatus Counts:")
status_counts = MultipleLicenseReference.objects.values('status').annotate(count=Count('id')).order_by('-count')
for item in status_counts:
    status = item['status'] if item['status'] else 'NULL'
    print(f"{status}: {item['count']}")

# Show sample records
print("\nSample records:")
for record in MultipleLicenseReference.objects.all()[:5]:
    print(f"GSTIN: {record.gstin}, License: {record.license_number}, Name: {record.taxpayer_name}, Org: {record.organisation_type}, Dzongkhag: {record.dzongkhag}, Status: {record.status}")