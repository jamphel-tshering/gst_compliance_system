import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from taxpayers.models import TaxpayerMaster

# Check the lowercase "sole Proprietorship" record
lowercase_sole = TaxpayerMaster.objects.filter(organisation_type='sole Proprietorship')
print(f"Records with 'sole Proprietorship' (lowercase): {lowercase_sole.count()}")

for record in lowercase_sole:
    print(f"\nDetails:")
    print(f"GSTIN: {record.gstin}")
    print(f"Name: {record.taxpayer_name}")
    print(f"Status: {record.status}")
    print(f"Dzongkhag: {record.dzongkhag}")
    print(f"Organisation Type: {record.organisation_type}")

# Check all records with different capitalization of Sole Proprietorship
print("\nAll Sole Proprietorship variations:")
from django.db.models import Count
sole_variations = TaxpayerMaster.objects.filter(organisation_type__icontains='sole proprietorship').values('organisation_type').annotate(count=Count('id'))
for item in sole_variations:
    org = item['organisation_type'] if item['organisation_type'] else 'NULL'
    print(f"{org}: {item['count']}")