import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from taxpayers.models import TaxpayerMaster

# Check sample records to see date format
print("Sample TaxpayerMaster records with dates:")
for record in TaxpayerMaster.objects.all()[:5]:
    print(f"GSTIN: {record.gstin}")
    print(f"Registration Date: {record.registration_date}")
    print(f"Commencement Date: {record.commencement_date}")
    print(f"Deregistration Date: {record.deregistration_date}")
    print("---")