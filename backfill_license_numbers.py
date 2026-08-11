import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from taxpayers.models import MultipleLicenseReference
import time

# Get all records without license numbers
records_without_license = (MultipleLicenseReference.objects.filter(license_number__isnull=True) | 
                          MultipleLicenseReference.objects.filter(license_number=''))
print(f"Found {records_without_license.count()} records without license numbers")

# Backfill license numbers
count = 0
for record in records_without_license:
    gstin = record.gstin if record.gstin else 'UNKNOWN'
    timestamp = int(time.time()) + count  # Add index to ensure uniqueness
    record.license_number = f"{gstin}-{timestamp}"
    record.save()
    count += 1
    if count % 50 == 0:
        print(f"Updated {count} records...")

print(f"\nSuccessfully backfilled {count} records with license numbers")