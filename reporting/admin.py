from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, FileResponse
from django.utils import timezone
from datetime import datetime
import csv
import io
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
    actions = ['generate_sample_csv_report', 'generate_sample_excel_report']
    
    def download_report(self, obj):
        """Download button for report"""
        if obj.output_file:
            return f'<a href="{obj.output_file.url}" class="button" download>Download</a>'
        return 'No file'
    download_report.short_description = 'Download'
    download_report.allow_tags = True
    
    def print_report(self, obj):
        """Print button for report"""
        if obj.output_file:
            return f'<button onclick="window.open(\'{obj.output_file.url}\', \'_blank\'); window.print();" class="button">Print</button>'
        return 'No file'
    print_report.short_description = 'Print'
    print_report.allow_tags = True
    
    def generate_sample_csv_report(self, request, queryset):
        """Generate a sample CSV report"""
        from taxpayers.models import TaxpayerMaster
        
        # Create CSV content
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="taxpayer_report.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['GSTIN', 'Taxpayer Name', 'Business Name', 'Status', 'Dzongkhag', 'Organisation Type'])
        
        taxpayers = TaxpayerMaster.objects.filter(is_primary_license=True)[:100]
        for taxpayer in taxpayers:
            writer.writerow([
                taxpayer.gstin,
                taxpayer.taxpayer_name,
                taxpayer.business_name,
                taxpayer.status,
                taxpayer.dzongkhag,
                taxpayer.organisation_type
            ])
        
        return response
    
    generate_sample_csv_report.short_description = 'Generate Sample CSV Report'
    
    def generate_sample_excel_report(self, request, queryset):
        """Generate a sample Excel report"""
        from taxpayers.models import TaxpayerMaster
        from django.http import HttpResponse
        import openpyxl
        from openpyxl.styles import Font
        from django.core.files.base import ContentFile
        from django.utils.text import slugify
        
        # Create Excel workbook
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'Taxpayer Report'
        
        # Add headers
        headers = ['GSTIN', 'Taxpayer Name', 'Business Name', 'Status', 'Dzongkhag', 'Organisation Type']
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
        
        # Add data
        taxpayers = TaxpayerMaster.objects.filter(is_primary_license=True)[:100]
        for row, taxpayer in enumerate(taxpayers, 2):
            ws.cell(row=row, column=1, value=taxpayer.gstin)
            ws.cell(row=row, column=2, value=taxpayer.taxpayer_name)
            ws.cell(row=row, column=3, value=taxpayer.business_name)
            ws.cell(row=row, column=4, value=taxpayer.status)
            ws.cell(row=row, column=5, value=taxpayer.dzongkhag)
            ws.cell(row=row, column=6, value=taxpayer.organisation_type)
        
        # Save to BytesIO
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        
        # Create response
        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="taxpayer_report.xlsx"'
        
        return response
    
    generate_sample_excel_report.short_description = 'Generate Sample Excel Report'


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