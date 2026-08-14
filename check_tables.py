import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
import django
django.setup()
from django.db import connection
cursor = connection.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print([table[0] for table in tables])