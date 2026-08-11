import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from taxpayers.models import TaxpayerMaster

# Check remaining records
remaining = TaxpayerMaster.objects.all()
print(f"Total remaining records: {remaining.count()}")

print("\nRemaining records details:")
for record in remaining:
    print(f"GSTIN: {record.gstin}, Name: {record.taxpayer_name}, Status: {record.status}, Dzongkhag: {record.dzongkhag}, Organisation: {record.organisation_type}")

# Check by status
deregistered = TaxpayerMaster.objects.filter(status='Deregistered')
print(f"\nDeregistered records: {deregistered.count()}")

# Other statuses
active = TaxpayerMaster.objects.filter(status='Active')
print(f"Active records: {active.count()}")

other_statuses = TaxpayerMaster.objects.exclude(status__in=['Active', 'Deregistered'])
print(f"Other status records: {other_statuses.count()}")