import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gst_compliance_system.settings')
django.setup()

from risk_assessment.models import ComplianceRiskRegister

print(f'Total records: {ComplianceRiskRegister.objects.count()}')
periods = ComplianceRiskRegister.objects.values('assessment_period').order_by('assessment_period').distinct()
print('\nRecords by period:')
for p in periods:
    count = ComplianceRiskRegister.objects.filter(assessment_period=p['assessment_period']).count()
    print(f"  {p['assessment_period']}: {count}")
