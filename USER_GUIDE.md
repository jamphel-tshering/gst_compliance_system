# 👥 GST COMPLIANCE SYSTEM - USER GUIDE

**System:** GST Compliance System  
**Domain:** mongargst.drc.gov.bt  
**Access:** http://127.0.0.1:8001/  
**Status:** ✅ OPERATIONAL

---

## 🔐 **DEFAULT ADMIN LOGIN**

### **Superuser Account:**
- **Email:** admin@drc.gov.bt
- **Username:** admin
- **Password:** Drc@2026

⚠️ **IMPORTANT:** Change this password immediately after first login!

---

## 🚀 **HOW TO START THE SYSTEM**

### **Method 1: Double-Click (Easiest)**
1. Go to your project folder
2. Double-click `start_production.bat`
3. Wait for "Starting Django Production Server..."
4. System will start automatically
5. Access at: http://127.0.0.1:8001/

### **Method 2: Command Line**
1. Open Command Prompt in project folder
2. Run: `python manage.py runserver 127.0.0.1:8001`
3. Access at: http://127.0.0.1:8001/

### **Method 3: PowerShell**
1. Open PowerShell in project folder
2. Run: `python manage.py runserver 127.0.0.1:8001`
3. Access at: http://127.0.0.1:8001/

---

## 📋 **SYSTEM ACCESS POINTS**

### **Main Access URLs:**
- **Home Page:** http://127.0.0.1:8001/
- **Login:** http://127.0.0.1:8001/login/
- **Admin Panel:** http://127.0.0.1:8001/admin/
- **Reports:** http://127.0.0.1:8001/reports/
- **Dashboard:** http://127.0.0.1:8001/admin/dashboard/

---

## 👥 **USER ROLES AND PERMISSIONS**

### **Available Roles:**
1. **Administrator** - Full system access
2. **Section Head** - Department management
3. **Audit and Refund** - Audit and refund operations
4. **Registration Taxpayer Enquiry** - Taxpayer registration
5. **Compliance** - Compliance monitoring

### **Creating New Users:**
1. Login as admin
2. Go to Admin Panel → Core → Users
3. Click "Add User"
4. Fill in user details
5. Assign role and permissions
6. Save

---

## 📊 **MODULE OVERVIEW**

### **1. Taxpayer Management**
- **Access:** Admin Panel → Taxpayers
- **Functions:** 
  - Add new taxpayers
  - Update taxpayer information
  - Manage taxpayer enquiries
  - View taxpayer history

### **2. GST Returns**
- **Access:** Admin Panel → Returns
- **Functions:**
  - File GST returns
  - View return history
  - Process payments
  - Generate return reports

### **3. Compliance & Enforcement**
- **Access:** Admin Panel → Compliance
- **Functions:**
  - Monitor compliance status
  - Run risk assessments
  - Manage enforcement cases
  - Track compliance indicators

### **4. Audit & Refund**
- **Access:** Admin Panel → Audit Refund
- **Functions:**
  - Create audit cases
  - Process refund claims
  - Manage audit assessments
  - Track enforcement recovery

### **5. Reports**
- **Access:** Admin Panel → Reports or http://127.0.0.1:8001/reports/
- **Available Reports:**
  - Executive GST Summary
  - Taxpayer Reports (7 types)
  - GST Return & Revenue Reports (6 types)
  - Compliance Reports (6 types)
  - Risk & Selection Reports (5 types)
  - Audit Reports (7 types)
  - Refund Reports (5 types)
  - Enforcement Reports (5 types)
  - Officer/Workload Reports (3 types)
  - Custom Report Builder

---

## 🔧 **COMMON TASKS**

### **Adding a New Taxpayer:**
1. Go to Admin Panel → Taxpayers → Taxpayer Masters
2. Click "Add Taxpayer Master"
3. Fill in taxpayer details
4. Click "Save"

### **Filing a GST Return:**
1. Go to Admin Panel → Returns → GST Returns
2. Click "Add GST Return"
3. Select taxpayer and tax period
4. Enter return details
5. Click "Save"

### **Running Risk Assessment:**
1. Go to Admin Panel → Compliance → Compliance Risk Referrals
2. Click "Run Risk Assessment"
3. Select tax period
4. System will generate risk scores
5. Review and approve risk selections

