from django.core.management.base import BaseCommand
from django.conf import settings
import os
import shutil
from datetime import datetime

class Command(BaseCommand):
    help = 'Create manual backup of the SQLite database'

    def handle(self, *args, **options):
        # Get database path
        db_path = settings.DATABASES['default']['NAME']
        
        # Create backup directory
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        
        # Create backup filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'gst_compliance_backup_{timestamp}.db'
        backup_path = os.path.join(backup_dir, backup_filename)
        
        # Copy database file
        try:
            shutil.copy2(db_path, backup_path)
            self.stdout.write(self.style.SUCCESS(f'✓ Backup created: {backup_filename}'))
            self.stdout.write(f'  Size: {os.path.getsize(backup_path) / 1024:.2f} KB')
            self.stdout.write(f'  Location: {backup_dir}')
            
            # List all backups
            backups = sorted([f for f in os.listdir(backup_dir) if f.startswith('gst_compliance_backup_')])
            self.stdout.write(f'\n  Total backups: {len(backups)}')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Backup failed: {e}'))
