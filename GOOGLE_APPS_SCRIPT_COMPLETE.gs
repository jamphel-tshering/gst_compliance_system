/**
 * GST COMPLIANCE SYSTEM - GOOGLE APPS SCRIPT VERSION
 * Complete replication of Django GST Compliance System
 * 
 * INSTRUCTIONS:
 * 1. Create a new Google Sheet
 * 2. Go to Extensions > Apps Script
 * 3. Delete all existing code
 * 4. Paste this entire script
 * 5. Click Run > setupSystem
 * 6. The script will automatically create all sheets, tabs, menus, and functionality
 * 
 * FEATURES:
 * - All modules from Django system
 * - Professional government-style interface
 * - Automated calculations and validations
 * - Dashboard with KPIs
 * - Data management forms
 * - Security features
 */

// ============================================
// SYSTEM CONFIGURATION
// ============================================

const CONFIG = {
  SYSTEM_NAME: "GST Compliance System",
  VERSION: "1.0",
  AUTHOR: "GST Department",
  
  // Sheet names
  SHEETS: {
    DASHBOARD: "Dashboard",
    TAXPAYERS: "Taxpayers",
    RETURNS: "GST Returns",
    COMPLIANCE: "Compliance",
    RISK: "Risk Assessment",
    AUDIT: "Audit Cases",
    ASSESSMENTS: "Audit Assessments",
    REFUNDS: "Refunds",
    ENFORCEMENT: "Enforcement",
    REPORTS: "Reports",
    SETTINGS: "Settings"
  },
  
  // Choice values matching Django models
  CHOICES: {
    ORGANISATION_TYPES: ["Sole Proprietorship", "Partnership", "Private Limited", "Public Limited", "Government", "NGO", "Trust", "Individual"],
    SECTORS: ["Manufacturing", "Trading", "Services", "Construction", "Agriculture", "Education", "Healthcare", "IT", "Tourism", "Transport"],
    DZONGKHAGS: ["Thimphu", "Paro", "Punakha", "Wangdue", "Tsirang", "Bumthang", "Trashigang", "Mongar", "Sarpang", "Samdrup", "Trashiyangtse", "Haa", "Gasa", "Chukha", "Dagana", "Trongsa"],
    FREQUENCIES: ["Monthly", "Quarterly", "Annual"],
    STATUS: ["Active", "Inactive", "Deregistered", "Suspended"],
    FILING_STATUS: ["Filed", "Late Filed", "Not Filed", "Amended"],
    PAYMENT_STATUS: ["Paid", "Partial", "Default", "No Liability"],
    COMPLIANCE_STATUS: ["Compliant", "Late Filer", "Non-Filer", "Late Payment", "Payment Default", "Return Amendment"],
    RISK_LEVELS: ["Low", "Medium", "High", "Critical"],
    RISK_TYPES: ["Filing & Payment Risk", "Sales & Output GST Risk", "Purchase & ITC Risk", "Import & Transaction Risk", "Refund Risk", "GST Behaviour & Compliance History Risk"],
    AUDIT_TYPES: ["Field Audit", "Desk Audit", "Special Audit"],
    AUDIT_STATUS: ["Pending Assignment", "Assigned", "In Progress", "Completed", "Closed"],
    ASSESSMENT_TYPES: ["Normal Assessment", "Scrutiny Assessment", "Best Judgment Assessment"],
    REFUND_STATUS: ["submitted", "under_review", "processing", "approved", "rejected", "paid", "closed"],
    ENFORCEMENT_STATUS: ["Initiated", "Notice Issued", "Assessment Issued", "Recovery Initiated", "Recovered", "Closed"]
  }
};

// ============================================
// MAIN SETUP FUNCTION
// ============================================

