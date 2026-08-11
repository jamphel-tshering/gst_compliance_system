"""
Test CSV file for Audit Allotment import - CSV is more reliable than Excel
"""
import pandas as pd

# Create test data with proper date format
test_data = {
    'Tax Period': ['Jan-2026', 'Jan-2026', 'Jan-2026'],
    'GSTIN': ['P10290800', 'P10290801', 'P10290802'],
    'Taxpayer Name': ['Dorji Namgay', 'Tashi Wangchuk', 'Karma Wangmo'],
    'Dzongkhag': ['Mongar', 'Trashigang', 'Trashiyangtse'],
    'Organization Type': ['Sole Proprietorship', 'Private Company', 'Partnership'],
    'Frequency': ['Monthly', 'Quarterly', 'Monthly'],
    'Assessor': ['admin', 'admin', 'admin'],
    'Allotment Date': ['2026-06-01', '2026-06-02', '2026-06-03'],  # Using YYYY-MM-DD format
    'Remarks': ['High risk taxpayer', 'Import business', '']  # Empty string for last one
}

# Create DataFrame
df = pd.DataFrame(test_data)

# Save to CSV
df.to_csv('test_audit_allotment.csv', index=False)

print("Test CSV file created: test_audit_allotment.csv")
print("CSV files are more reliable for import and don't have 'id' column issues.")
print("Column names:", list(df.columns))
print("Date format: YYYY-MM-DD (2026-06-01) for better compatibility")
print("Column name: Organization Type (American spelling)")
print("Remarks field: Can be empty string")
print("All fields are now nullable in database to prevent NOT NULL constraint errors")