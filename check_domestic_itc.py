import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from returns.models import GSTReturn

# Check sample records to see Domestic Purchase ITC Claimed data
print("Sample GSTReturn records with Domestic Purchase ITC Claimed:")
for record in GSTReturn.objects.all()[:5]:
    print(f"GSTIN: {record.gstin}")
    print(f"Declared Domestic Purchase: {record.declared_domestic_purchase}")
    print(f"Domestic Purchase ITC Claimed: {record.domestic_purchase_itc_claimed}")
    print("---")