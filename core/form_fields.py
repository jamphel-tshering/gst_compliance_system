"""
Custom form fields for GST Compliance System
"""
from django import forms
from datetime import datetime


class CustomDateField(forms.DateField):
    """Custom date field that accepts DD-MM-YYYY format"""
    
    def __init__(self, *args, **kwargs):
        kwargs['input_formats'] = ['%d-%m-%Y']
        kwargs['error_messages'] = {
            'invalid': 'Enter a valid date in DD-MM-YYYY format (e.g., 15-08-2026)'
        }
        super().__init__(*args, **kwargs)
    
    def to_python(self, value):
        """Convert DD-MM-YYYY string to date object"""
        if value in [None, '']:
            return None
        
        if isinstance(value, datetime):
            return value.date()
        
        if isinstance(value, str):
            # Try DD-MM-YYYY format first
            try:
                return datetime.strptime(value, '%d-%m-%Y').date()
            except ValueError:
                # Try other formats as fallback
                for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d']:
                    try:
                        return datetime.strptime(value, fmt).date()
                    except ValueError:
                        continue
        
        return super().to_python(value)