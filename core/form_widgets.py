"""
Custom form widgets for GST Compliance System
"""
from django import forms
from django.forms import DateInput
from datetime import datetime


class CustomDateInput(DateInput):
    """Custom date input widget with dd-mm-yyyy format"""
    input_type = 'text'
    
    def __init__(self, attrs=None):
        default_attrs = {'type': 'text', 'placeholder': 'DD-MM-YYYY', 'pattern': r'\d{2}-\d{2}-\d{4}'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)
    
    def format_value(self, value):
        """Format date value to dd-mm-yyyy for display"""
        if value:
            if isinstance(value, str):
                # Try to parse various date formats
                for fmt in ['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y']:
                    try:
                        parsed_date = datetime.strptime(value, fmt)
                        return parsed_date.strftime('%d-%m-%Y')
                    except ValueError:
                        continue
                return value
            else:
                # Convert datetime to DD-MM-YYYY
                return value.strftime('%d-%m-%Y')
        return ''


class TaxPeriodSelect(forms.Select):
    """Custom select widget for tax periods in Jan-2026 format"""
    def __init__(self, attrs=None):
        # Generate tax periods for current and next year
        current_year = datetime.now().year
        choices = []
        
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        for year in [current_year, current_year + 1]:
            for month in months:
                period = f"{month}-{year}"
                choices.append((period, period))
        
        default_attrs = {}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs, choices=choices)