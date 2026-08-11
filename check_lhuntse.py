import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from taxpayers.models import TaxpayerMaster

# Check all Lhuntse records regardless of any filters
lhuntse_all = TaxpayerMaster.objects.filter(dzongkhag='Lhuntse')
print(f"Lhuntse (all records): {lhuntse_all.count()}")

# Check Lhuntse by status
lhuntse_active = TaxpayerMaster.objects.filter(dzongkhag='Lhuntse', status='Active')
print(f"Lhuntse (active): {lhuntse_active.count()}")

lhuntse_deregistered = TaxpayerMaster.objects.filter(dzongkhag='Lhuntse', status='Deregistered')
print(f"Lhuntse (deregistered): {lhuntse_deregistered.count()}")

# Check all dzongkhag values in the database
print("\nAll dzongkhag values in database:")
from django.db.models import Count
dzongkhag_counts = TaxpayerMaster.objects.values('dzongkhag').annotate(count=Count('id')).order_by('-count')
for item in dzongkhag_counts:
    dzongkhag = item['dzongkhag'] if item['dzongkhag'] else 'NULL'
    print(f"{dzongkhag}: {item['count']}")

# Check for any records with NULL dzongkhag
null_dzongkhag = TaxpayerMaster.objects.filter(dzongkhag__isnull=True)
print(f"\nRecords with NULL dzongkhag: {null_dzongkhag.count()}")

# Check for any records with empty string dzongkhag
empty_dzongkhag = TaxpayerMaster.objects.filter(dzongkhag='')
print(f"Records with empty string dzongkhag: {empty_dzongkhag.count()}")