import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from returns.models import GSTReturn
from django.db.models import Count

# Check all unique values for each choice field
print("Unique Organization Types:")
org_types = GSTReturn.objects.values('organisation_type').annotate(count=Count('id')).order_by('-count')
for item in org_types:
    org = item['organisation_type'] if item['organisation_type'] else 'NULL'
    print(f"  {org}: {item['count']}")

print("\nUnique Dzongkhag:")
dzongkhags = GSTReturn.objects.values('dzongkhag').annotate(count=Count('id')).order_by('-count')
for item in dzongkhags:
    dzongkhag = item['dzongkhag'] if item['dzongkhag'] else 'NULL'
    print(f"  {dzongkhag}: {item['count']}")

print("\nUnique Frequency:")
frequencies = GSTReturn.objects.values('frequency').annotate(count=Count('id')).order_by('-count')
for item in frequencies:
    freq = item['frequency'] if item['frequency'] else 'NULL'
    print(f"  {freq}: {item['count']}")

print("\nUnique Filing Status:")
filing_statuses = GSTReturn.objects.values('filing_status').annotate(count=Count('id')).order_by('-count')
for item in filing_statuses:
    status = item['filing_status'] if item['filing_status'] else 'NULL'
    print(f"  {status}: {item['count']}")

print("\nUnique Payment Status:")
payment_statuses = GSTReturn.objects.values('payment_status').annotate(count=Count('id')).order_by('-count')
for item in payment_statuses:
    status = item['payment_status'] if item['payment_status'] else 'NULL'
    print(f"  {status}: {item['count']}")

print("\nUnique Compliance Status:")
compliance_statuses = GSTReturn.objects.values('compliance_status').annotate(count=Count('id')).order_by('-count')
for item in compliance_statuses:
    status = item['compliance_status'] if item['compliance_status'] else 'NULL'
    print(f"  {status}: {item['count']}")