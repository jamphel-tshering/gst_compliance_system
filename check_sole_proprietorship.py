import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from taxpayers.models import TaxpayerMaster

# Check all Sole Proprietorship records regardless of status
sole_proprietorship_all = TaxpayerMaster.objects.filter(organisation_type='Sole Proprietorship')
print(f"Sole Proprietorship (all records): {sole_proprietorship_all.count()}")

# Check by status
sole_proprietorship_active = TaxpayerMaster.objects.filter(organisation_type='Sole Proprietorship', status='Active')
print(f"Sole Proprietorship (active): {sole_proprietorship_active.count()}")

sole_proprietorship_deregistered = TaxpayerMaster.objects.filter(organisation_type='Sole Proprietorship', status='Deregistered')
print(f"Sole Proprietorship (deregistered): {sole_proprietorship_deregistered.count()}")

# Check other statuses
other_statuses = TaxpayerMaster.objects.filter(organisation_type='Sole Proprietorship').exclude(status__in=['Active', 'Deregistered'])
print(f"Sole Proprietorship (other statuses): {other_statuses.count()}")

# Check by primary license status
sole_proprietorship_primary = TaxpayerMaster.objects.filter(organisation_type='Sole Proprietorship', is_primary_license=True)
print(f"Sole Proprietorship (primary licenses): {sole_proprietorship_primary.count()}")

sole_proprietorship_additional = TaxpayerMaster.objects.filter(organisation_type='Sole Proprietorship', is_primary_license=False)
print(f"Sole Proprietorship (additional licenses): {sole_proprietorship_additional.count()}")

# Show the non-active records
print("\nNon-active Sole Proprietorship records:")
non_active = TaxpayerMaster.objects.filter(organisation_type='Sole Proprietorship').exclude(status='Active')
for record in non_active:
    print(f"GSTIN: {record.gstin}, Name: {record.taxpayer_name}, Status: {record.status}, Dzongkhag: {record.dzongkhag}")