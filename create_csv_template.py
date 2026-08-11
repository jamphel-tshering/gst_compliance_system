"""
Create CSV template for Audit Allotment import - CSV files don't have 'id' column issues
"""
import pandas as pd

# Define the template structure (empty rows for user to fill)
template_data = {
    'Tax Period': [],
    'GSTIN': [],
    'Taxpayer Name': [],
    'Dzongkhag': [],
    'Organization Type': [],
    'Frequency': [],
    'Assessor': [],
    'Allotment Date': [],
    'Remarks': []
}

# Create DataFrame
df = pd.DataFrame(template_data)

# Save to CSV
df.to_csv('audit_allotment_template.csv', index=False)

print("CSV template created successfully: audit_allotment_template.csv")
print("CSV files are simpler and don't have 'id' column issues.")
print("Columns included:", list(df.columns))
print("\nColumn Guidelines:")
print("- Tax Period: Format Jan-2026 (e.g., Jan-2026, Feb-2026)")
print("- GSTIN: Valid GSTIN from Taxpayer Master")
print("- Taxpayer Name: Full taxpayer name")
print("- Dzongkhag: Mongar, Trashigang, Trashiyangtse, Lhuntse")
print("- Organization Type: Sole Proprietorship, Private Company, Public Company, Partnership, State Owned Company, Joint Venture, Foreign Company")
print("- Frequency: Monthly, Quarterly, Annual")
print("- Assessor: Email address or username of existing user")
print("- Allotment Date: Format YYYY-MM-DD (e.g., 2026-06-01) - this format is more reliable")
print("- Remarks: Optional notes")