function setupSystem() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  
  // Set system name
  ss.rename(CONFIG.SYSTEM_NAME);
  
  // Delete all existing sheets except the first one
  const sheets = ss.getSheets();
  for (let i = 1; i < sheets.length; i++) {
    ss.deleteSheet(sheets[i]);
  }
  
  // Rename first sheet to Dashboard
  const dashboardSheet = sheets[0];
  dashboardSheet.setName(CONFIG.SHEETS.DASHBOARD);
  
  // Create all required sheets
  createAllSheets(ss);
  
  // Setup dashboard
  setupDashboard(dashboardSheet);
  
  // Setup data sheets
  setupTaxpayerSheet(ss.getSheetByName(CONFIG.SHEETS.TAXPAYERS));
  setupReturnsSheet(ss.getSheetByName(CONFIG.SHEETS.RETURNS));
  setupComplianceSheet(ss.getSheetByName(CONFIG.SHEETS.COMPLIANCE));
  setupRiskSheet(ss.getSheetByName(CONFIG.SHEETS.RISK));
  setupAuditSheet(ss.getSheetByName(CONFIG.SHEETS.AUDIT));
  setupAssessmentsSheet(ss.getSheetByName(CONFIG.SHEETS.ASSESSMENTS));
  setupRefundsSheet(ss.getSheetByName(CONFIG.SHEETS.REFUNDS));
  setupEnforcementSheet(ss.getSheetByName(CONFIG.SHEETS.ENFORCEMENT));
  setupReportsSheet(ss.getSheetByName(CONFIG.SHEETS.REPORTS));
  setupSettingsSheet(ss.getSheetByName(CONFIG.SHEETS.SETTINGS));
  
  // Create custom menu
  createCustomMenu();
  
  // Set triggers
  setupTriggers();
  
  Browser.msgBox("✅ GST Compliance System Setup Complete!", 
    "All sheets, tabs, menus, and functionality have been created. You can now use the system.",
    Browser.Buttons.OK);
}

// ============================================
// SHEET CREATION
// ============================================

function createAllSheets(ss) {
  // Create sheets if they don't exist
  const sheetNames = Object.values(CONFIG.SHEETS);
  
  sheetNames.forEach(name => {
    if (!ss.getSheetByName(name)) {
      ss.insertSheet(name);
    }
  });
  
  // Hide settings sheet
  const settingsSheet = ss.getSheetByName(CONFIG.SHEETS.SETTINGS);
  if (settingsSheet) {
    settingsSheet.hideSheet();
  }
}

// ============================================
// DASHBOARD SETUP
// ============================================

function setupDashboard(sheet) {
  // Clear the sheet
  sheet.clear();
  
  // Set up header
  sheet.getRange("A1").setValue(CONFIG.SYSTEM_NAME);
  sheet.getRange("A1").setFontWeight("bold").setFontSize(20).setFontColor("#667eea");
  sheet.getRange("A1:B1").merge();
  
  sheet.getRange("A2").setValue("Version " + CONFIG.VERSION + " | " + CONFIG.AUTHOR);
  sheet.getRange("A2").setFontStyle("italic").setFontColor("#666");
  sheet.getRange("A2:B2").merge();
  
  // Add navigation cards
  const cards = [
    {name: "📊 GST Reports", desc: "Centralized Reporting and Analytics Layer", url: "#", row: 4},
    {name: "✅ Compliance & Enforcement", desc: "Compliance monitoring, risk assessment, and enforcement", url: "#", row: 5},
    {name: "🔍 Audit & Refund", desc: "Audit case management and refund processing", url: "#", row: 6},
    {name: "💰 Taxpayer Management", desc: "Taxpayer registration and master data", url: "#", row: 7},
    {name: "📋 GST Returns", desc: "Return filing and revenue management", url: "#", row: 8},
    {name: "⚠️ Risk Assessment", desc: "Risk evaluation and selection process", url: "#", row: 9},
  ];
  
  cards.forEach(card => {
    sheet.getRange("A" + card.row).setValue(card.name);
    sheet.getRange("A" + card.row).setFontWeight("bold").setFontSize(14);
    sheet.getRange("B" + card.row).setValue(card.desc);
    sheet.getRange("B" + card.row).setFontStyle("italic").setFontColor("#666");
  });
  
  // Add KPIs section
  sheet.getRange("A11").setValue("📊 KEY PERFORMANCE INDICATORS");
  sheet.getRange("A11").setFontWeight("bold").setFontSize(16).setFontColor("#667eea");
  sheet.getRange("A11:F11").merge();
  
  // KPI cards
  const kpis = [
    {label: "Active Taxpayers", value: "0", row: 12, col: "A"},
    {label: "Returns Filed", value: "0", row: 12, col: "C"},
    {label: "Compliance Rate", value: "0%", row: 12, col: "E"},
    {label: "Audit Cases", value: "0", row: 13, col: "A"},
    {label: "Refund Claims", value: "0", row: 13, col: "C"},
    {label: "Enforcement Cases", value: "0", row: 13, col: "E"},
  ];
  
  kpis.forEach(kpi => {
    sheet.getRange(kpi.col + kpi.row).setValue(kpi.label);
    sheet.getRange(kpi.col + kpi.row).setFontWeight("bold").setFontSize(11);
    sheet.getRange(kpi.col + (kpi.row + 1)).setValue(kpi.value);
    sheet.getRange(kpi.col + (kpi.row + 1)).setFontWeight("bold").setFontSize(24).setFontColor("#667eea");
  });
  
  // Set column widths
  sheet.setColumnWidth(1, 300);
  sheet.setColumnWidth(2, 400);
  sheet.setColumnWidth(3, 150);
  sheet.setColumnWidth(4, 150);
  sheet.setColumnWidth(5, 150);
  sheet.setColumnWidth(6, 150);
  
  // Add borders and formatting
  const dashboardRange = sheet.getRange("A1:F15");
  dashboardRange.setBorder(true, true, true, true);
  
  // Freeze first row
  sheet.setFrozenRows(1);
}

