# GST Compliance Management System

## 🎯 Overview
A comprehensive web-based GST compliance management system built with Django framework and SQLite database for local deployment.

## 🚀 Quick Start

### Prerequisites
- Python 3.14.7
- Virtual environment
- Required packages

### Installation

1. **Navigate to project directory:**
   ```bash
   cd C:\Users\jamphelt_mongar\gst_compliance_system
   ```

2. **Activate virtual environment:**
   ```bash
   ..\venv\Scripts\activate
   ```

3. **Run the server:**
   ```bash
   python manage.py runserver
   ```

4. **Access the system:**
   - **Web Interface**: http://localhost:8000
   - **Admin Panel**: http://localhost:8000/admin/

### Default Login Credentials
- **Email**: admin@gst-system.local
- **Username**: admin
- **Password**: admin123

**⚠️ Important**: Change the default password after first login!

## 📋 System Features

### 🔐 User Management
- Email-based authentication
- Role-based access control (Admin, Auditor, Viewer, Data Entry)
- Password management
- User activity logging

### 📊 Core Modules
1. **Taxpayer Master**: Complete taxpayer profile management
2. **Return Filing**: GST return processing and tracking
3. **Refund Register**: Refund application workflow
4. **Risk Assessment**: Automated risk scoring and audit selection
5. **Reporting**: Comprehensive reports and dashboards

### 🎯 Risk Assessment
The system implements your existing risk scoring rules:
- **Inherent Risk (20%)**: Business type, industry volatility
- **Control Risk (15%)**: Internal controls, accounting systems
- **Detection Risk (15%)**: Documentation quality, record keeping
- **Transaction Risk (25%)**: High-value transactions, related parties
- **Behavior Risk (25%)**: Filing timeliness, payment compliance

## 🗄️ Database Models

### Core Models
- **User**: Extended user model with email authentication
- **AuditLog**: User activity tracking
- **SystemSettings**: System configuration

### Taxpayer Models
- **Taxpayer**: Main taxpayer records
- **TaxpayerAddress**: Address information
- **TaxpayerContact**: Contact details
- **GSTRegistration**: GSTIN details

### Return Models
- **GSTReturn**: GST return records
- **ITCClaim**: Input tax credit details
- **PaymentRecord**: Payment tracking
- **FilingStatus**: Status history

### Refund Models
- **RefundApplication**: Refund applications
- **RefundDocument**: Supporting documents
- **RefundApproval**: Approval workflow
- **RefundPayment**: Payment processing

### Risk Assessment Models
- **RiskAssessment**: Risk scores and categories
- **RiskFactor**: Individual risk factors
- **AuditSelection**: Audit candidate selection
- **RiskAlert**: Risk notifications

### Reporting Models
- **ReportTemplate**: Report definitions
- **GeneratedReport**: Generated report instances
- **ReportSchedule**: Scheduled reports
- **DashboardWidget**: Dashboard components

## 🔧 Management Commands

### Database Operations
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### Server Operations
```bash
# Run development server
python manage.py runserver

# Run on specific port
python manage.py runserver 8080
```

### Admin Panel
- Access at: http://localhost:8000/admin/
- Full CRUD operations for all models
- User management
- System configuration

## 📁 Project Structure

```
gst_compliance_system/
├── core/                   # User authentication and system core
├── taxpayers/              # Taxpayer management
├── returns/                # GST return filing
├── refunds/                # Refund processing
├── risk_assessment/        # Risk assessment and audit selection
├── reporting/              # Reports and analytics
├── gst_compliance_system/  # Project configuration
├── media/                  # File uploads
├── static/                 # Static files
└── db.sqlite3             # SQLite database
```

## 🎨 Technology Stack

- **Backend**: Django 6.1, Python 3.14.7
- **Database**: SQLite 3
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **Data Processing**: Pandas, OpenPyXL
- **Forms**: Django Crispy Forms
- **Import/Export**: Django Import-Export

## 🔐 Security Features

- Email-based authentication
- Role-based access control
- Password validation
- Audit logging
- Session management
- CSRF protection

## 📊 Deployment

### Local Server Deployment
1. Install Python dependencies
2. Configure settings.py
3. Run database migrations
4. Create superuser
5. Start server: `python manage.py runserver`
6. Access via local network: `http://[server-ip]:8000`

### Configuration Settings
Edit `gst_compliance_system/settings.py`:
- `ALLOWED_HOSTS`: Add your server IP
- `SECRET_KEY`: Change for production
- `DEBUG`: Set to False for production

## 🔄 Data Import (Future Enhancement)
The system will support Excel import for:
- Taxpayer master data
- GST returns
- Refund applications
- Historical data

## 📈 Reporting (Future Enhancement)
- Standard compliance reports
- Custom report generation
- Data visualization with charts
- Export to PDF, Excel, CSV
- Scheduled reports

## 🚧 Current Status

### ✅ Completed
- Database models for all modules
- User authentication system
- Admin interface configuration
- Basic URL routing
- Login and dashboard views
- Bootstrap 5 templates

### 🚧 In Progress
- Excel import functionality
- Advanced reporting
- Risk assessment automation
- Data validation

### 📋 Planned
- Backup system
- Advanced security features
- Performance optimization
- User management interface

## 🛠️ Troubleshooting

### Common Issues

**Server won't start:**
- Check if port 8000 is available
- Try different port: `python manage.py runserver 8080`

**Login issues:**
- Verify email and password
- Check if user is active
- Reset password via admin panel

**Database errors:**
- Run migrations: `python manage.py migrate`
- Check file permissions

## 📞 Support

For issues or questions:
1. Check admin panel for system status
2. Review audit logs
3. Check system settings
4. Contact system administrator

## 📝 Notes

This is a professional-grade GST compliance management system designed for local deployment. The system provides comprehensive functionality for managing taxpayers, GST returns, refunds, compliance risk assessment, and audit selection.

The modular architecture allows for incremental development and easy future enhancements. As mentioned, we can continue to improve upon completion as needed.