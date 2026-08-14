import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from django.db import connection

print("Starting comprehensive data cleanup...")

# Get all tables and clear them in correct order
with connection.cursor() as cursor:
    # Get all user tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = cursor.fetchall()
    
    # Clear tables in order (excluding django tables we want to keep)
    tables_to_clear = []
    django_tables = ['django_migrations', 'django_content_type', 'auth_permission', 'auth_group', 'auth_group_permissions', 'sqlite_sequence']
    
    for table in tables:
        table_name = table[0]
        if table_name not in django_tables:
            tables_to_clear.append(table_name)
    
    # Clear each table
    for table in tables_to_clear:
        print(f"Deleting from {table}...")
        try:
            # Disable foreign key constraints temporarily
            cursor.execute("PRAGMA foreign_keys = OFF")
            cursor.execute(f"DELETE FROM {table}")
            connection.commit()
            print(f"  Successfully cleared {table}")
        except Exception as e:
            print(f"  Error clearing {table}: {e}")
        finally:
            # Re-enable foreign key constraints
            cursor.execute("PRAGMA foreign_keys = ON")

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
print("Database has been cleared of all user data while preserving system tables.")
