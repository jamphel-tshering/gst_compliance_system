from django.contrib import admin
from .models import ReportTemplate, GeneratedReport, ReportSchedule, DashboardWidget, AnalyticsData

@admin.register(ReportTemplate)
class ReportTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'report_type', 'is_active', 'is_public', 'created_at']
    list_filter = ['report_type', 'is_active', 'is_public']
    search_fields = ['name', 'description']


@admin.register(GeneratedReport)
class GeneratedReportAdmin(admin.ModelAdmin):
    list_display = ['report_name', 'report_template', 'report_status', 'generated_by', 'generated_at']
    list_filter = ['report_status', 'file_type', 'generated_at']
    search_fields = ['report_name', 'report_template__name']
    readonly_fields = ['generated_at', 'file_size']


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