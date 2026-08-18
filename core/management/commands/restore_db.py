from django.core.management.base import BaseCommand
from django.conf import settings
import os
import shutil
from datetime import datetime

class Command(BaseCommand):
    help = 'Restore SQLite database from a backup file'

    def add_arguments(self, parser):
        parser.add_argument(
            'backup_file',
            type=str,
            help='Backup filename to restore (e.g., gst_compliance_backup_20240818_223000.db)'
        )

    def handle(self, *args, **options):
        backup_filename = options['backup_file']
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        backup_path = os.path.join(backup_dir, backup_filename)
        db_path = settings.DATABASES['default']['NAME']
        
        # Check if backup exists
        if not os.path.exists(backup_path):
            self.stdout.write(self.style.ERROR(f'✗ Backup file not found: {backup_filename}'))
            self.stdout.write('\nAvailable backups:')
            backups = sorted([f for f in os.listdir(backup_dir) if f.startswith('gst_compliance_backup_')], reverse=True)
            for backup in backups:
                self.stdout.write(f'  - {backup}')
            return
        
        # Create a backup of current database before restoring
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        pre_restore_backup = f'pre_restore_{timestamp}.db'
        pre_restore_path = os.path.join(backup_dir, pre_restore_backup)
        
        try:
            shutil.copy2(db_path, pre_restore_path)
            self.stdout.write(self.style.SUCCESS(f'✓ Pre-restore backup created: {pre_restore_backup}'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'⚠ Could not create pre-restore backup: {e}'))
        
        # Restore from backup
        try:
            shutil.copy2(backup_path, db_path)
            self.stdout.write(self.style.SUCCESS(f'✓ Database restored from: {backup_filename}'))
            self.stdout.write(f'  Size: {os.path.getsize(db_path) / 1024:.2f} KB')
            self.stdout.write(f'\n⚠ Please restart the application for changes to take effect')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Restore failed: {e}'))
            self.stdout.write(self.style.ERROR(f'  Pre-restore backup: {pre_restore_backup}'))
