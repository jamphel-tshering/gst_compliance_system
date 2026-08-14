import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from django.db import connection

# Delete existing test data
with connection.cursor() as cursor:
    cursor.execute('DELETE FROM compliance_complianceriskreferral WHERE gstin LIKE "TEST%" OR gstin LIKE "CRIT%"')
    print('Deleted existing test data (TEST and CRIT prefixes)')

print('Now run create_test_risk_data.py to create new test data')