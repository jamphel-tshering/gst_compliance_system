"""
Test file for Audit Allotment import
"""
import pandas as pd

# Create test data with actual taxpayers from the system
test_data = {
    'Tax Period': ['Jan-2026', 'Jan-2026', 'Jan-2026'],
    'GSTIN': ['P10290800', 'P10290801', 'P10290802'],
    'Taxpayer Name': ['Dorji Namgay', 'Tashi Wangchuk', 'Karma Wangmo'],
    'Dzongkhag': ['Mongar', 'Trashigang', 'Trashiyangtse'],
    'Organisation Type': ['Sole Proprietorship', 'Private Company', 'Partnership'],
    'Frequency': ['Monthly', 'Quarterly', 'Monthly'],
    'Assessor': ['admin', 'admin', 'admin'],  # Using admin username
    'Allotment Date': ['01-06-2026', '02-06-2026', '03-06-2026'],
    'Remarks': ['High risk taxpayer', 'Import business', 'New registrant']
}

# Create DataFrame
df = pd.DataFrame(test_data)

# Save to Excel
df.to_excel('test_audit_allotment.xlsx', index=False, sheet_name='Audit Allotments')

print("Test file created: test_audit_allotment.xlsx")
print("This file can be used to test the import functionality.")
print("Note: Make sure the GSTINs exist in your Taxpayer Master and 'admin' user exists.")
print("Column names match the resource configuration exactly.")