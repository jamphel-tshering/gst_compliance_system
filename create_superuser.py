import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from core.models import User

def create_superuser():
    try:
        # Check if superuser already exists
        if User.objects.filter(email='admin@gst-system.local').exists():
            print("Superuser already exists!")
            user = User.objects.get(email='admin@gst-system.local')
            print(f"Email: admin@gst-system.local")
            print(f"Username: {user.username}")
            return
        
        # Create superuser
        user = User.objects.create_user(
            username='admin',
            email='admin@gst-system.local',
            password='admin123',
            first_name='System',
            last_name='Administrator',
            role='admin'
        )
        user.is_superuser = True
        user.is_staff = True
        user.save()
        
        print(f"Superuser created successfully!")
        print(f"Email: admin@gst-system.local")
        print(f"Username: admin")
        print(f"Password: admin123")
        print(f"Please change the password after first login!")
        
    except Exception as e:
        print(f"Error creating superuser: {e}")

if __name__ == '__main__':
    create_superuser()