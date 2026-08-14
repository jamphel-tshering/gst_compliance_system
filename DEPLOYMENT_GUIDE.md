# 🚀 GST COMPLIANCE SYSTEM - PRODUCTION DEPLOYMENT GUIDE

**Domain:** mongargst.drc.gov.bt  
**Status:** ✅ Configuration Complete  
**Date:** August 14, 2026

---

## 📋 **CONFIGURATION SUMMARY**

### ✅ **Environment Variables Configured**
- **SECRET_KEY:** ✅ Securely generated and configured
- **DEBUG:** ✅ Set to False for production
- **ALLOWED_HOSTS:** ✅ Configured for mongargst.drc.gov.bt
- **CORS_ALLOWED_ORIGINS:** ✅ Configured for mongargst.drc.gov.bt
- **DATABASE:** ✅ SQLite (easy deployment, can upgrade to PostgreSQL later)
- **TIME_ZONE:** ✅ Set to Asia/Thimphu (Bhutan)
- **Email:** ✅ Placeholder SMTP configuration (Gmail ready)

---

## 🚀 **DEPLOYMENT OPTIONS**

### **Option 1: Traditional Server Deployment (Recommended for Government)**

#### **Prerequisites:**
- Server with Windows/Linux
- Python 3.12+ installed
- SSL certificate for HTTPS
- Domain DNS pointing to server

#### **Deployment Steps:**

1. **Upload Files to Server**
   ```bash
   # Upload entire project to server
   # Location: /var/www/gst-compliance-system/
   ```

2. **Install Dependencies**
   ```bash
   cd /var/www/gst-compliance-system/
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   ```bash
   # Copy .env.production to .env
   cp .env.production .env
   
   # Update email settings if needed
   # Update database path if using PostgreSQL
   ```

4. **Database Setup**
   ```bash
   # Run migrations
   python manage.py migrate
   
   # Create superuser
   python manage.py createsuperuser
   ```

5. **Static Files**
   ```bash
   # Collect static files
   python manage.py collectstatic
   ```

6. **Start Production Server**
   ```bash
   # Using Gunicorn (recommended)
   pip install gunicorn
   gunicorn gst_compliance_system.wsgi:application --bind 0.0.0.0:8000
   ```

7. **Configure Web Server (Nginx/Apache)**
   ```nginx
   # Nginx configuration example
   server {
       listen 80;
       server_name mongargst.drc.gov.bt;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
       
       location /static/ {
           alias /var/www/gst-compliance-system/staticfiles/;
       }
   }
   ```

8. **Configure SSL**
   ```bash
   # Install Certbot for Let's Encrypt SSL
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d mongargst.drc.gov.bt
   ```

---

### **Option 2: Cloud Platform Deployment**

#### **Render.com (Easiest Option)**
1. Push code to GitHub
2. Create new Render account
3. Connect GitHub repository
4. Configure environment variables in Render dashboard
5. Deploy automatically

#### **Heroku**
1. Install Heroku CLI
2. Create Heroku app
3. Push code to Heroku
4. Configure environment variables
5. Deploy

---

## 🔧 **CURRENT CONFIGURATION DETAILS**

### **Domain Configuration**
```
Primary Domain: mongargst.drc.gov.bt
WWW Domain: www.mongargst.drc.gov.bt
```

### **Database Configuration**
```
Current: SQLite (db.sqlite3)
Recommended: PostgreSQL (for production)
Migration Path: Easy - just change DATABASE_URL
```

### **Email Configuration**
```
Current: Console backend (logs only)
Recommended: Gmail SMTP or government email server
Status: Placeholder configuration ready
```

### **Security Configuration**
```
DEBUG: False ✅
SECRET_KEY: Secure ✅
ALLOWED_HOSTS: Configured ✅
CORS: Restricted ✅
SSL: Required (to be configured) ⚠️
```

---

## 📊 **POST-DEPLOYMENT CHECKLIST**

### **Immediate (Before Going Live)**
- [ ] SSL/HTTPS certificate configured
- [ ] DNS pointing to correct server
- [ ] Database migrations run successfully
- [ ] Static files collected
- [ ] Superuser account created
- [ ] Email notifications tested
- [ ] Backup procedures configured

### **After Launch**
- [ ] Monitor system performance
- [ ] Check error logs regularly
- [ ] Test all user workflows
- [ ] Verify data backups working
- [ ] Monitor security logs
- [ ] Update documentation

---

## 🔄 **UPGRADE PATH RECOMMENDATIONS**

### **Phase 1: Initial Launch (Current)**
- SQLite database
- Console email backend
- Basic SSL certificate
- Single server deployment

### **Phase 2: Stabilization (1-2 weeks)**
- Upgrade to PostgreSQL
- Configure real email server
- Implement database backups
- Add monitoring

### **Phase 3: Scaling (1-2 months)**
- Load balancer
- Multiple application servers
- CDN for static files
- Advanced monitoring
- Disaster recovery

---

## 🆘 **TROUBLESHOOTING**

### **Common Issues:**

**1. ALLOWED_HOSTS Error**
```bash
# Error: Invalid HTTP_HOST header
# Solution: Ensure mongargst.drc.gov.bt is in ALLOWED_HOSTS
```

**2. Database Connection Error**
```bash
# Error: Unable to open database file
# Solution: Check database file permissions and path
```

**3. Static Files Not Loading**
```bash
# Error: 404 on static files
# Solution: Run python manage.py collectstatic
```

**4. Email Not Sending**
```bash
# Error: Email backend configuration
# Solution: Configure SMTP settings in .env
```

---

## 📞 **SUPPORT CONTACTS**

**Technical Support:** [Your IT Department]  
**Domain Support:** [Your Network Administrator]  
**Security Team:** [Your Security Team]

---

## 📝 **NOTES**

- **Backup Strategy:** Daily database backups recommended
- **Security Updates:** Keep Django and dependencies updated
- **Monitoring:** Set up uptime monitoring
- **Logs:** Monitor application and server logs
- **Performance:** Optimize database queries as needed

---

**Configuration Complete:** ✅  
**Ready for Deployment:** ✅  
**Next Step:** Choose deployment platform and follow guide above