// ============================================
// TAXPAYER SHEET SETUP
// ============================================

function setupTaxpayerSheet(sheet) {
  // Clear the sheet
  sheet.clear();
  
  // Set up headers
  const headers = [
    "GSTIN",
    "Taxpayer Name",
    "Business Name",
    "Organisation Type",
    "Sector",
    "Dzongkhag",
    "Frequency",
    "Registration Date",
    "Status",
    "License Number",
    "Contact Person",
    "Phone",
    "Email",
    "Address",
    "License Valid From",
    "License Valid To"
  ];
  
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  sheet.getRange(1, 1, 1, headers.length).setFontWeight("bold").setBackground("#667eea").setFontColor("white");
  
  // Set data validation for dropdowns
  const orgTypeRange = sheet.getRange(2, 4, 1000, 4);
  const sectorRange = sheet.getRange(2, 5, 1000, 5);
  const dzongkhagRange = sheet.getRange(2, 6, 1000, 6);
  const frequencyRange = sheet.getRange(2, 7, 1000, 7);
  const statusRange = sheet.getRange(2, 9, 1000, 9);
  
  const orgTypeRule = SpreadsheetApp.newDataValidation().setValues(CONFIG.CHOICES.ORGANISATION_TYPES).build();
  const sectorRule = SpreadsheetApp.newDataValidation().setValues(CONFIG.CHOICES.SECTORS).build();
  const dzongkhagRule = SpreadsheetApp.newDataValidation().setValues(CONFIG.CHOICES.DZONGKHAGS).build();
  const frequencyRule = SpreadsheetApp.newDataValidation().setValues(CONFIG.CHOICES.FREQUENCIES).build();
  const statusRule = SpreadsheetApp.newDataValidation().setValues(CONFIG.CHOICES.STATUS).build();
  
  orgTypeRange.setDataValidation(orgTypeRule);
  sectorRange.setDataValidation(sectorRule);
  dzongkhagRange.setDataValidation(dzongkhagRule);
  frequencyRange.setDataValidation(frequencyRule);
  statusRange.setDataValidation(statusRule);
  
  // Set column widths
  headers.forEach((_, index) => {
    sheet.setColumnWidth(index + 1, 150);
  });
  
  // Freeze header row
  sheet.setFrozenRows(1);
  
  // Protect header row
  const headerProtection = sheet.protect().setDescription("Taxpayer headers are protected");
  headerProtection.removeEditors(Session.getActiveUser());
  headerProtection.addEditor(sheet.getRange(1, 1, 1, headers.length));
}

// ============================================
// GST RETURNS SHEET SETUP
// ============================================

function setupReturnsSheet(sheet) {
  sheet.clear();
  
  const headers = [
    "GSTIN",
    "Taxpayer Name",
    "Tax Period",
    "Declared Sales",
    "Domestic Purchase",
    "Import Value",
    "Output GST",
    "ITC Claimed",
    "GST Payable/Refundable",
    "Filing Status",
    "Payment Status",
    "Compliance Status",
    "Return Due Date",
    "Return Filing Date",
    "Actual GST Payment",
    "Remarks"
  ];
  
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  sheet.getRange(1, 1, 1, headers.length).setFontWeight("bold").setBackground("#667eea").setFontColor("white");
  
  // Data validation
  const filingStatusRange = sheet.getRange(2, 11, 1000, 11);
  const paymentStatusRange = sheet.getRange(2, 12, 1000, 12);
  const complianceStatusRange = sheet.getRange(2, 13, 1000, 13);
  
  const filingStatusRule = SpreadsheetApp.newDataValidation().setValues(CONFIG.CHOICES.FILING_STATUS).build();
  const paymentStatusRule = SpreadsheetApp.newDataValidation().setValues(CONFIG.CHOICES.PAYMENT_STATUS).build();
  const complianceStatusRule = SpreadsheetApp.newDataValidation().setValues(CONFIG.CHOICES.COMPLIANCE_STATUS).build();
  
  filingStatusRange.setDataValidation(filingStatusRule);
  paymentStatusRange.setDataValidation(paymentStatusRule);
  complianceStatusRange.setDataValidation(complianceStatusRule);
  
  headers.forEach((_, index) => {
    sheet.setColumnWidth(index + 1, 140);
  });
  
  sheet.setFrozenRows(1);
}

