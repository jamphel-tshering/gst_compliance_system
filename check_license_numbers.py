import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from taxpayers.models import MultipleLicenseReference

# Check existing records
total = MultipleLicenseReference.objects.count()
print(f"Total Multiple License Reference records: {total}")

# Check records with license numbers
with_license = MultipleLicenseReference.objects.exclude(license_number__isnull=True).exclude(license_number='')
print(f"Records with license numbers: {with_license.count()}")

# Check records without license numbers
without_license = MultipleLicenseReference.objects.filter(license_number__isnull=True) | MultipleLicenseReference.objects.filter(license_number='')
print(f"Records without license numbers: {without_license.count()}")

# Show sample records
print("\nSample records:")
for record in MultipleLicenseReference.objects.all()[:5]:
    print(f"GSTIN: {record.gstin}, License: {record.license_number}, Name: {record.taxpayer_name}")