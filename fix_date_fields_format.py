import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from returns.models import GSTReturn
from datetime import datetime

print("Updating return_due_date and return_filing_date to YYYY-MM-DD format...")
total = GSTReturn.objects.count()
updated_due = 0
updated_filing = 0

for record in GSTReturn.objects.all():
    if record.return_due_date:
        try:
            # Remove time component if present
            if isinstance(record.return_due_date, str):
                date_str = record.return_due_date.strip()
                if ' ' in date_str:
                    date_str = date_str.split(' ')[0]
                from datetime import datetime as dt
                date_obj = dt.strptime(date_str, '%Y-%m-%d')
                record.return_due_date = date_obj.date()
                record.save()
                updated_due += 1
            elif hasattr(record.return_due_date, 'hour'):
                # It's a datetime object, convert to date
                record.return_due_date = record.return_due_date.date()
                record.save()
                updated_due += 1
        except:
            pass
    
    if record.return_filing_date:
        try:
            # Remove time component if present
            if isinstance(record.return_filing_date, str):
                date_str = record.return_filing_date.strip()
                if ' ' in date_str:
                    date_str = date_str.split(' ')[0]
                from datetime import datetime as dt
                date_obj = dt.strptime(date_str, '%Y-%m-%d')
                record.return_filing_date = date_obj.date()
                record.save()
                updated_filing += 1
            elif hasattr(record.return_filing_date, 'hour'):
                # It's a datetime object, convert to date
                record.return_filing_date = record.return_filing_date.date()
                record.save()
                updated_filing += 1
        except:
            pass

print(f"Updated {updated_due} return_due_date fields")
print(f"Updated {updated_filing} return_filing_date fields")
print("Date format update complete")