// ============================================
// COMPLIANCE SHEET SETUP
// ============================================

function setupComplianceSheet(sheet) {
  sheet.clear();
  
  const headers = [
    "Compliance ID",
    "GSTIN",
    "Taxpayer Name",
    "Tax Period",
    "Filing Status",
    "Filing Delay (Days)",
    "Payment Status",
    "Compliance Status",
    "Compliance Flag",
    "Assessment Date",
    "Remarks"
  ];
  
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  sheet.getRange(1, 1, 1, headers.length).setFontWeight("bold").setBackground("#667eea").setFontColor("white");
  
  const complianceStatusRange = sheet.getRange(2, 8, 1000, 8);
  const complianceFlagRange = sheet.getRange(2, 9, 1000, 9);
  
  const complianceStatusRule = SpreadsheetApp.newDataValidation().setValues(CONFIG.CHOICES.COMPLIANCE_STATUS).build();
  const complianceFlagRule = SpreadsheetApp.newDataValidation().setValues(["Green", "Yellow", "Red"]).build();
  
  complianceStatusRange.setDataValidation(complianceStatusRule);
  complianceFlagRange.setDataValidation(complianceFlagRule);
  
  headers.forEach((_, index) => {
    sheet.setColumnWidth(index + 1, 150);
  });
  
  sheet.setFrozenRows(1);
}

// ============================================
// RISK ASSESSMENT SHEET SETUP
// ============================================

function setupRiskSheet(sheet) {
  sheet.clear();
  
  const headers = [
    "Risk ID",
    "GSTIN",
    "Taxpayer Name",
    "Assessment From Period",
    "Assessment To Period",
    "Risk Type",
    "Risk Indicator",
    "Risk Score",
    "Risk Level",
    "Filing Indicator",
    "Payment Indicator",
    "Selection Decision",
    "Selection By",
    "Selection Date",
    "Final Selection",
    "Remarks"
  ];
  
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  sheet.getRange(1, 1, 1, headers.length).setFontWeight("bold").setBackground("#667eea").setFontColor("white");
  
  const riskTypeRange = sheet.getRange(2, 7, 1000, 7);
  const riskLevelRange = sheet.getRange(2, 9, 1000, 9);
  const finalSelectionRange = sheet.getRange(2, 16, 1000, 16);
  
  const riskTypeRule = SpreadsheetApp.newDataValidation().setValues(CONFIG.CHOICES.RISK_TYPES).build();
  const riskLevelRule = SpreadsheetApp.newDataValidation().setValues(CONFIG.CHOICES.RISK_LEVELS).build();
  const finalSelectionRule = SpreadsheetApp.newDataValidation().setValues(["AUDIT", "REVIEW", "MONITOR", "NOT SELECTED"]).build();
  
  riskTypeRange.setDataValidation(riskTypeRule);
  riskLevelRange.setDataValidation(riskLevelRule);
  finalSelectionRange.setDataValidation(finalSelectionRule);
  
  headers.forEach((_, index) => {
    sheet.setColumnWidth(index + 1, 150);
  });
  
  sheet.setFrozenRows(1);
}

// ============================================
// AUDIT CASES SHEET SETUP
// ============================================

function setupAuditSheet(sheet) {
  sheet.clear();
  
  const headers = [
    "Audit Case ID",
    "GSTIN",
    "Taxpayer Name",
    "From Tax Period",
    "To Tax Period",
    "Assessment Type",
    "Audit Type",
    "Status",
    "Assigned Officer",
    "Assigned Date",
    "Due Date",
    "Completion Date",
    "Remarks"
  ];
  
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  sheet.getRange(1, 1, 1, headers.length).setFontWeight("bold").setBackground("#667eea").setFontColor("white");
  
  const auditTypeRange = sheet.getRange(2, 7, 1000, 7);
  const statusRange = sheet.getRange(2, 8, 1000, 8);
  
  const auditTypeRule = SpreadsheetApp.newDataValidation().setValues(CONFIG.CHOICES.AUDIT_TYPES).build();
  const statusRule = SpreadsheetApp.newDataValidation().setValues(CONFIG.CHOICES.AUDIT_STATUS).build();
  
  auditTypeRange.setDataValidation(auditTypeRule);
  statusRange.setDataValidation(statusRule);
  
  headers.forEach((_, index) => {
    sheet.setColumnWidth(index + 1, 150);
  });
  
  sheet.setFrozenRows(1);
}

