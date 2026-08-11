"""
Script to update old choice values in the database to match new choices
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from taxpayers.models import TaxpayerMaster

# Update old frequency values
print("Updating frequency values...")
old_frequency_mapping = {
    'annual': 'half_yearly'  # Change Annual to Half Yearly
}

for taxpayer in TaxpayerMaster.objects.all():
    if taxpayer.frequency in old_frequency_mapping:
        taxpayer.frequency = old_frequency_mapping[taxpayer.frequency]
        taxpayer.save()
        print(f"Updated {taxpayer.taxpayer_name}: frequency {taxpayer.frequency}")

# Update old organisation type values
print("\nUpdating organisation type values...")
old_org_mapping = {
    'llp': 'other',  # Change LLP to Other
    'trust': 'other'  # Change Trust to Other
}

for taxpayer in TaxpayerMaster.objects.all():
    if taxpayer.organisation_type in old_org_mapping:
        taxpayer.organisation_type = old_org_mapping[taxpayer.organisation_type]
        taxpayer.save()
        print(f"Updated {taxpayer.taxpayer_name}: organisation_type {taxpayer.organisation_type}")

print("\nUpdate complete!")
