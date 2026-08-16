"""
Reset superuser password script
Run this to create a new superuser if you forgot your credentials
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Delete existing superuser if exists
try:
    user = User.objects.get(username='jamphel.tshering')
    user.delete()
    print("Old user deleted")
except User.DoesNotExist:
    print("No existing user found")

# Create new superuser
User.objects.create_superuser(
    username='jamphel.tshering',
    email='jimmes2008@gmail.com',
    password='NewPassword@123'
)

print("New superuser created!")
print("Username: jamphel.tshering")
print("Password: NewPassword@123")
print("Please change your password after first login!")