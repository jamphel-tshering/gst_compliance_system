import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from returns.models import GSTReturn
from datetime import datetime

print("Updating tax_period to YYYY-MM-DD format (to match Taxpayer Master)...")
total = GSTReturn.objects.count()
updated = 0

for record in GSTReturn.objects.all():
    if record.tax_period:
        try:
            # Try to parse different formats and convert to YYYY-MM-DD
            date_str = str(record.tax_period).strip()
            
            # Try quarterly format first: "Jan-Mar 2026"
            if '-' in date_str and ' ' in date_str:
                parts = date_str.split(' ')
                if len(parts) == 2:
                    year = parts[1]
                    quarter = parts[0]
                    # Convert quarterly to start month
                    if quarter == 'Jan-Mar':
                        date_str = f"{year}-01-01"
                    elif quarter == 'Apr-Jun':
                        date_str = f"{year}-04-01"
                    elif quarter == 'Jul-Sep':
                        date_str = f"{year}-07-01"
                    elif quarter == 'Oct-Dec':
                        date_str = f"{year}-10-01"
            
            # Try monthly format: "May-2026"
            elif '-' in date_str:
                parts = date_str.split('-')
                if len(parts) == 2:
                    year = parts[1]
                    month = parts[0]
                    # Convert month to number
                    months = {
                        'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
                        'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
                        'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
                    }
                    month_num = months.get(month, '01')
                    date_str = f"{year}-{month_num}-01"
            
            # Parse the date
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            record.tax_period = date_obj.strftime('%Y-%m-%d')
            record.save()
            updated += 1
        except Exception as e:
            print(f"Error processing tax_period '{record.tax_period}': {e}")

print(f"Updated {updated} tax_period fields in {total} GSTReturn records")
print("Tax period format update complete")