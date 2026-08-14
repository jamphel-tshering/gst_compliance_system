import os
import shutil
from datetime import datetime
import sqlite3

def backup_database():
    """Create a backup of the SQLite database"""
    
    # Paths
    db_path = 'C:/Users/jamphelt_mongar/gst_compliance_system/db.sqlite3'
    backup_dir = 'C:/Users/jamphelt_mongar/gst_compliance_system/backups'
    
    # Create backup directory if it doesn't exist
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    # Create backup filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f'gst_compliance_backup_{timestamp}.db'
    backup_path = os.path.join(backup_dir, backup_filename)
    
    # Copy database file
    try:
        shutil.copy2(db_path, backup_path)
        print(f"Backup created successfully: {backup_path}")
        
        # Keep only last 7 backups
        backups = sorted([f for f in os.listdir(backup_dir) if f.startswith('gst_compliance_backup_')])
        while len(backups) > 7:
            old_backup = backups.pop(0)
            os.remove(os.path.join(backup_dir, old_backup))
            print(f"Removed old backup: {old_backup}")
            
        return backup_path
    except Exception as e:
        print(f"Error creating backup: {e}")
        return None

if __name__ == '__main__':
    print("Starting database backup...")
    backup_database()
    print("Backup process completed.")
