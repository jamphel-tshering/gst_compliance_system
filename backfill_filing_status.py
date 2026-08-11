import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from returns.models import GSTReturn
from datetime import date, datetime, timedelta
import calendar

print("Backfilling filing status and due dates...")
total = GSTReturn.objects.count()
updated_status = 0
updated_due_date = 0

for record in GSTReturn.objects.all():
    # Auto-calculate return_due_date from tax_period if not set
    if record.tax_period and not record.return_due_date:
        try:
            tax_date = datetime.strptime(str(record.tax_period), '%Y-%m-%d').date()
            # Due date = End of tax period + 30 days
            if record.frequency == 'Monthly':
                # Get last day of the month
                last_day = calendar.monthrange(tax_date.year, tax_date.month)[1]
                end_of_month = date(tax_date.year, tax_date.month, last_day)
            elif record.frequency == 'Quarterly':
                # For quarterly, end is 3 months from start
                end_date = tax_date + timedelta(days=90)
                last_day = calendar.monthrange(end_date.year, end_date.month)[1]
                end_of_month = date(end_date.year, end_date.month, last_day)
            else:
                end_of_month = tax_date
            
            record.return_due_date = end_of_month + timedelta(days=30)
            updated_due_date += 1
        except:
            pass
    
    # Auto-calculate filing_status
    if record.return_due_date:
        today = date.today()
        if not record.return_filing_date:
            # No filing date
            if today <= record.return_due_date:
                record.filing_status = 'Due'
            else:
                record.filing_status = 'Overdue / Non-Filer'
        else:
            # Has filing date
            if record.return_filing_date <= record.return_due_date:
                record.filing_status = 'Filed On Time'
            else:
                record.filing_status = 'Late Filer'
        updated_status += 1
    
    record.save()

print(f"Updated {updated_due_date} due dates")
print(f"Updated {updated_status} filing statuses")
print("Backfill complete")