// ============================================
// AUDIT ASSESSMENTS SHEET SETUP
// ============================================

function setupAssessmentsSheet(sheet) {
  sheet.clear();
  
  const headers = [
    "Assessment ID",
    "Audit Case ID",
    "GSTIN",
    "Taxpayer Name",
    "Tax Period",
    "Declared Sales",
    "Assessed Sales",
    "Declared Output GST",
    "Assessed Output GST",
    "Difference",
    "Shortfall Amount",
    "Amount Recovered",
    "Assessment Type",
    "Assessor",
    "Assessment Date",
    "Outcome",
    "Remarks"
  ];
  
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  sheet.getRange(1, 1, 1, headers.length).setFontWeight("bold").setBackground("#667eea").setFontColor("white");
  
  const assessmentTypeRange = sheet.getRange(2, 13, 1000, 13);
  
  const assessmentTypeRule = SpreadsheetApp.newDataValidation().setValues(CONFIG.CHOICES.ASSESSMENT_TYPES).build();
  assessmentTypeRange.setDataValidation(assessmentTypeRule);
  
  headers.forEach((_, index) => {
    sheet.setColumnWidth(index + 1, 150);
  });
  
  sheet.setFrozenRows(1);
}

// ============================================
// REFUNDS SHEET SETUP
// ============================================

function setupRefundsSheet(sheet) {
  sheet.clear();
  
  const headers = [
    "Refund ID",
    "GST/TPN",
    "Taxpayer Name",
    "Tax Period",
    "Claimed Amount",
    "Refund Approved",
    "Adjustment",
    "Status",
    "Submitted Date",
    "Approved Date",
    "Processing Officer",
    "Remarks"
  ];
  
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  sheet.getRange(1, 1, 1, headers.length).setFontWeight("bold").setBackground("#667eea").setFontColor("white");
  
  const statusRange = sheet.getRange(2, 8, 1000, 8);
  
  const statusRule = SpreadsheetApp.newDataValidation().setValues(CONFIG.CHOICES.REFUND_STATUS).build();
  statusRange.setDataValidation(statusRule);
  
  headers.forEach((_, index) => {
    sheet.setColumnWidth(index + 1, 150);
  });
  
  sheet.setFrozenRows(1);
}

// ============================================
// ENFORCEMENT SHEET SETUP
// ============================================

function setupEnforcementSheet(sheet) {
  sheet.clear();
  
  const headers = [
    "Case ID",
    "GSTIN",
    "Taxpayer Name",
    "Tax Period",
    "Case Type",
    "Amount Due",
    "Amount Recovered",
    "Outstanding",
    "Status",
    "Notice Date",
    "Assigned Officer",
    "Remarks"
  ];
  
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  sheet.getRange(1, 1, 1, headers.length).setFontWeight("bold").setBackground("#667eea").setFontColor("white");
  
  const statusRange = sheet.getRange(2, 9, 1000, 9);
  
  const statusRule = SpreadsheetApp.newDataValidation().setValues(CONFIG.CHOICES.ENFORCEMENT_STATUS).build();
  statusRange.setDataValidation(statusRule);
  
  headers.forEach((_, index) => {
    sheet.setColumnWidth(index + 1, 150);
  });
  
  sheet.setFrozenRows(1);
}

// ============================================
// REPORTS SHEET SETUP
// ============================================

function setupReportsSheet(sheet) {
  sheet.clear();
  
  // Report categories
  const reportCategories = [
    "📊 Management Reports",
    "👥 Taxpayer Reports", 
    "💰 GST Return & Revenue Reports",
    "✅ Compliance Reports",
    "⚠️ Risk & Selection Reports",
    "🔍 Audit Reports",
    "💸 Refund Reports",
    "⚖️ Enforcement Reports",
    "👔 Officer/Workload Reports",
    "🔧 Custom Reports"
  ];
  
  sheet.getRange("A1").setValue("📊 GST REPORTS");
  sheet.getRange("A1").setFontWeight("bold").setFontSize(20).setFontColor("#667eea");
  
  sheet.getRange("A3").setValue("Select a report category to view available reports:");
  sheet.getRange("A3").setFontStyle("italic").setFontColor("#666");
  
  reportCategories.forEach((category, index) => {
    sheet.getRange("A" + (index + 5)).setValue(category);
    sheet.getRange("A" + (index + 5)).setFontWeight("bold").setFontSize(14);
  });
  
  sheet.setColumnWidth(1, 400);
  sheet.setFrozenRows(1);
}

