"""
Simple test file for Audit Allotment import - guaranteed no 'id' column
"""
import pandas as pd

# Create minimal test data
test_data = {
    'Tax Period': ['Jan-2026'],
    'GSTIN': ['P10290800'],
    'Taxpayer Name': ['Dorji Namgay'],
    'Dzongkhag': ['Mongar'],
    'Organisation Type': ['Sole Proprietorship'],
    'Frequency': ['Monthly'],
    'Assessor': ['admin'],
    'Allotment Date': ['01-06-2026'],
    'Remarks': ['Test import']
}

# Create DataFrame
df = pd.DataFrame(test_data)

# Save to Excel with no index (this prevents Excel from adding an index column)
df.to_excel('simple_test.xlsx', index=False, sheet_name='Audit Allotments')

print("Simple test file created: simple_test.xlsx")
print("This file has no 'id' column and only one row for testing.")
print("Column names:", list(df.columns))