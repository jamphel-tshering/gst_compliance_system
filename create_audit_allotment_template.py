"""
Create Excel template for Audit Allotment import
"""
import pandas as pd

# Define the template structure (empty rows for user to fill)
template_data = {
    'Tax Period': [],
    'GSTIN': [],
    'Taxpayer Name': [],
    'Dzongkhag': [],
    'Organisation Type': [],
    'Frequency': [],
    'Assessor': [],
    'Allotment Date': [],
    'Remarks': []
}

# Create DataFrame
df = pd.DataFrame(template_data)

# Save to Excel
df.to_excel('audit_allotment_template.xlsx', index=False, sheet_name='Audit Allotments')

print("Excel template created successfully: audit_allotment_template.xlsx")
print("Columns included:", list(df.columns))
print("\nColumn Guidelines:")
print("- Tax Period: Format Jan-2026 (e.g., Jan-2026, Feb-2026)")
print("- GSTIN: Valid GSTIN from Taxpayer Master")
print("- Taxpayer Name: Full taxpayer name")
print("- Dzongkhag: Mongar, Trashigang, Trashiyangtse, Lhuntse")
print("- Organisation Type: Sole Proprietorship, Private Company, Public Company, Partnership, State Owned Company, Joint Venture, Foreign Company")
print("- Frequency: Monthly, Quarterly, Annual")
print("- Assessor: Email address or username of existing user")
print("- Allotment Date: Format dd-mm-yyyy (e.g., 01-06-2026)")
print("- Remarks: Optional notes")
print("\nIMPORTANT: Do not add an 'id' column to the Excel file. The system handles this automatically.")
print("\nYou can now use this template to import audit allotments via the admin interface.")