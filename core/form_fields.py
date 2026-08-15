"""
Custom form fields for GST Compliance System
"""
from django import forms
from datetime import datetime


class CustomDateField(forms.DateField):
    """Custom date field that accepts DD-MM-YYYY format"""
    
    def __init__(self, *args, **kwargs):
        kwargs['input_formats'] = ['%d-%m-%Y', '%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d']
        super().__init__(*args, **kwargs)
    
    def to_python(self, value):
        """Convert DD-MM-YYYY string to date object"""
        if value in [None, '']:
            return None
        
        if isinstance(value, datetime):
            return value
        
        if isinstance(value, str):
            # Try DD-MM-YYYY format first
            for fmt in ['%d-%m-%Y', '%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d']:
                try:
                    return datetime.strptime(value, fmt).date()
                except ValueError:
                    continue
        
        return super().to_python(value)