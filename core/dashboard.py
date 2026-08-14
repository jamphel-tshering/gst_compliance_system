from jet.dashboard import Dashboard
from jet.dashboard.dashboard_modules import DashboardModule
from django.utils.translation import gettext_lazy as _
from taxpayers.models import TaxpayerMaster
from returns.models import GSTReturn
from compliance.models import ComplianceRiskReferral, EnforcementRecovery
from django.db.models import Count


class CustomDashboard(Dashboard):
    columns = 3

    def init_with_context(self, context):
        self.available_children.append(self.model())
        self.children.append(self.model())


class KPIModule(DashboardModule):
    title = _('KPI Cards')
    template = 'core/dashboard_modules/kpi.html'
    layout = 'stack'
    
    def context(self):
        total_taxpayers = TaxpayerMaster.objects.filter(is_primary_license=True).count()
        active_taxpayers = TaxpayerMaster.objects.filter(status='Active', is_primary_license=True).count()
        
        try:
            pending_returns = GSTReturn.objects.filter(filing_status='Overdue / Non-Filer').count()
        except:
            pending_returns = 0
        
        high_risk_count = ComplianceRiskReferral.objects.filter(risk_level='High').count()
        
        return {
            'total_taxpayers': total_taxpayers,
            'active_taxpayers': active_taxpayers,
            'pending_returns': pending_returns,
            'high_risk_count': high_risk_count,
        }


class OrganisationTypeChartModule(DashboardModule):
    title = _('Taxpayers by Organisation Type')
    template = 'core/dashboard_modules/org_type_chart.html'
    layout = 'stack'
    
    def context(self):
        org_type_data = TaxpayerMaster.objects.filter(is_primary_license=True).values('organisation_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        return {
            'org_type_data': list(org_type_data)
        }


class DzongkhagChartModule(DashboardModule):
    title = _('Taxpayers by Dzongkhag')
    template = 'core/dashboard_modules/dzongkhag_chart.html'
    layout = 'stack'
    
    def context(self):
        dzongkhag_data = TaxpayerMaster.objects.filter(is_primary_license=True).values('dzongkhag').annotate(
            count=Count('id')
        ).order_by('-count')
        
        return {
            'dzongkhag_data': list(dzongkhag_data)
        }


class StatusChartModule(DashboardModule):
    title = _('Taxpayer Status Breakdown')
    template = 'core/dashboard_modules/status_chart.html'
    layout = 'stack'
    
    def context(self):
        status_data = TaxpayerMaster.objects.filter(is_primary_license=True).values('status').annotate(
            count=Count('id')
        ).order_by('-count')
        
        return {
            'status_data': list(status_data)
        }


class RiskSummaryModule(DashboardModule):
    title = _('Risk Assessment Summary')
    template = 'core/dashboard_modules/risk_summary.html'
    layout = 'stack'
    
    def context(self):
        high_risk_count = ComplianceRiskRegister.objects.filter(overall_risk_level='High').count()
        medium_risk_count = ComplianceRiskRegister.objects.filter(overall_risk_level='Medium').count()
        low_risk_count = ComplianceRiskRegister.objects.filter(overall_risk_level='Low').count()
        
        return {
            'high_risk': high_risk_count,
            'medium_risk': medium_risk_count,
            'low_risk': low_risk_count,
        }
