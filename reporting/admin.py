from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import ReportTemplate, GeneratedReport, ReportSchedule, DashboardWidget, AnalyticsData


@admin.register(ReportTemplate)
class ReportTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'report_type', 'is_active', 'is_public', 'created_at']
    list_filter = ['category', 'report_type', 'is_active', 'is_public']
    search_fields = ['name', 'description']
    



@admin.register(GeneratedReport)
class GeneratedReportAdmin(admin.ModelAdmin):
    list_display = ['report_name', 'report_template', 'report_status', 'generated_by', 'generated_at', 'download_report', 'print_report']
    list_filter = ['report_status', 'file_type', 'generated_at']
    search_fields = ['report_name', 'report_template__name']
    readonly_fields = ['generated_at', 'file_size']
    
    def download_report(self, obj):
        """Download button for report"""
        if obj.file_path:
            return f'<a href="{obj.file_path}" class="button" download>Download</a>'
        return 'No file'
    download_report.short_description = 'Download'
    download_report.allow_tags = True
    
    def print_report(self, obj):
        """Print button for report"""
        if obj.file_path:
            return f'<button onclick="window.print()" class="button">Print</button>'
        return 'No file'
    print_report.short_description = 'Print'
    print_report.allow_tags = True


@admin.register(ReportSchedule)
class ReportScheduleAdmin(admin.ModelAdmin):
    list_display = ['schedule_name', 'report_template', 'frequency', 'next_run', 'last_run', 'is_active']
    list_filter = ['frequency', 'is_active']
    search_fields = ['schedule_name', 'report_template__name']


@admin.register(DashboardWidget)
class DashboardWidgetAdmin(admin.ModelAdmin):
    list_display = ['name', 'widget_type', 'chart_type', 'position_x', 'position_y', 'is_active']
    list_filter = ['widget_type', 'chart_type', 'is_active']
    search_fields = ['name', 'data_source']


@admin.register(AnalyticsData)
class AnalyticsDataAdmin(admin.ModelAdmin):
    list_display = ['data_key', 'updated_at', 'expires_at']
    search_fields = ['data_key']
    readonly_fields = ['data_key', 'data_value', 'created_at', 'updated_at']


# Admin dashboard view for reporting module
def reporting_dashboard(request):
    """Reporting Module Dashboard"""
    context = {
        'title': 'Reporting Module',
        'subtitle': 'Centralized Reporting and Analytics Layer',
        'dashboard_url': '/reports/',
        'report_templates_url': reverse('admin:reporting_reporttemplate_changelist'),
        'generated_reports_url': reverse('admin:reporting_generatedreport_changelist'),
        'report_schedules_url': reverse('admin:reporting_reportschedule_changelist'),
        'dashboard_widgets_url': reverse('admin:reporting_dashboardwidget_changelist'),
    }
    return render(request, 'reporting/admin_dashboard.html', context)