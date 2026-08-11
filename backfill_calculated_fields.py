import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from returns.models import GSTReturn
from decimal import Decimal

print("Backfilling calculated fields...")
total = GSTReturn.objects.count()
updated = 0

for record in GSTReturn.objects.all():
    # Auto-calculate declared_import_gst
    if record.declared_import_value:
        record.declared_import_gst = round(record.declared_import_value * Decimal('0.05'), 2)
        updated += 1
    
    # Auto-calculate domestic_purchase_itc_claimed
    if record.declared_domestic_purchase:
        record.domestic_purchase_itc_claimed = round(record.declared_domestic_purchase * Decimal('0.05'), 2)
        updated += 1
    
    # Auto-calculate declared_output_gst
    if record.declared_sales:
        record.declared_output_gst = round(record.declared_sales * Decimal('0.05'), 2)
        updated += 1
    
    # Auto-calculate filing_delay_days
    if record.return_due_date and record.return_filing_date:
        due_date = record.return_due_date
        filing_date = record.return_filing_date
        delay = (filing_date - due_date).days
        record.filing_delay_days = max(0, delay)
        updated += 1
    
    record.save()

print(f"Updated {updated} fields in {total} GSTReturn records")
print("Backfill complete")