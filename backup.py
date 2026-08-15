"""
Automated Backup Script for GST Compliance System
Backs up database and code to local backup folder
"""
import os
import shutil
import subprocess
from datetime import datetime
import zipfile

# Configuration
PROJECT_DIR = r"C:\Users\jamphelt_mongar\gst_compliance_system"
BACKUP_DIR = os.path.join(PROJECT_DIR, "backups")
DB_FILE = os.path.join(PROJECT_DIR, "db.sqlite3")

def create_backup_dir():
    """Create backup directory if it doesn't exist"""
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        print(f"Created backup directory: {BACKUP_DIR}")

def backup_database():
    """Backup SQLite database"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"database_backup_{timestamp}.sqlite3"
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    
    if os.path.exists(DB_FILE):
        shutil.copy2(DB_FILE, backup_path)
        print(f"✅ Database backed up: {backup_name}")
        return backup_path
    else:
        print("⚠️  Database file not found")
        return None

def backup_code():
    """Backup code using Git"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"code_backup_{timestamp}"
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    
    try:
        # Create a git archive
        subprocess.run(
            ["git", "archive", "--format=zip", f"--output={backup_path}.zip", "HEAD"],
            cwd=PROJECT_DIR,
            check=True,
            capture_output=True
        )
        print(f"✅ Code backed up: {backup_name}.zip")
        return f"{backup_name}.zip"
    except subprocess.CalledProcessError as e:
        print(f"❌ Code backup failed: {e}")
        return None

def create_full_backup():
    """Create full backup package"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"full_backup_{timestamp}.zip"
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    
    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add database
        if os.path.exists(DB_FILE):
            zipf.write(DB_FILE, "db.sqlite3")
            print("✅ Added database to backup")
        
        # Add important files
        important_files = [
            "requirements.txt",
            "Procfile",
            ".env.example",
            "README.md",
            "AGENTS.md"
        ]
        
        for file in important_files:
            file_path = os.path.join(PROJECT_DIR, file)
            if os.path.exists(file_path):
                zipf.write(file_path, file)
                print(f"✅ Added {file} to backup")
        
        # Add code directories
        for dir_name in ["core", "taxpayers", "returns", "compliance", "audit_refund", "reporting", "refunds", "static", "templates"]:
            dir_path = os.path.join(PROJECT_DIR, dir_name)
            if os.path.exists(dir_path):
                for root, dirs, files in os.walk(dir_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, PROJECT_DIR)
                        zipf.write(file_path, arcname)
        
        print(f"✅ Full backup created: {backup_name}")
        return backup_path

def main():
    """Main backup function"""
    print("=" * 60)
    print("GST COMPLIANCE SYSTEM - BACKUP SCRIPT")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    create_backup_dir()
    
    print("\n📊 Select Backup Type:")
    print("1. Database Only")
    print("2. Code Only (Git Archive)")
    print("3. Full Backup (Database + Code)")
    print("4. All Backups")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        backup_database()
    elif choice == "2":
        backup_code()
    elif choice == "3":
        create_full_backup()
    elif choice == "4":
        backup_database()
        backup_code()
        create_full_backup()
    else:
        print("❌ Invalid choice")
    
    print("\n" + "=" * 60)
    print(f"Backups saved to: {BACKUP_DIR}")
    print("=" * 60)

if __name__ == "__main__":
    main()