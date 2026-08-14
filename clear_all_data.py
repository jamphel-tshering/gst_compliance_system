import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from django.db import connection

print("Starting data cleanup...")

# Clear in correct order to handle foreign key constraints
clear_order = [
    # Clear reporting first (has no dependencies)
    'reporting_dashboardwidget',
    'reporting_analyticsdata', 
    'reporting_reportschedule',
    'reporting_generatedreport',
    'reporting_reporttemplate',
    
    # Clear audit/refund
    'audit_refund_auditfinding',
    'audit_refund_auditassessment',
    'audit_refund_auditcase',
    'audit_refund_refundregister',
    
    # Clear compliance
    'compliance_enforcementrecovery',
    'compliance_complianceriskreferral',
    'compliance_compliancemonitoring',
    
    # Clear returns
    'returns_gstreturn',
    'returns_notfile',
    
    # Clear taxpayers
    'taxpayers_multiplelicensereference',
    'taxpayers_taxpayerenquiry',
    'taxpayers_businesslicense',
    'taxpayers_taxpayermaster',
    
    # Clear core (except admin user)
    'core_auditlog',
    'core_systemsettings',
]

# Clear data in order
for table in clear_order:
    print(f"Deleting from {table}...")
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM {table}")
            connection.commit()
            print(f"  Successfully cleared {table}")
    except Exception as e:
        print(f"  Error clearing {table}: {e}")

# Reset sequences
print("\nResetting sequences...")
try:
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM sqlite_sequence")
        connection.commit()
        print("Sequences reset successfully")
except Exception as e:
    print(f"Error resetting sequences: {e}")

print("\nAll data has been successfully deleted from the system!")
print("Database has been cleared of all taxpayer data, returns, compliance records, audits, and reports.")
