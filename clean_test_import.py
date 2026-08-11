"""
Clean test CSV file for Audit Allotment import - No empty rows
"""
import pandas as pd

# Create test data with proper date format and no empty values
test_data = {
    'Tax Period': ['Jan-2026', 'Jan-2026', 'Jan-2026'],
    'GSTIN': ['P10290800', 'P10290801', 'P10290802'],
    'Taxpayer Name': ['Dorji Namgay', 'Tashi Wangchuk', 'Karma Wangmo'],
    'Dzongkhag': ['Mongar', 'Trashigang', 'Trashiyangtse'],
    'Organization Type': ['Sole Proprietorship', 'Private Company', 'Partnership'],
    'Frequency': ['Monthly', 'Quarterly', 'Monthly'],
    'Assessor': ['admin', 'admin', 'admin'],
    'Allotment Date': ['2026-06-01', '2026-06-02', '2026-06-03'],
    'Remarks': ['High risk taxpayer', 'Import business', 'New registrant']
}

# Create DataFrame
df = pd.DataFrame(test_data)

# Save to CSV
df.to_csv('clean_test_audit_allotment.csv', index=False)

print("Clean test CSV file created: clean_test_audit_allotment.csv")
print("This file has no empty rows and should import successfully.")
print("Column names:", list(df.columns))
print("All fields have proper values.")