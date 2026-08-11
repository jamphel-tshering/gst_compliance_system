import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from returns.models import GSTReturn
from taxpayers.models import TaxpayerMaster

print("Backfilling compliance status...")
total = GSTReturn.objects.count()
updated = 0

for record in GSTReturn.objects.all():
    try:
        taxpayer = TaxpayerMaster.objects.get(gstin=record.gstin)
        if taxpayer.status != 'Active':
            record.compliance_status = 'Inactive Taxpayer'
        elif record.filing_status == 'Overdue / Non-Filer':
            record.compliance_status = 'Non-Filer'
        elif record.filing_status == 'Late Filer':
            record.compliance_status = 'Late Filer'
        elif record.filing_status == 'Filed On Time':
            record.compliance_status = 'Compliant'
        elif record.filing_status == 'Due':
            record.compliance_status = 'Pending'
        else:
            record.compliance_status = 'Compliant'
        updated += 1
    except TaxpayerMaster.DoesNotExist:
        record.compliance_status = 'Unknown Taxpayer'
        updated += 1
    
    record.save()

print(f"Updated {updated} compliance statuses in {total} GSTReturn records")
print("Backfill complete")