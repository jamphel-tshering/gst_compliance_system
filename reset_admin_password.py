import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from core.models import User

# Reset admin password
admin = User.objects.get(username='admin')
admin.set_password('admin123')
admin.save()

print("Admin password has been reset to: admin123")
print("Username: admin")
print("Password: admin123")
print("Email: admin@gst-system.local")