// ============================================
// SETTINGS SHEET SETUP
// ============================================

function setupSettingsSheet(sheet) {
  sheet.clear();
  
  const settings = [
    ["System Name", CONFIG.SYSTEM_NAME],
    ["Version", CONFIG.VERSION],
    ["Created Date", new Date()],
    ["Author", CONFIG.AUTHOR],
    ["", ""],
    ["Tax Period Format", "Jan-2026"],
    ["Date Format", "DD-MM-YYYY"],
    ["", ""],
    ["Sheet Names", Object.values(CONFIG.SHEETS).join(", ")],
  ];
  
  sheet.getRange("A1:B" + settings.length).setValues(settings);
  sheet.getRange("A1:A" + settings.length).setFontWeight("bold");
  
  sheet.setColumnWidth(1, 200);
  sheet.setColumnWidth(2, 300);
}

// ============================================
// CUSTOM MENU CREATION
// ============================================

function createCustomMenu() {
  const ui = SpreadsheetApp.getUi();
  
  ui.createMenu(CONFIG.SYSTEM_NAME)
    .addItem("📊 Dashboard", "showDashboard")
    .addItem("👥 Taxpayer Management", "showTaxpayers")
    .addItem("📋 GST Returns", "showReturns")
    .addItem("✅ Compliance", "showCompliance")
    .addItem("⚠️ Risk Assessment", "showRisk")
    .addItem("🔍 Audit Cases", "showAudit")
    .addItem("📝 Audit Assessments", "showAssessments")
    .addItem("💸 Refunds", "showRefunds")
    .addItem("⚖️ Enforcement", "showEnforcement")
    .addItem("📊 Reports", "showReports")
    .addSeparator()
    .addItem("🔄 Refresh Dashboard", "refreshDashboard")
    .addItem("⚙️ Settings", "showSettings")
    .addSeparator()
    .addItem("❓ Help", "showHelp");
}

// ============================================
// MENU HANDLERS
// ============================================

function showDashboard() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  ss.getSheetByName(CONFIG.SHEETS.DASHBOARD).activate();
}

function showTaxpayers() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  ss.getSheetByName(CONFIG.SHEETS.TAXPAYERS).activate();
}

function showReturns() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  ss.getSheetByName(CONFIG.SHEETS.RETURNS).activate();
}

function showCompliance() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  ss.getSheetByName(CONFIG.SHEETS.COMPLIANCE).activate();
}

function showRisk() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  ss.getSheetByName(CONFIG.SHEETS.RISK).activate();
}

function showAudit() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  ss.getSheetByName(CONFIG.SHEETS.AUDIT).activate();
}

function showAssessments() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  ss.getSheetByName(CONFIG.SHEETS.ASSESSMENTS).activate();
}

function showRefunds() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  ss.getSheetByName(CONFIG.SHEETS.REFUNDS).activate();
}

function showEnforcement() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  ss.getSheetByName(CONFIG.SHEETS.ENFORCEMENT).activate();
}

function showReports() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  ss.getSheetByName(CONFIG.SHEETS.REPORTS).activate();
}

function showSettings() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  ss.getSheetByName(CONFIG.SHEETS.SETTINGS).activate();
}

function showHelp() {
  const htmlOutput = HtmlService.createHtmlOutput(`
    <h2>${CONFIG.SYSTEM_NAME} Help</h2>
    <p><strong>Version:</strong> ${CONFIG.VERSION}</p>
    <p><strong>Author:</strong> ${CONFIG.AUTHOR}</p>
    <h3>Quick Start:</h3>
    <ol>
      <li>Use the custom menu to navigate between modules</li>
      <li>Add data to the respective sheets</li>
      <li>Dashboard will automatically update KPIs</li>
      <li>All dropdown choices are pre-configured</li>
    </ol>
    <h3>Modules:</h3>
    <ul>
      <li><strong>Taxpayers:</strong> Manage taxpayer master data</li>
      <li><strong>GST Returns:</strong> Track return filings and payments</li>
      <li><strong>Compliance:</strong> Monitor compliance status</li>
      <li><strong>Risk:</strong> Risk assessment and selection</li>
      <li><strong>Audit:</strong> Audit case management</li>
      <li><strong>Refunds:</strong> Refund processing</li>
      <li><strong>Enforcement:</strong> Recovery management</li>
    </ul>
  `)
  .setWidth(400)
  .setHeight(600);
  
  SpreadsheetApp.getUi().showModalDialog(htmlOutput, "Help");
}

