# 🚀 RENDER.COM DEPLOYMENT GUIDE - mongargst.drc.gov.bt

**Platform:** Render.com  
**Domain:** mongargst.drc.gov.bt  
**Experience:** Previous Render deployment  
**DNS Handler:** User will handle DNS configuration  
**Timeline:** 1-2 days

---

## 🎯 **QUICK START - RENDER.COM DEPLOYMENT**

### **Why Render.com:**
- ✅ Easy Django deployment
- ✅ Free SSL certificates (automatic)
- ✅ PostgreSQL database included
- ✅ Automatic HTTPS
- ✅ Easy scaling
- ✅ Government compliance options

---

## 📋 **PRE-DEPLOYMENT CHECKLIST**

### **Requirements:**
- [ ] GitHub account with code repository
- [ ] Render.com account (free tier available)
- [ ] mongargst.drc.gov.bt domain registered
- [ ] Access to domain DNS management

### **Files Ready:**
- ✅ All project files
- ✅ .env.production configured
- ✅ requirements.txt complete
- ✅ System tested and verified

---

## 🚀 **STEP-BY-STEP DEPLOYMENT**

### **Step 1: Prepare Code Repository (1 hour)**

#### **1.1 Create GitHub Repository:**
1. Go to GitHub.com
2. Create new repository
3. Name: `gst-compliance-system`
4. Make it private (recommended for government system)
5. Initialize with README

#### **1.2 Upload Your Code:**
```bash
# In your project directory
cd C:\Users\jamphelt_mongar\gst_compliance_system

# Initialize git
git init
git add .
git commit -m "Initial commit - GST Compliance System"

# Add remote repository
git remote add origin https://github.com/your-username/gst-compliance-system.git

# Push to GitHub
git branch -M main
git push -u origin main
```

#### **1.3 Create .gitignore:**
```bash
# Add to .gitignore
.env
.env.local
*.pyc
__pycache__/
db.sqlite3
staticfiles/
media/
```

---

### **Step 2: Configure Render.com (30 minutes)**

#### **2.1 Create Render Account:**
1. Go to render.com
2. Sign up with GitHub
3. Authorize Render to access your repositories
4. Select "gst-compliance-system" repository

#### **2.2 Create Web Service:**
1. Click "New +" → "Web Service"
2. Select "gst-compliance-system" repository
3. Configure deployment settings:

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
gunicorn gst_compliance_system.wsgi:application
```

**Python Version:** 3.12.10

---

### **Step 3: Configure Environment Variables (15 minutes)**

#### **3.1 Add Environment Variables in Render:**
Go to your web service → Environment → Add Environment Variables:

```
SECRET_KEY=eaS-uAD"PBaq=gq-Y\P'I5scc0~wo1MQx)7'9"ST;q>7K#r+iB
DEBUG=False
ALLOWED_HOSTS=mongargst.drc.gov.bt,*.onrender.com
CORS_ALLOWED_ORIGINS=https://mongargst.drc.gov.bt
DATABASE_URL=postgresql://[render-provided]
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=gst-compliance@drc.gov.bt
TIME_ZONE=Asia/Thimphu
```

**Note:** Render will automatically provide the DATABASE_URL for PostgreSQL.

---

### **Step 4: Deploy and Test (30 minutes)**

#### **4.1 Initial Deployment:**
1. Click "Create Web Service"
2. Render will automatically deploy
3. Wait for deployment to complete (5-10 minutes)
4. Access at: `https://gst-compliance-system.onrender.com`

#### **4.2 Test Deployment:**
- [ ] Homepage loads correctly
- [ ] Admin panel accessible
- [ ] Database connection working
- [ ] All modules functional

---

### **Step 5: Configure Custom Domain (30 minutes)**

#### **5.1 Add Custom Domain in Render:**
1. Go to your web service → Settings → Custom Domains
2. Click "Add Custom Domain"
3. Enter: `mongargst.drc.gov.bt`
4. Render will provide DNS configuration

#### **5.2 Configure DNS (You Handle This):**

**DNS Configuration Required:**
```
Type: CNAME
Name: mongargst
Value: [your-app-name].onrender.com
TTL: 300
```

**For www subdomain:**
```
Type: CNAME
Name: www
Value: [your-app-name].onrender.com
TTL: 300
```

#### **5.3 DNS Configuration Steps:**
1. Log into your domain registrar (where mongargst.drc.gov.bt is registered)
2. Go to DNS management
3. Add the CNAME records provided by Render
4. Wait for DNS propagation (usually 1-24 hours)

---

### **Step 6: SSL Certificate (Automatic)**

#### **✅ Render Handles SSL Automatically:**
- Render automatically provides SSL certificates
- HTTPS is enabled by default
- No manual SSL configuration needed
- Certificates are auto-renewed

---

