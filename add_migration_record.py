import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
import django
django.setup()
from django.db import connection
cursor = connection.cursor()
cursor.execute("INSERT INTO django_migrations (app, name, applied) VALUES ('compliance', '0001_initial', CURRENT_TIMESTAMP)")
print('Migration record created')