import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from returns.models import GSTReturn

# Check sample records to see current format
print("Sample GSTReturn records:")
for record in GSTReturn.objects.all()[:5]:
    print(f"Org Type: '{record.organisation_type}'")
    print(f"Dzongkhag: '{record.dzongkhag}'")
    print(f"Frequency: '{record.frequency}'")
    print(f"Filing Status: '{record.filing_status}'")
    print(f"Payment Status: '{record.payment_status}'")
    print(f"Compliance Status: '{record.compliance_status}'")
    print("---")