### **Creating Audit Case:**
1. Go to Admin Panel → Audit Refund → Audit Cases
2. Click "Add Audit Case"
3. Select risk referral
4. Assign officer and set due date
5. Click "Save"

### **Processing Refund:**
1. Go to Admin Panel → Audit Refund → Refund Registers
2. Click "Add Refund Register"
3. Enter refund details
4. Process and approve
5. Click "Save"

---

## 📈 **DASHBOARD NAVIGATION**

### **Main Dashboard:**
- **GST Reports** - Centralized reporting
- **Compliance & Enforcement** - Compliance monitoring
- **Audit & Refund** - Audit and refund operations
- **Taxpayer Management** - Taxpayer data
- **GST Returns** - Return processing
- **Risk Assessment** - Risk evaluation

### **Admin Dashboard:**
- Shows all modules
- Quick access to all functions
- System statistics
- Recent activities

---

## 🔍 **SEARCHING AND FILTERING**

### **In Admin Panel:**
- Use the search bar at the top
- Filter by date ranges
- Filter by status
- Filter by taxpayer
- Sort by any column

### **In Reports:**
- Use filter dropdowns
- Select tax periods
- Filter by risk levels
- Filter by status
- Export filtered results

---

## 📤 **EXPORTING DATA**

### **Export Reports:**
1. Go to Reports section
2. Select desired report
3. Apply filters if needed
4. Click "Export" button
5. Choose format (Excel, PDF, CSV)

### **Export Admin Data:**
1. Go to any admin section
2. Use the "Export" button
3. Select format
4. Download file

---

## ⚙️ **SYSTEM SETTINGS**

### **Accessing Settings:**
1. Go to Admin Panel → Core → System Settings
2. Update system name, organization details
3. Configure email settings
4. Update contact information
5. Save changes

---

## 🔒 **SECURITY BEST PRACTICES**

### **For Admin Users:**
- Change default password immediately
- Use strong passwords
- Don't share credentials
- Log out after use
- Monitor audit logs regularly

### **For All Users:**
- Keep passwords secure
- Report suspicious activity
- Use only assigned permissions
- Follow data handling procedures

---

## 🆘 **TROUBLESHOOTING**

### **Server Won't Start:**
- Check if port 8001 is available
- Close other Python processes
- Restart the server

### **Can't Login:**
- Check username and password
- Clear browser cache
- Try incognito mode
- Contact admin if locked out

### **Reports Not Loading:**
- Check if server is running
- Refresh the page
- Clear browser cache
- Check internet connection

### **Database Errors:**
- Check if db.sqlite3 exists
- Run migrations: `python manage.py migrate`
- Restart the server

---

## 📞 **SUPPORT CONTACTS**

### **Technical Support:**
- **System Administrator:** [Your IT Department]
- **Database Issues:** [Your DBA Team]
- **Network Issues:** [Your Network Team]

### **Business Support:**
- **GST Operations:** [Your GST Team]
- **Policy Questions:** [Your Policy Team]
- **Training Requests:** [Your Training Team]

---

## 📅 **REGULAR MAINTENANCE**

### **Daily:**
- Check server status
- Monitor error logs
- Verify backup completion

### **Weekly:**
- Review user activities
- Check system performance
- Update security patches

### **Monthly:**
- Review audit logs
- Clean up old data
- Update documentation

### **Quarterly:**
- Security audit
- Performance review
- User training refresh

---

## 🎯 **QUICK REFERENCE**

### **Start System:** Double-click `start_production.bat`
### **Stop System:** Press Ctrl+C in command window
### **Admin Login:** admin@drc.gov.bt / Drc@2026
### **Main URL:** http://127.0.0.1:8001/
### **Admin URL:** http://127.0.0.1:8001/admin/
### **Reports URL:** http://127.0.0.1:8001/reports/

---

## 📝 **IMPORTANT NOTES**

1. **First Action:** Change admin password immediately
2. **Backup:** Regular backup of db.sqlite3
3. **Security:** Keep SECRET_KEY secure
4. **Updates:** Keep Django updated
5. **Monitoring:** Regular system monitoring

---

**🎉 SYSTEM READY FOR USE!**

**Start by:** Double-clicking `start_production.bat`  
**Login with:** admin@drc.gov.bt / Drc@2026  
**Change password:** Immediately after first login

**For questions:** Contact your system administrator