function refreshDashboard() {
  updateDashboardKPIs();
  Browser.msgBox("Dashboard refreshed!", "KPIs have been updated.", Browser.Buttons.OK);
}

// ============================================
// DASHBOARD KPI UPDATE
// ============================================

function updateDashboardKPIs() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const dashboardSheet = ss.getSheetByName(CONFIG.SHEETS.DASHBOARD);
  
  // Get data from other sheets
  const taxpayerSheet = ss.getSheetByName(CONFIG.SHEETS.TAXPAYERS);
  const returnsSheet = ss.getSheetByName(CONFIG.SHEETS.RETURNS);
  const auditSheet = ss.getSheetByName(CONFIG.SHEETS.AUDIT);
  const refundsSheet = ss.getSheetByName(CONFIG.SHEETS.REFUNDS);
  const enforcementSheet = ss.getSheetByName(CONFIG.SHEETS.ENFORCEMENT);
  
  // Calculate KPIs
  const activeTaxpayers = taxpayerSheet.getLastRow() > 1 ? taxpayerSheet.getLastRow() - 1 : 0;
  const returnsFiled = returnsSheet.getLastRow() > 1 ? returnsSheet.getLastRow() - 1 : 0;
  const auditCases = auditSheet.getLastRow() > 1 ? auditSheet.getLastRow() - 1 : 0;
  const refundClaims = refundsSheet.getLastRow() > 1 ? refundsSheet.getLastRow() - 1 : 0;
  const enforcementCases = enforcementSheet.getLastRow() > 1 ? enforcementSheet.getLastRow() - 1 : 0;
  
  // Calculate compliance rate
  const complianceSheet = ss.getSheetByName(CONFIG.SHEETS.COMPLIANCE);
  const compliantRecords = complianceSheet.getLastRow() > 1 ? 
    complianceSheet.getRange(2, 8, complianceSheet.getLastRow(), 8).getValues().filter(row => row[0] === "Compliant").length : 0;
  const totalRecords = complianceSheet.getLastRow() > 1 ? complianceSheet.getLastRow() - 1 : 0;
  const complianceRate = totalRecords > 0 ? Math.round((compliantRecords / totalRecords) * 100) + "%" : "0%";
  
  // Update KPIs on dashboard
  dashboardSheet.getRange("C13").setValue(activeTaxpayers);
  dashboardSheet.getRange("D13").setValue(returnsFiled);
  dashboardSheet.getRange("F13").setValue(complianceRate);
  dashboardSheet.getRange("C14").setValue(auditCases);
  dashboardSheet.getRange("D14").setValue(refundClaims);
  dashboardSheet.getRange("F14").setValue(enforcementCases);
}

// ============================================
// AUTOMATED CALCULATIONS
// ============================================

function onEdit(e) {
  const range = e.range;
  const sheet = range.getSheet();
  
  // Trigger calculations when compliance status changes
  if (sheet.getName() === CONFIG.SHEETS.COMPLIANCE && range.getColumn() === 8) {
    calculateComplianceFlag(sheet, range.getRow());
  }
  
  // Refresh dashboard when data changes
  updateDashboardKPIs();
}

function calculateComplianceFlag(sheet, row) {
  const complianceStatus = sheet.getRange(row, 8).getValue();
  const flagCell = sheet.getRange(row, 9);
  
  let flag = "";
  let bgColor = "";
  
  switch(complianceStatus) {
    case "Compliant":
      flag = "Green";
      bgColor = "#4CAF50";
      break;
    case "Late Filer":
      flag = "Yellow";
      bgColor = "#FFC107";
      break;
    case "Non-Filer":
    case "Payment Default":
      flag = "Red";
      bgColor = "#F44336";
      break;
    default:
      flag = "Yellow";
      bgColor = "#FFC107";
  }
  
  flagCell.setValue(flag);
  flagCell.setBackground(bgColor).setFontColor("white");
}

// ============================================
// TRIGGER SETUP
// ============================================

function setupTriggers() {
  // Delete existing triggers
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(trigger => {
    ScriptApp.deleteTrigger(trigger);
  });
  
  // Create new triggers
  ScriptApp.newTrigger("onEdit")
    .forSpreadsheet(SpreadsheetApp.getActiveSpreadsheet())
    .onEdit()
    .create();
}

// ============================================
// UTILITY FUNCTIONS
// ============================================

