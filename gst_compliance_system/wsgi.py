"""
WSGI config for gst_compliance_system project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/wsgi/
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

# Only run migrations and create user on SQLite (for local development)
# PostgreSQL on Render will handle migrations differently to avoid data loss
if os.environ.get('DATABASE_URL') is None:  # SQLite (local)
    # Run migrations on startup
    from django.core.management import call_command
    try:
        call_command('migrate', '--noinput', verbosity=0)
        print("Migrations completed successfully")
    except Exception as e:
        print(f"Migration error: {e}")

    # Create admin user if not exists
    from django.contrib.auth import get_user_model
    User = get_user_model()

    try:
        # Try to find existing user by email or username
        user = User.objects.filter(email='jimmes2008@gmail.com').first()
        if not user:
            user = User.objects.filter(username='jamphel.tshering').first()
        
        if not user:
            # Create new superuser with email as username
            User.objects.create_superuser(
                username='jimmes2008@gmail.com',
                email='jimmes2008@gmail.com',
                password='Admin@123'
            )
            print("Superuser created: jimmes2008@gmail.com / Admin@123")
        else:
            # Update password to ensure it works
            user.set_password('Admin@123')
            user.save()
            print("Superuser password updated: jimmes2008@gmail.com / Admin@123")
    except Exception as e:
        print(f"User creation error: {e}")
        import traceback
        traceback.print_exc()
else:
    print("Using PostgreSQL - skipping automatic migrations and user creation")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
