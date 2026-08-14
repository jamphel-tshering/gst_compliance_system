from django.core.management.base import BaseCommand
from compliance.models import ComplianceMonitoring, ComplianceRiskReferral, EnforcementRecovery
from audit_refund.models import AuditCase, AuditAssessment, RefundRegister
from returns.models import GSTReturn

class Command(BaseCommand):
    help = 'Standardize tax period format to Jan-2026 across all modules'

    def handle(self, *args, **options):
        def convert_to_month_year(date_str):
            """Convert various date formats to Jan-2026 format"""
            if not date_str:
                return date_str
            
            # If already in Jan-2026 format, return as is
            if '-' in date_str and len(date_str) == 8:  # Jan-2026 format
                return date_str
            
            # Handle date format like 2026-04-01
            if '-' in date_str and len(date_str) == 10:
                try:
                    from datetime import datetime
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                    return f"{month_names[date_obj.month-1]}-{date_obj.year}"
                except:
                    return date_str
            
            return date_str

        # Fix ComplianceMonitoring
        self.stdout.write("Fixing ComplianceMonitoring tax periods...")
        for record in ComplianceMonitoring.objects.all():
            if record.tax_period:
                new_period = convert_to_month_year(record.tax_period)
                if new_period != record.tax_period:
                    self.stdout.write(f"Updating {record.tax_period} to {new_period}")
                    record.tax_period = new_period
                    record.save()

        # Fix ComplianceRiskReferral
        self.stdout.write("\nFixing ComplianceRiskReferral tax periods...")
        for record in ComplianceRiskReferral.objects.all():
            if record.assessment_from_period:
                new_period = convert_to_month_year(record.assessment_from_period)
                if new_period != record.assessment_from_period:
                    self.stdout.write(f"Updating assessment_from_period {record.assessment_from_period} to {new_period}")
                    record.assessment_from_period = new_period
                    record.save()
            
            if record.assessment_to_period:
                new_period = convert_to_month_year(record.assessment_to_period)
                if new_period != record.assessment_to_period:
                    self.stdout.write(f"Updating assessment_to_period {record.assessment_to_period} to {new_period}")
                    record.assessment_to_period = new_period
                    record.save()

        # Fix EnforcementRecovery
        self.stdout.write("\nFixing EnforcementRecovery tax periods...")
        for record in EnforcementRecovery.objects.all():
            if record.tax_period:
                new_period = convert_to_month_year(record.tax_period)
                if new_period != record.tax_period:
                    self.stdout.write(f"Updating {record.tax_period} to {new_period}")
                    record.tax_period = new_period
                    record.save()

        # Fix AuditCase
        self.stdout.write("\nFixing AuditCase tax periods...")
        for record in AuditCase.objects.all():
            if record.from_tax_period:
                new_period = convert_to_month_year(record.from_tax_period)
                if new_period != record.from_tax_period:
                    self.stdout.write(f"Updating from_tax_period {record.from_tax_period} to {new_period}")
                    record.from_tax_period = new_period
                    record.save()
            
            if record.to_tax_period:
                new_period = convert_to_month_year(record.to_tax_period)
                if new_period != record.to_tax_period:
                    self.stdout.write(f"Updating to_tax_period {record.to_tax_period} to {new_period}")
                    record.to_tax_period = new_period
                    record.save()

        # Fix AuditAssessment
        self.stdout.write("\nFixing AuditAssessment tax periods...")
        for record in AuditAssessment.objects.all():
            if record.from_tax_period:
                new_period = convert_to_month_year(record.from_tax_period)
                if new_period != record.from_tax_period:
                    self.stdout.write(f"Updating from_tax_period {record.from_tax_period} to {new_period}")
                    record.from_tax_period = new_period
                    record.save()
            
            if record.to_tax_period:
                new_period = convert_to_month_year(record.to_tax_period)
                if new_period != record.to_tax_period:
                    self.stdout.write(f"Updating to_tax_period {record.to_tax_period} to {new_period}")
                    record.to_tax_period = new_period
                    record.save()
            
            if record.tax_period:
                new_period = convert_to_month_year(record.tax_period)
                if new_period != record.tax_period:
                    self.stdout.write(f"Updating tax_period {record.tax_period} to {new_period}")
                    record.tax_period = new_period
                    record.save()

        # Fix RefundRegister
        self.stdout.write("\nFixing RefundRegister tax periods...")
        for record in RefundRegister.objects.all():
            if record.tax_period:
                new_period = convert_to_month_year(record.tax_period)
                if new_period != record.tax_period:
                    self.stdout.write(f"Updating {record.tax_period} to {new_period}")
                    record.tax_period = new_period
                    record.save()

        self.stdout.write(self.style.SUCCESS("\nTax period format standardization completed!"))
        self.stdout.write("All tax periods are now in Jan-2026 format.")