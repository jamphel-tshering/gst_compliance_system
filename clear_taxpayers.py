import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from taxpayers.models import TaxpayerMaster

# Delete all existing taxpayer records
count = TaxpayerMaster.objects.count()
TaxpayerMaster.objects.all().delete()
print(f"Deleted {count} taxpayer records")