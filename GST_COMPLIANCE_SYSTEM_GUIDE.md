# GST COMPLIANCE SYSTEM - COMPREHENSIVE USER GUIDE

## TABLE OF CONTENTS

1. [System Overview](#system-overview)
2. [Module Descriptions](#module-descriptions)
3. [Compliance Risk Selection Rationales](#compliance-risk-selection-rationales)
4. [Detailed Procedures](#detailed-procedures)
5. [User Guide](#user-guide)
6. [Risk Assessment Workflow](#risk-assessment-workflow)
7. [Appendices](#appendices)

---

## 1. SYSTEM OVERVIEW

### 1.1 Purpose
The GST Compliance System is a comprehensive web-based application designed to manage GST registration, returns filing, compliance monitoring, risk assessment, audit processes, and reporting for the Bhutan Revenue and Customs Department.

### 1.2 Key Features
- **Taxpayer Registration and Management**
- **GST Returns Filing and Calculation**
- **Compliance Monitoring and Enforcement**
- **Risk-Based Selection for Audit**
- **Audit Case Management**
- **Reporting and Analytics**
- **Automated Calculations**
- **Real-time Data Validation**

### 1.3 Technology Stack
- **Backend**: Django 6.1 (Python 3.12)
- **Database**: SQLite (development), PostgreSQL (production)
- **Frontend**: Django Admin with custom templates
- **Charts**: Chart.js for analytics
- **Deployment**: Render.com

### 1.4 Access Information
- **Live URL**: https://gst-compliance-system-19um.onrender.com
- **Admin Panel**: https://gst-compliance-system-19um.onrender.com/admin/
- **Development**: http://localhost:8000/admin/

---

## 2. MODULE DESCRIPTIONS

### 2.1 Core Module
The Core module provides authentication and user management:
- **User Management**: Create and manage user accounts
- **Authentication**: Login/logout functionality
- **Access Control**: Role-based permissions
- **Audit Log**: Track all system changes

### 2.2 Taxpayers Module
Manages taxpayer registration and enquiries:
- **Taxpayer Master**: Primary registration for all GST taxpayers
- **Multiple License Reference**: Secondary license management
- **Taxpayer Enquiry**: Query taxpayer information
- **Auto-fetch**: Automatic information retrieval via GSTIN

### 2.3 Returns Module
Handles GST return filing and processing:
- **GST Return**: Monthly return filing with automated calculations
- **Auto-calculations**: GST payable/refundable, filing delays, due dates
- **Validation**: Real-time data validation and error checking
- **Import/Export**: Bulk data import and report generation

### 2.4 Compliance & Enforcement Module
Monitors compliance and manages enforcement actions:
- **Compliance Monitoring**: Track filing status and compliance levels
- **Compliance Risk Referral**: Risk-based selection for audit
- **Enforcement & Recovery**: Case management for non-compliance

### 2.5 Audit & Refund Module
Manages audit processes and refund claims:
- **Audit Case**: Create and manage audit cases
- **Audit Assessment**: Detailed assessment calculations
- **Audit Finding**: Document audit findings
- **Refund Register**: Process refund claims

### 2.6 Reporting Module
Generates reports and analytics:
- **Report Templates**: Create custom report formats
- **Generated Reports**: Run and store reports
- **Dashboard Analytics**: Visual charts and trends
- **Export Options**: CSV, Excel, PDF formats

---

## 3. COMPLIANCE RISK SELECTION RATIONALES

### 3.1 Risk Assessment Framework

The system uses a risk-based approach to select taxpayers for audit, ensuring efficient resource allocation and maximizing revenue protection.

### 3.2 Risk Selection Criteria

#### A. Filing & Payment Risk
**Rationale**: Taxpayers who consistently file late or make partial payments pose higher compliance risk.

**Selection Criteria:**
- **Filing Status**: "Overdue / Non-Filer" or "Late Filer"
- **Payment Status**: "Not paid" or "Partial payment"
- **Filing Delay**: > 30 days from due date
- **History**: Pattern of non-compliance in last 3 periods

**Risk Level Assignment:**
- **Critical**: > 90 days overdue, non-filer for 2+ periods
- **High**: 60-90 days overdue, partial payment
- **Medium**: 30-60 days overdue, occasional late filing
- **Low**: < 30 days overdue, first-time late filer

#### B. Sales & Output GST Risk
**Rationale**: Significant discrepancies between declared sales and actual sales indicate potential underreporting.

**Selection Criteria:**
- **Variation**: > 20% variation from expected sales
- **Growth Pattern**: Unusual sales growth (> 50% increase)
- **Decline Pattern**: Sudden sales decline (> 50% decrease)
- **Industry Benchmark**: Deviation from industry averages

**Risk Level Assignment:**
- **Critical**: > 50% variation, inconsistent patterns
- **High**: 30-50% variation, unusual trends
- **Medium**: 20-30% variation, explainable variations
- **Low**: < 20% variation, normal patterns

#### C. Purchase & ITC Risk
**Rationale**: Excessive ITC claims or mismatched purchase declarations may indicate fraudulent claims.

**Selection Criteria:**
- **ITC Ratio**: ITC > 80% of output GST
- **Purchase Patterns**: Large purchases without supporting documents
- **Import Claims**: High import GST claims without import permits
- **Domestic Purchase**: Inconsistent purchase declarations

**Risk Level Assignment:**
- **Critical**: ITC > 90%, no supporting documents
- **High**: ITC 80-90%, irregular patterns
- **Medium**: ITC 60-80%, some documentation
- **Low**: ITC < 60%, proper documentation

#### D. Import & Transaction Risk
**Rationale**: Import transactions with unusual patterns or high-value imports without proper customs clearance.

**Selection Criteria:**
- **Import Value**: High import value (> Nu. 1 million per period)
- **Import Frequency**: Frequent imports without corresponding sales
- **Customs Records**: Mismatch with customs data
- **Cross-border**: High cross-border transactions

**Risk Level Assignment:**
- **Critical**: No customs records, high value imports
- **High**: Partial customs records, medium-high value
- **Medium**: Complete customs records, explainable patterns
- **Low**: Proper documentation, normal import patterns

### 3.3 Risk Scoring Methodology

#### Composite Risk Score Calculation

**Formula:**
```
Risk Score = (Filing Risk × 0.3) + (Sales Risk × 0.25) + (ITC Risk × 0.25) + (Import Risk × 0.2)
```

**Score Interpretation:**
- **0-1.5**: Low Risk
- **1.6-2.5**: Medium Risk
- **2.6-3.5**: High Risk
- **3.6-5.0**: Critical Risk

#### Risk Level Assignment

**Critical Risk (Red Flag):**
- **Action**: Immediate audit, full investigation
- **Timeline**: Audit within 15 days
- **Resources**: Senior auditor + support team
- **Priority**: Highest

**High Risk (Yellow Flag):**
- **Action**: Desk audit or field audit
- **Timeline**: Audit within 30 days
- **Resources**: Assigned auditor
- **Priority**: High

**Medium Risk (Orange Flag):**
- **Action**: Document review, additional information request
- **Timeline**: Review within 45 days
- **Resources**: Case officer
- **Priority**: Medium

**Low Risk (Green Flag):**
- **Action**: Routine monitoring, regular filing checks
- **Timeline**: Quarterly review
- **Resources**: Automated monitoring
- **Priority**: Low

### 3.4 Risk Referral Process

#### Automatic Risk Referral
The system automatically refers high-risk taxpayers to the Compliance Risk Referral module when:
- Risk score > 2.5 (High or Critical)
- Compliance status = "Non-Filer" or "Payment Default"
- Filing delay > 60 days
- Unusual transaction patterns detected

#### Manual Risk Referral
Officers can manually refer taxpayers for risk assessment when:
- Intelligence received from other sources
- Cross-border information indicates issues
- Public complaints received
- Special investigation required

---

## 4. DETAILED PROCEDURES

### 4.1 Taxpayer Registration Procedure

#### Step 1: Access Taxpayer Registration
1. Login to admin panel
2. Navigate to Taxpayers → Taxpayer Master
3. Click "Add Taxpayer Master"

#### Step 2: Enter Basic Information
- **GSTIN**: Enter 15-character GSTIN
- **Taxpayer Name**: Enter legal name as per business registration
- **Business Name**: Trade name (if different)
- **CID/Company Reg No**: Enter registration number
- **RAMIS TPN**: Enter RAMIS taxpayer number

#### Step 3: Enter Contact Information
- **Address**: Complete business address
- **Dzongkhag**: Select dzongkhag
- **Phone**: Contact phone number
- **Email**: Business email address

#### Step 4: Enter Business Details
- **Organisation Type**: Select from dropdown
- **Frequency**: Select filing frequency (Monthly/Quarterly)
- **Sector**: Select business sector
- **Registration Date**: Enter date in DD-MM-YYYY format

#### Step 5: Set License Status
- **Is Primary License**: Check if this is the primary GST license
- **Status**: Select (Active/Inactive/Suspended/Cancelled/Deregistered)
- **Registration Type**: Select registration type

#### Step 6: Save and Review
- Click "Save"
- System auto-validates GSTIN format
- System checks for duplicate registrations
- Review all entered information

#### Step 7: Auto-fetch Verification
- Enter GSTIN and press Tab
- System auto-fills taxpayer information if already registered
- Verify auto-filled information for accuracy

### 4.2 GST Return Filing Procedure

#### Step 1: Access Returns Module
1. Navigate to Returns → GST Return
2. Click "Add GST Return"

#### Step 2: Enter Tax Period
- Select tax period from dropdown (e.g., Jan-2026)
- System auto-calculates due date (end of period + 30 days)
- Bhutan GST Rule: January 2026 due date = 02-03-2026

#### Step 3: Enter GSTIN
- Enter taxpayer GSTIN
- System auto-fetches taxpayer information
- Verify taxpayer name and details

#### Step 4: Enter Sales Information
- **Declared Sales**: Total sales for the period
- **Declared Import Value**: Value of imports
- **Declared Domestic Purchase**: Domestic purchases

#### Step 5: Enter GST Details
- **Declared Output GST**: GST on sales (auto-calculated as 5% of sales)
- **Declared Import GST**: GST on imports (auto-calculated as 5% of imports)
- **Domestic Purchase ITC**: ITC claimed on domestic purchases
- **Total ITC**: Total Input Tax Credit

#### Step 6: System Auto-Calculations
System automatically calculates:
- **GST Payable/Refundable**: Output GST - Total ITC
- **Filing Delay**: Days from due date to filing date
- **Filing Status**: On time/Late/Overdue based on filing date
- **Payment Status**: Based on actual payment received

#### Step 7: Review and Submit
- Review all auto-calculated values
- Add remarks if needed
- Click "Save"
- System validates all data
- Return is saved with compliance status

### 4.3 Compliance Monitoring Procedure

#### Step 1: Access Compliance Monitoring
1. Navigate to Compliance → Compliance Monitoring
2. Click "Add Compliance Monitoring"

#### Step 2: Select Tax Period
- Select tax period from dropdown
- System links to corresponding GST return

#### Step 3: Enter GSTIN
- Enter taxpayer GSTIN
- System auto-fetches taxpayer information
- Auto-populates taxpayer name and details

#### Step 4: Auto-Populate from GST Return
- System automatically fetches data from GST return:
  - Filing status
  - Filing delay
  - Payment status
  - GST payable/refundable

#### Step 5: Determine Compliance Status
System automatically assigns:
- **Compliant**: On-time filing, full payment
- **Non-Filer**: Not filed or > 90 days overdue
- **Late Filer**: Filed 30-90 days late
- **Payment Default**: Not paid or partial payment

#### Step 6: Set Compliance Flag
- **Green**: Compliant
- **Yellow**: Minor issues (late filing)
- **Red**: Major issues (non-filer, payment default)

#### Step 7: Add Remarks
- Document any special circumstances
- Note manual overrides
- Add contact information

#### Step 8: Save and Monitor
- Click "Save"
- Compliance record created
- System updates compliance dashboard

### 4.4 Compliance Risk Referral Procedure

#### Step 1: Access Risk Referral
1. Navigate to Compliance → Compliance Risk Referral
2. Click "Add Compliance Risk Referral"

#### Step 2: Select Tax Period
- Select assessment period (From and To)
- System fetches returns for selected period

#### Step 3: Enter GSTIN
- Enter taxpayer GSTIN
- System auto-fetches taxpayer information
- Auto-populates taxpayer details

#### Step 4: Risk Analysis
System calculates risk factors:
- **Filing & Payment Risk**: Based on filing history
- **Sales & Output GST Risk**: Based on sales variations
- **Purchase & ITC Risk**: Based on ITC patterns
- **Import & Transaction Risk**: Based on import patterns

#### Step 5: Risk Scoring
System calculates composite risk score:
- **Risk Score**: 0-5 scale
- **Risk Level**: Low/Medium/High/Critical
- **Risk Type**: Category of risk identified

#### Step 6: System Decision
System automatically recommends:
- **AUDIT**: For High/Critical risk
- **REVIEW**: For Medium risk
- **MONITOR**: For Low risk
- **NOT SELECTED**: For compliant taxpayers

#### Step 7: Officer Judgment
Officer can override system decision:
- Review system recommendation
- Consider additional factors
- Override if justified
- Document reasoning

#### Step 8: Assignment
- **Assessor**: Assign compliance officer
- **Assessment Date**: Set assessment date
- **Assessment Status**: Set status (Pending/In Progress/Completed)

#### Step 9: Final Selection
- **Final Selection**: Confirm selection for audit
- **Action Status**: Track referral status
- **Remarks**: Document decision rationale

### 4.5 Enforcement & Recovery Procedure

#### Step 1: Access Enforcement
1. Navigate to Compliance → Enforcement & Recovery
2. Click "Add Enforcement & Recovery"

#### Step 2: Select Tax Period
- Select relevant tax period
- Links to compliance monitoring record

#### Step 3: Enter GSTIN
- Enter taxpayer GSTIN
- System auto-fetches taxpayer information

#### Step 4: Case Information
- **Case ID**: Auto-generated
- **Case Type**: Select (Non-Filing/Non-Payment/Recovery/Other)
- **Amount Due**: Enter outstanding amount

#### Step 5: Notice Details
- **Notice Date**: Enter notice date (DD-MM-YYYY)
- System tracks notice timeline

#### Step 6: Action & Recovery
- **Action Taken**: Document actions taken
- **Amount Recovered**: Enter recovered amount
- **Status**: Set case status (Open/Follow-up/Recovered/Closed)

#### Step 7: Assignment
- **Assigned Officer**: Assign case officer
- **Assigned By**: Track who assigned the case
- **Assigned Date**: Auto-set on assignment

#### Step 8: Close Case
- When amount fully recovered
- Update status to "Closed"
- Document final resolution

### 4.6 Audit Case Procedure

#### Step 1: Access Audit Case
1. Navigate to Audit & Refund → Audit Case
2. Click "Add Audit Case"

#### Step 2: Risk Referral Link
- Select risk referral (if from risk assessment)
- Or create new case independently

#### Step 3: Assessment Information
- **Assessment Date**: Enter assessment date
- **From/To Tax Period**: Select audit period range
- **Assessment Type**: Select (Desk Assessment/Field Audit/Targeted Audit)

#### Step 4: Taxpayer Information
- Enter GSTIN
- System auto-fetches taxpayer details
- Auto-populates dzongkhag, organization type, frequency

#### Step 5: Assignment
- **Assigned Officer**: Assign audit officer
- **Assigned By**: Track assignment
- **Assigned Date**: Auto-set
- **Due Date**: Set case due date

#### Step 6: Status Management
- **Status**: Track case status (Referred/Pending Assignment/Assigned/In Progress/Completed/Closed)
- **Assessor**: Assign assessor
- **Case Closed Date**: When case closed

#### Step 7: Remarks
- Document case details
- Add relevant notes

### 4.7 Audit Assessment Procedure

#### Step 1: Access Audit Assessment
1. Navigate to Audit & Refund → Audit Assessment
2. Click "Add Audit Assessment"

#### Step 2: Link to Audit Case
- Select audit case
- System auto-populates taxpayer information

#### Step 3: Enter Assessment Details
- **ASC No**: Auto-generated
- **Assessment Date**: Enter date
- **Tax Period**: Auto-populated from audit case

#### Step 4: GST Return Information (Read-Only)
- System displays original return data:
  - Declared sales
  - Declared output GST
  - Declared imports
  - ITC claimed
  - GST payable/refundable

#### Step 5: Assessed Information
- **Assessed Sales Turnover**: Enter assessed value
- **Actual Import Value (eCMS)**: From eCMS system
- **Assessed Import Value**: Assessed import value
- **GST on Assessed Import**: Auto-calculated (5%)
- **Assessed Domestic Purchase**: Assessed purchase value
- **GST on Assessed Domestic Purchase**: Auto-calculated (5%)
- **GST Payable/Refundable (Assessed)**: Auto-calculated

#### Step 6: Calculations
System calculates:
- **Variation**: Assessed - Declared
- **Variation %**: Percentage variation

#### Step 7: Findings
- **Reason Code**: Select reason for variation
- **Discrepancy**: Document discrepancy details

#### Step 8: Outcome
- **Assessment Outcome**: Select outcome
- **Action Taken**: Document actions

#### Step 9: Status
- **Status**: Set assessment status
- **Case Closed Date**: When closed
- **Assessment Duration**: Auto-calculated

### 4.8 Audit Finding Procedure

#### Step 1: Access Audit Finding
1. Navigate to Audit & Refund → Audit Finding
2. Click "Add Audit Finding"

#### Step 2: Link to Audit Case
- Select audit case
- Links to ongoing audit

#### Step 3: Finding Information
- **Finding ID**: Auto-generated
- **Reason Code**: Select finding category
- **Finding Type**: Select type
- **Discrepancy**: Document discrepancy
- **Amount Involved**: Enter amount
- **Description**: Detailed description
- **Action Taken**: Document action
- **Auditor Remarks**: Add remarks

#### Step 4: Save Finding
- Click "Save"
- Finding linked to audit case
- Visible in audit case dashboard

### 4.9 Report Generation Procedure

#### Step 1: Access Reporting
1. Navigate to Reporting → Generated Reports
2. View dashboard with analytics

#### Step 2: Generate Reports
Click report generation buttons:
- **Taxpayer CSV**: Download all taxpayers
- **Taxpayer Excel**: Download in Excel format
- **Returns CSV**: Download all returns
- **Returns Excel**: Download in Excel format
- **Compliance CSV**: Download compliance records
- **Compliance Excel**: Download in Excel format

#### Step 3: Dashboard Analytics
View interactive charts:
- **Taxpayer Status Distribution**: Pie chart
- **Returns by Tax Period**: Bar chart
- **Compliance Status**: Doughnut chart
- **Monthly Revenue Trend**: Line chart

#### Step 4: Download/Print
- **Download**: Click download button to save report
- **Print**: Click print button to print report

---

## 5. USER GUIDE

### 5.1 First-Time Login

#### Step 1: Access Admin Panel
- Go to: https://gst-compliance-system-19um.onrender.com/admin/
- Enter your username and password

#### Step 2: Change Password
1. Click your username (top right)
2. Click "Change password"
3. Enter new password
4. Confirm new password
5. Click "Change Password"

#### Step 3: Explore Dashboard
- View all modules in left sidebar
- Click on each module to explore
- Familiarize yourself with the interface

### 5.2 Creating Taxpayer Records

#### Quick Reference:
- **GSTIN Format**: 15 characters, e.g., p1234
- **Date Format**: DD-MM-YYYY, e.g., 15-08-2026
- **Tax Period**: Jan-2026, Feb-2026, etc.
- **Auto-fetch**: Enter GSTIN and press Tab

#### Tips:
- Use the Tab key to trigger auto-fetch
- Date fields have calendar picker
- All fields have validation
- Save frequently to avoid data loss

### 5.3 Filing GST Returns

#### Quick Reference:
- **Due Date**: End of period + 30 days
- **GST Rate**: 5% for all transactions
- **ITC**: Can be claimed on purchases
- **Calculation**: Automatic - no manual math needed

#### Tips:
- Sales, imports, purchases automatically calculate GST
- Filing delay auto-calculates
- Compliance status auto-updates
- Review before saving

### 5.4 Monitoring Compliance

#### Quick Reference:
- **Compliance Status**: Green/Yellow/Red
- **Filing Status**: On time/Late/Overdue
- **Auto-population**: Data from GST returns
- **Risk Flags**: Based on compliance history

#### Tips:
- Monitor compliance status regularly
- Follow up on Red flags
- Document manual overrides
- Use compliance reports for trends

### 5.5 Managing Risk Assessment

#### Quick Reference:
- **Risk Score**: 0-5 scale
- **Risk Levels**: Low/Medium/High/Critical
- **System Decision**: Automatic recommendation
- **Officer Override**: Manual adjustment

#### Tips:
- Review system recommendations
- Consider additional factors
- Document override reasons
- Focus on high/critical risks

### 5.6 Conducting Audits

#### Quick Reference:
- **Audit Case**: Created from risk referral
- **Assessment**: Detailed review
- **Findings**: Document issues
- **Outcome**: Final decision

#### Tips:
- Link assessment to audit case
- Use auto-calculations
- Document all findings
- Close cases when complete

### 5.7 Generating Reports

#### Quick Reference:
- **6 Report Types**: Taxpayer, Returns, Compliance
- **2 Formats**: CSV and Excel
- **Interactive Charts**: Real-time analytics
- **Download/Print**: Direct access

#### Tips:
- Generate regular reports
- Use charts for presentations
- Download for offline analysis
- Print for documentation

---

## 6. RISK ASSESSMENT WORKFLOW

### 6.1 Automated Risk Assessment Workflow

```
1. Taxpayer Files Return
       ↓
2. System Analyzes Return
       ↓
3. Calculates Risk Score
       ↓
4. Assigns Risk Level
       ↓
5. Auto-Refers if High/Critical
       ↓
6. Officer Reviews
       ↓
7. Final Selection for Audit
```

### 6.2 Manual Risk Assessment Workflow

```
1. Officer Identifies Risk
       ↓
2. Creates Risk Referral
       ↓
3. Documents Risk Factors
       ↓
4. Calculates Risk Score
       ↓
5. Assigns Risk Level
       ↓
6. System Recommends Action
       ↓
7. Officer Approves/Overrides
       ↓
8. Creates Audit Case
```

### 6.3 Audit Workflow

```
1. Risk Referral Created
       ↓
2. Audit Case Opened
       ↓
3. Officer Assigned
       ↓
4. Assessment Conducted
       ↓
5. Findings Documented
       ↓
6. Outcome Determined
       ↓
7. Case Closed
```

### 6.4 Enforcement Workflow

```
1. Non-Compliance Detected
       ↓
2. Compliance Monitoring Updated
       ↓
3. Enforcement Case Created
       ↓
4. Notice Issued
       ↓
5. Follow-up Conducted
       ↓
6. Recovery Initiated
       ↓
7. Case Closed
```

---

## 7. APPENDICES

### Appendix A: Risk Selection Criteria Reference

| Risk Category | Selection Criteria | Risk Level | Action |
|--------------|-------------------|-------------|--------|
| Filing Risk | > 90 days overdue | Critical | Immediate audit |
| Filing Risk | 60-90 days overdue | High | Priority audit |
| Filing Risk | 30-60 days overdue | Medium | Document review |
| Filing Risk | < 30 days overdue | Low | Monitor |
| Sales Risk | > 50% variation | Critical | Full investigation |
| Sales Risk | 30-50% variation | High | Desk audit |
| Sales Risk | 20-30% variation | Medium | Additional info |
| Sales Risk | < 20% variation | Low | Routine check |
| ITC Risk | > 90% of output GST | Critical | ITC verification |
| ITC Risk | 80-90% of output GST | High | Document review |
| ITC Risk | 60-80% of output GST | Medium | Spot check |
| ITC Risk | < 60% of output GST | Low | Accept |
| Import Risk | No customs records | Critical | Import verification |
| Import Risk | Partial records | High | Customs check |
| Import Risk | Complete records | Medium | Routine review |
| Import Risk | Normal patterns | Low | Accept |

### Appendix B: Compliance Status Definitions

| Status | Definition | Color Code | Action |
|--------|-----------|------------|--------|
| Compliant | On-time filing, full payment | Green | Routine monitoring |
| Non-Filer | Not filed or > 90 days overdue | Red | Immediate action |
| Late Filer | Filed 30-90 days late | Yellow | Follow-up required |
| Payment Default | Not paid or partial payment | Red | Enforcement action |

### Appendix C: GST Calculation Formulas

#### Sales GST Calculation
```
Declared Output GST = Declared Sales × 5%
```

#### Import GST Calculation
```
Declared Import GST = Declared Import Value × 5%
```

#### ITC Calculation
```
Total ITC = Import GST + Domestic Purchase ITC
```

#### GST Payable/Refundable
```
GST Payable/Refundable = Output GST - Total ITC
```

#### Filing Delay Calculation
```
Filing Delay = Filing Date - Due Date (in days)
```

#### Bhutan GST Due Date
```
Due Date = End of Tax Period + 30 days
Example: January 2026 → 31 January + 30 days = 02 March 2026
```

### Appendix D: Frequently Asked Questions

**Q: How do I reset my password?**
A: Click your username → Change password → Enter new password → Save

**Q: Can I change the due date calculation?**
A: No, it's fixed by Bhutan GST regulations (end of period + 30 days)

**Q: What if the auto-fetch doesn't work?**
A: Check GSTIN format (15 characters), ensure taxpayer is registered as primary license

**Q: How do I delete a record?**
A: Select the record → Click "Delete" → Confirm deletion

**Q: Can I import bulk data?**
A: Yes, use the Import button in Taxpayers and Returns modules

**Q: How do I restore from backup?**
A: See BACKUP_GUIDE.md for detailed restoration instructions

**Q: What if the site is slow?**
A: Free tier has sleep mode - wait 30 seconds for it to wake up

**Q: Can I add custom fields?**
A: Yes, but requires database migration - contact developer

**Q: How do I add new users?**
A: Core → Users → Add User → Set permissions

### Appendix E: Contact Information

**Technical Support:**
- Email: jimmes2008@gmail.com
- System Administrator: jamphel.tshering

**Documentation Updates:**
- Version: 1.0
- Last Updated: August 15, 2026
- Next Review: December 2026

---

## END OF GUIDE

This guide provides comprehensive procedures for using the GST Compliance System. For additional assistance or training requests, please contact the system administrator.