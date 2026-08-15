"""
Helper functions for GST Compliance System
"""
from taxpayers.models import TaxpayerMaster
from datetime import datetime, timedelta


def get_taxpayer_by_gstin(gstin):
    """
    Fetch taxpayer information by GSTIN from primary taxpayer database
    Returns taxpayer object or None if not found
    """
    try:
        taxpayer = TaxpayerMaster.objects.filter(
            gstin=gstin,
            is_primary_license=True
        ).first()
        return taxpayer
    except:
        return None


def calculate_tax_period_due_date(tax_period):
    """
    Calculate due date for a given tax period (format: Jan-2026)
    Due date is typically 20th of the following month
    """
    try:
        # Parse Jan-2026 format
        month_abbr, year = tax_period.split('-')
        month_map = {
            'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
            'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
        }
        month = month_map.get(month_abbr, 1)
        year = int(year)
        
        # Due date is 20th of the following month
        if month == 12:
            due_date = datetime(year + 1, 1, 20)
        else:
            due_date = datetime(year, month + 1, 20)
        
        return due_date
    except:
        return None


def calculate_filing_delay(return_filing_date, return_due_date):
    """
    Calculate filing delay in days
    Returns positive number if late, 0 if on time
    """
    try:
        if return_filing_date and return_due_date:
            delay = (return_filing_date - return_due_date).days
            return max(0, delay)  # Only count late days
        return 0
    except:
        return 0


def calculate_gst_calculations(declared_sales, declared_import_value, declared_domestic_purchase):
    """
    Calculate GST values based on 5% rate
    Returns dict with all calculated values
    """
    try:
        # Convert to float if needed
        declared_sales = float(declared_sales or 0)
        declared_import_value = float(declared_import_value or 0)
        declared_domestic_purchase = float(declared_domestic_purchase or 0)
        
        # Calculate with 5% GST rate
        declared_import_gst = declared_import_value * 0.05
        domestic_purchase_itc_claimed = declared_domestic_purchase * 0.05
        declared_output_gst = declared_sales * 0.05
        total_itc_claimed = declared_import_gst + domestic_purchase_itc_claimed
        
        # Calculate GST payable/refundable
        gst_payable_refundable = declared_output_gst - total_itc_claimed
        
        return {
            'declared_import_gst': round(declared_import_gst, 2),
            'domestic_purchase_itc_claimed': round(domestic_purchase_itc_claimed, 2),
            'declared_output_gst': round(declared_output_gst, 2),
            'total_itc_claimed': round(total_itc_claimed, 2),
            'gst_payable_refundable': round(gst_payable_refundable, 2)
        }
    except:
        return {
            'declared_import_gst': 0,
            'domestic_purchase_itc_claimed': 0,
            'declared_output_gst': 0,
            'total_itc_claimed': 0,
            'gst_payable_refundable': 0
        }


def format_date_display(date_value):
    """
    Format date for display in dd-mm-yyyy format
    """
    if date_value:
        if isinstance(date_value, str):
            # Try to parse and reformat
            for fmt in ['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y']:
                try:
                    parsed_date = datetime.strptime(date_value, fmt)
                    return parsed_date.strftime('%d-%m-%Y')
                except ValueError:
                    continue
            return date_value
        else:
            return date_value.strftime('%d-%m-%Y')
    return '-'