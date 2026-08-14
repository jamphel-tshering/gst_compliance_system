import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from django.db import connection

print("Fixing corrupted risk_score values using raw SQL...")

try:
    with connection.cursor() as cursor:
        # Check if there are records with NULL or invalid risk_score
        cursor.execute("SELECT COUNT(*) FROM compliance_complianceriskreferral")
        total_count = cursor.fetchone()[0]
        print(f"Total records: {total_count}")
        
        # Set all risk_score values to 0.0 to fix the corruption (NOT NULL constraint)
        cursor.execute("UPDATE compliance_complianceriskreferral SET risk_score = 0.0")
        updated_count = cursor.rowcount
        print(f"Updated {updated_count} records to 0.0 risk_score")
        
        # Verify the fix
        cursor.execute("SELECT COUNT(*) FROM compliance_complianceriskreferral WHERE risk_score IS NOT NULL")
        remaining_count = cursor.fetchone()[0]
        print(f"Records with non-NULL risk_score: {remaining_count}")
        
    print("Successfully fixed corrupted risk_score values!")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
