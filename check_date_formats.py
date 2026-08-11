import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from returns.models import GSTReturn

# Check sample records to see date format
print("Sample GSTReturn records with dates:")
for record in GSTReturn.objects.all()[:5]:
    print(f"Tax Period: {record.tax_period} (type: {type(record.tax_period).__name__})")
    print(f"Return Due Date: {record.return_due_date} (type: {type(record.return_due_date).__name__})")
    print(f"Return Filing Date: {record.return_filing_date} (type: {type(record.return_filing_date).__name__})")
    print("---")