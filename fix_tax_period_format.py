import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from returns.models import GSTReturn
from datetime import datetime

print("Updating tax_period format to match Taxpayer Master (YYYY-MM-DD)...")
total = GSTReturn.objects.count()
updated = 0

for record in GSTReturn.objects.all():
    if record.tax_period:
        try:
            # Try to parse various date formats and convert to YYYY-MM-DD
            date_str = str(record.tax_period).strip()
            
            # Remove time component if present
            if ' ' in date_str:
                date_str = date_str.split(' ')[0]
            
            # Try different date formats
            date_formats = [
                '%Y-%m-%d',  # 2026-05-01
                '%b-%Y',      # May-2026
                '%B-%Y',      # May-2026
            ]
            
            for fmt in date_formats:
                try:
                    date_obj = datetime.strptime(date_str, fmt)
                    record.tax_period = date_obj.strftime('%Y-%m-%d')
                    record.save()
                    updated += 1
                    break
                except:
                    continue
        except:
            # If not a date, keep as is
            pass

print(f"Updated {updated} tax_period fields in {total} GSTReturn records")
print("Tax period format update complete")