function generateID(prefix, sheet, column) {
  const lastRow = sheet.getLastRow();
  let nextNumber = 1;
  
  if (lastRow > 1) {
    const lastID = sheet.getRange(lastRow, column).getValue();
    if (lastID) {
      const lastNumber = parseInt(lastID.split("-")[1]);
      nextNumber = lastNumber + 1;
    }
  }
  
  return `${prefix}-${String(nextNumber).padStart(4, '0')}`;
}

function formatDate(date) {
  return Utilities.formatDate(new Date(date), "dd-MM-yyyy");
}

function getCurrentTaxPeriod() {
  const now = new Date();
  const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  return `${monthNames[now.getMonth()]}-${now.getFullYear()}`;
}

// ============================================
// DATA IMPORT/EXPORT FUNCTIONS
// ============================================

function exportDataToCSV(sheetName) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(sheetName);
  
  const data = sheet.getDataRange().getValues();
  const csv = data.map(row => row.join(",")).join("\n");
  
  const blob = Utilities.newBlob(csv, sheetName + ".csv", "text/csv");
  
  // Create a temporary file in Drive
  const file = DriveApp.createFile(blob);
  
  Browser.msgBox("Export Complete", "Data exported to Drive as CSV: " + file.getUrl(), Browser.Buttons.OK);
}

function importFromCSV() {
  const htmlOutput = HtmlService.createHtmlOutput(`
    <h2>Import Data from CSV</h2>
    <p>Upload a CSV file to import data into the system.</p>
    <input type="file" id="csvFile" accept=".csv">
    <button onclick="uploadCSV()">Upload</button>
    <script>
    function uploadCSV() {
      const file = document.getElementById('csvFile').files[0];
      const reader = new FileReader();
      reader.onload = function(e) {
        google.script.run.processCSV(e.target.result);
      };
      reader.readAsText(file);
    }
    </script>
  `)
  .setWidth(400)
  .setHeight(300);
  
  SpreadsheetApp.getUi().showModalDialog(htmlOutput, "Import CSV");
}

function processCSV(csvData) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getActiveSheet();
  
  const rows = csvData.split("\n");
  const data = rows.map(row => row.split(","));
  
  sheet.getRange(sheet.getLastRow() + 1, 1, sheet.getLastRow() + data.length, data[0].length).setValues(data);
  
  Browser.msgBox("Import Complete", "Data imported successfully!", Browser.Buttons.OK);
}

// ============================================
// VALIDATION FUNCTIONS
// ============================================

function validateGSTIN(gstin) {
  // GSTIN validation logic (simplified)
  const gstinPattern = /^[A-Z]{2}[0-9A-Z]{10}[A-Z]{2}[A-Z0-9]{2}$/;
  return gstinPattern.test(gstin);
}

function validateTaxPeriod(taxPeriod) {
  // Validate tax period format (Jan-2026)
  const pattern = /^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-\d{4}$/;
  return pattern.test(taxPeriod);
}

// ============================================
// AUTOMATED REPORT GENERATION
// ============================================

function generateExecutiveSummary() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  
  // Create new sheet for report
  const reportSheet = ss.insertSheet("Executive Summary");
  
  // Add report content
  reportSheet.getRange("A1").setValue("EXECUTIVE GST SUMMARY");
  reportSheet.getRange("A1").setFontWeight("bold").setFontSize(20).setFontColor("#667eea");
  
  reportSheet.getRange("A3").setValue("Generated: " + formatDate(new Date()));
  
  // Add KPIs
  const kpis = updateDashboardKPIs();
  
  const summaryData = [
    ["KPI", "Value"],
    ["Active Taxpayers", "=COUNTA(Taxpayers!A:A)-1"],
    ["Returns Filed", "=COUNTA('GST Returns'!A:A)-1"],
    ["Compliance Rate", "=COUNTIF(Compliance!H:H, 'Compliant')/COUNTA(Compliance!A:A)-1"],
    ["Audit Cases", "=COUNTA('Audit Cases'!A:A)-1"],
    ["Refund Claims", "=COUNTA(Refunds!A:A)-1"],
    ["Enforcement Cases", "=COUNTA(Enforcement!A:A)-1"]
  ];
  
  reportSheet.getRange("A5:B11").setValues(summaryData);
  reportSheet.getRange("A5:B5").setFontWeight("bold").setBackground("#667eea").setFontColor("white");
  
  Browser.msgBox("Report Generated", "Executive Summary report has been generated.", Browser.Buttons.OK);
}

// ============================================
// OPEN ON INSTALLATION
// ============================================

function onOpen() {
  createCustomMenu();
  updateDashboardKPIs();
}