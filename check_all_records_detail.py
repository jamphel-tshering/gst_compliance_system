import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from taxpayers.models import TaxpayerMaster

# Check total records
total = TaxpayerMaster.objects.count()
print(f"Total records in database: {total}")

# Check by organisation type
print("\nOrganisation Type Counts:")
from django.db.models import Count
org_counts = TaxpayerMaster.objects.values('organisation_type').annotate(count=Count('id')).order_by('-count')
for item in org_counts:
    org = item['organisation_type'] if item['organisation_type'] else 'NULL'
    print(f"{org}: {item['count']}")

# Check Sole Proprietorship by all possible statuses
print("\nSole Proprietorship detailed breakdown:")
sole_proprietorship = TaxpayerMaster.objects.filter(organisation_type='Sole Proprietorship')
status_breakdown = sole_proprietorship.values('status').annotate(count=Count('id')).order_by('-count')
for item in status_breakdown:
    status = item['status'] if item['status'] else 'NULL'
    print(f"Status: {status}, Count: {item['count']}")

# Check if there are any records with status='Inactive', 'Suspended', 'Cancelled', etc.
print("\nOther status counts:")
other_statuses = TaxpayerMaster.objects.exclude(status__in=['Active', 'Deregistered']).values('status').annotate(count=Count('id'))
for item in other_statuses:
    status = item['status'] if item['status'] else 'NULL'
    print(f"Status: {status}, Count: {item['count']}")

# Show all records that are not Active and not Deregistered
print("\nRecords with non-standard status:")
non_standard = TaxpayerMaster.objects.exclude(status__in=['Active', 'Deregistered'])
for record in non_standard:
    print(f"GSTIN: {record.gstin}, Name: {record.taxpayer_name}, Status: {record.status}, Organisation: {record.organisation_type}")