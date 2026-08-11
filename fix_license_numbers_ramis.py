import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from taxpayers.models import MultipleLicenseReference

# Update all records to use RAMIS TPN as license number
total = MultipleLicenseReference.objects.count()
print(f"Updating {total} records to use RAMIS TPN as license number")

count = 0
for record in MultipleLicenseReference.objects.all():
    if record.ramis_tpn:
        record.license_number = record.ramis_tpn
        record.save()
        count += 1
        if count % 50 == 0:
            print(f"Updated {count} records...")
    else:
        # If no RAMIS TPN, use GSTIN as fallback
        if record.gstin:
            record.license_number = record.gstin
            record.save()
            count += 1
            if count % 50 == 0:
                print(f"Updated {count} records...")

print(f"\nSuccessfully updated {count} records to use RAMIS TPN as license number")