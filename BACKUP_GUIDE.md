# Backup Instructions for GST Compliance System

## 📋 Quick Start

### **Option 1: Use the Batch File (Easiest)**
1. Double-click `backup.bat` in your project folder
2. Select backup type (1-4)
3. Backups are saved in the `backups/` folder

### **Option 2: Run the Python Script**
```bash
python backup.py
```

---

## 📊 Backup Types

### **1. Database Only**
- Backs up your SQLite database
- Saves as `database_backup_YYYYMMDD_HHMMSS.sqlite3`
- Use this if you only need to backup data

### **2. Code Only**
- Creates a Git archive of your code
- Saves as `code_backup_YYYYMMDD_HHMMSS.zip`
- Use this if you only need to backup code changes

### **3. Full Backup (Recommended)**
- Backs up database + all code
- Saves as `full_backup_YYYYMMDD_HHMMSS.zip`
- Use this for complete system backup

### **4. All Backups**
- Runs all three backup types
- Use this for comprehensive backup

---

## 📁 Backup Location

All backups are saved in:
```
C:\Users\jamphelt_mongar\gst_compliance_system\backups\
```

---

## 🔄 Backup Schedule Recommendations

### **Personal/Interest Project:**
- **Weekly** full backup
- **Before major changes** full backup
- **After important data entry** database backup

### **When Officially Adopted:**
- **Daily** database backup
- **Weekly** full backup
- **Before updates** full backup
- **Consider cloud storage** for off-site backups

---

## 🎯 How to Restore from Backup

### **Restore Database:**
1. Stop the local server
2. Go to the `backups/` folder
3. Find the database backup file
4. Copy it to your project folder as `db.sqlite3`
5. Restart the server

### **Restore Code:**
1. Go to the `backups/` folder
2. Extract the code backup zip file
3. Copy files to your project folder
4. Or use Git to revert to a specific commit

---

## ☁️ Cloud Backup (Optional)

For extra safety, you can:
1. Copy backup files to Google Drive, Dropbox, or OneDrive
2. Upload to cloud storage services
3. Or sync the `backups/` folder with cloud storage

---

## ⚠️ Important Notes

- **Local database** is only backed up when you run the script
- **Live database** on Render is separate
- To backup live data, use the CSV export buttons in the admin panel
- **GitHub** automatically backs up your code history

---

## 🔧 Live Data Backup

To backup the live production data:

1. Go to: https://gst-compliance-system-19um.onrender.com/admin/
2. Use the report buttons:
   - 📊 Taxpayer CSV
   - 📈 Returns CSV
   - ✓ Compliance CSV
3. Download and save to your backup folder

---

## 📞 Need Help?

If you have issues with backups:
- Check that the backup folder exists
- Ensure you have write permissions
- Verify Python is installed and accessible