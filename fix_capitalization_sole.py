import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from taxpayers.models import TaxpayerMaster

# Fix the lowercase "sole Proprietorship" record
lowercase_sole = TaxpayerMaster.objects.filter(organisation_type='sole Proprietorship')
print(f"Found {lowercase_sole.count()} records with lowercase 'sole Proprietorship'")

for record in lowercase_sole:
    print(f"Fixing: GSTIN {record.gstin}, Name {record.taxpayer_name}")
    record.organisation_type = 'Sole Proprietorship'
    record.save()

# Verify the fix
print("\nAfter fix:")
proper_case_sole = TaxpayerMaster.objects.filter(organisation_type='Sole Proprietorship')
print(f"Records with 'Sole Proprietorship' (proper case): {proper_case_sole.count()}")

# Check active count
active_sole = TaxpayerMaster.objects.filter(organisation_type='Sole Proprietorship', status='Active')
print(f"Active 'Sole Proprietorship' records: {active_sole.count()}")