### **Step 7: Database Setup (Automatic)**

#### **✅ Render Provides PostgreSQL:**
- PostgreSQL database automatically created
- Connection string provided in DATABASE_URL
- Automatic backups included
- Easy scaling options

---

### **Step 8: Final Testing (1 hour)**

#### **8.1 Test Custom Domain:**
1. Wait for DNS propagation
2. Access: `https://mongargst.drc.gov.bt`
3. Verify HTTPS works properly
4. Test all functionality

#### **8.2 User Testing:**
- [ ] Login functionality
- [ ] Admin panel access
- [ ] All modules working
- [ ] Reports generating
- [ ] Performance acceptable

---

## 🔧 **RENDER.COM SPECIFIC CONFIGURATIONS**

### **Update requirements.txt:**
Add these if not already present:
```
Django==6.1
dj-database-url==2.1.0
gunicorn==21.2.0
psycopg2-binary==2.9.9
whitenoise==6.6.0
python-dotenv==1.0.0
```

### **Update settings.py for Render:**
```python
# Add these imports at the top
import dj_database_url
import os

# Update database configuration
DATABASES['default'] = dj_database_url.config(
    default=os.environ.get('DATABASE_URL'),
    conn_max_age=600,
    ssl_require=True
)

# Add whitenoise for static files
MIDDLEWARE.insert(5, 'whitenoise.middleware.WhiteNoiseMiddleware', 'django.middleware.security.SecurityMiddleware')
```

---

## 📊 **RENDER.COM PRICING**

### **Free Tier (For Testing):**
- ✅ Web Service: Free
- ✅ PostgreSQL: Free (256MB)
- ✅ SSL: Free
- ✅ Custom Domain: Free
- ⚠️ Sleeps after 15 minutes inactivity

### **Starter Tier ($7/month):**
- ✅ No sleep (always available)
- ✅ More CPU/RAM
- ✅ Better performance
- ✅ Professional usage

---

## 🎯 **TIMELINE ESTIMATE**

### **Day 1:**
- 1 hour: Prepare and push code to GitHub
- 1 hour: Configure Render.com deployment
- 1 hour: Initial deployment and testing

### **Day 2:**
- 1 hour: Configure custom domain
- 2-24 hours: DNS propagation (wait time)
- 1 hour: Final testing and verification

---

## 🔒 **SECURITY CONSIDERATIONS**

### **Render.com Security:**
- ✅ Automatic SSL certificates
- ✅ Encrypted connections
- ✅ Secure database connections
- ✅ Regular security updates
- ✅ DDoS protection

### **Your Responsibilities:**
- Keep SECRET_KEY secure
- Regular password changes
- Monitor user access
- Regular backups (Render provides automatic backups)

---

## 📞 **RENDER.COM SUPPORT**

### **Documentation:**
- Render Dashboard: https://dashboard.render.com/
- Documentation: https://render.com/docs
- Django Guide: https://render.com/docs/deploy-django

### **Support:**
- Email: support@render.com
- Chat: Available in dashboard
- Community: Discord and forums

---

## 🎯 **ADVANTAGES OF RENDER.COM**

### **For Government Systems:**
- ✅ Compliance ready (SOC 2, HIPAA available)
- ✅ Data security features
- ✅ Regular backups
- ✅ Professional support
- ✅ Easy scaling
- ✅ Automatic HTTPS
- ✅ No server management needed

---

## 📋 **FINAL CHECKLIST**

### **Before Deployment:**
- [ ] Code pushed to GitHub
- [ ] Render.com account created
- [ ] Repository connected to Render
- [ ] Environment variables configured
- [ ] DNS access ready

### **After Deployment:**
- [ ] Initial deployment successful
- [ ] Custom domain configured
- [ ] DNS records added
- [ ] HTTPS working
- [ ] All functionality tested
- [ ] User training completed

---

## 🚀 **QUICK COMMANDS**

### **Update Code:**
```bash
git add .
git commit -m "Update description"
git push
```
Render will automatically redeploy.

### **View Logs:**
1. Go to Render Dashboard
2. Select your service
3. Click "Logs"
4. View real-time logs

### **Restart Service:**
1. Go to Render Dashboard
2. Select your service
3. Click "Manual Deploy"
4. Click "Deploy latest commit"

---

## 🎉 **DEPLOYMENT SUCCESS**

### **When Complete:**
- ✅ System accessible at https://mongargst.drc.gov.bt
- ✅ HTTPS working automatically
- ✅ SSL certificates active
- ✅ All modules operational
- ✅ No browser security issues
- ✅ Professional production setup

---

**🎯 Ready to deploy! This guide provides everything needed for successful Render.com deployment.**

**Estimated Time:** 1-2 days  
**Difficulty:** Easy (especially with previous Render experience)  
**Success Rate:** Very High