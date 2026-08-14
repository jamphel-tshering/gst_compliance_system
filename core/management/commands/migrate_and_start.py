from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Run migrations and create superuser if needed'

    def handle(self, *args, **options):
        self.stdout.write('Running migrations...')
        call_command('migrate', '--noinput')
        self.stdout.write(self.style.SUCCESS('Migrations completed successfully!'))
        
        # Create superuser if not exists
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@gst-system.local',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS('Superuser created: admin/admin123'))
        else:
            self.stdout.write('Superuser already exists')
