from jet.dashboard import DashboardApp
from jet.dashboard.dashboard_modules import RecentActions
from django.utils.translation import gettext_lazy as _


class CustomDashboardApp(DashboardApp):
    title = _('GST Compliance Dashboard')
    layout = 'stack'
    children = [
        RecentActions(),
    ]
    
    def init_with_context(self, context):
        from .dashboard import KPIModule, OrganisationTypeChartModule, DzongkhagChartModule, StatusChartModule, RiskSummaryModule
        
        self.available_children.append(KPIModule())
        self.available_children.append(OrganisationTypeChartModule())
        self.available_children.append(DzongkhagChartModule())
        self.available_children.append(StatusChartModule())
        self.available_children.append(RiskSummaryModule())
        
        self.children.append(KPIModule())
        self.children.append(OrganisationTypeChartModule())
        self.children.append(DzongkhagChartModule())
        self.children.append(StatusChartModule())
        self.children.append(RiskSummaryModule())
