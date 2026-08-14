import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from compliance.models import ComplianceRiskReferral
from decimal import Decimal, InvalidOperation

print("Checking for corrupted risk_score values...")

try:
    # Try to access records with invalid risk_score
    records = ComplianceRiskReferral.objects.all()
    total_count = records.count()
    print(f"Total records: {total_count}")
    
    corrupted_count = 0
    fixed_count = 0
    
    for record in records:
        try:
            # Try to access the risk_score
            if record.risk_score is not None:
                # Try to convert to Decimal to check validity
                score_value = Decimal(str(record.risk_score))
        except (InvalidOperation, ValueError, TypeError) as e:
            print(f"Found corrupted risk_score in record {record.risk_id}: {record.risk_score}")
            corrupted_count += 1
            # Fix by setting to None or a valid default
            record.risk_score = None
            record.save()
            fixed_count += 1
            print(f"Fixed record {record.risk_id}")
    
    print(f"\nCorrupted records found: {corrupted_count}")
    print(f"Records fixed: {fixed_count}")
    
    if corrupted_count == 0:
        print("No corrupted risk_score values found.")
    else:
        print("All corrupted risk_score values have been fixed.")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
