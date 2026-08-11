import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from taxpayers.models import TaxpayerMaster

# Count current records
total = TaxpayerMaster.objects.count()
print(f"Current total records: {total}")

# Delete all records
if total > 0:
    TaxpayerMaster.objects.all().delete()
    print(f"Deleted {total} records successfully")
else:
    print("No records to delete")

# Verify deletion
remaining = TaxpayerMaster.objects.count()
print(f"Remaining records after deletion: {remaining}")

if remaining == 0:
    print("Database is now clean and ready for fresh import")
else:
    print(f"{remaining} records still remain")