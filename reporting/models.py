from django.db import models
from core.models import User

class ReportTemplate(models.Model):
    """
    Report Templates for Standard and Custom Reports
    """
    REPORT_TYPES = (
        ('compliance', 'Compliance Report'),
        ('risk_assessment', 'Risk Assessment Report'),
        ('audit_selection', 'Audit Selection Report'),
        ('refund_analysis', 'Refund Analysis Report'),
        ('taxpayer_summary', 'Taxpayer Summary Report'),
        ('custom', 'Custom Report'),
    )
    
    name = models.CharField(max_length=200, verbose_name='Report Name')
    report_type = models.CharField(max_length=30, choices=REPORT_TYPES)
    description = models.TextField(blank=True)
    
    # Report Configuration
    template_file = models.FileField(upload_to='report_templates/', blank=True)
    parameters = models.JSONField(default=dict, blank=True)
    
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=False)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Report Template'
        verbose_name_plural = 'Report Templates'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class GeneratedReport(models.Model):
    """
    Generated Report Instances
    """
    REPORT_STATUS = (
        ('generating', 'Generating'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    
    report_template = models.ForeignKey(ReportTemplate, on_delete=models.CASCADE, related_name='generated_reports')
    
    report_name = models.CharField(max_length=200)
    report_status = models.CharField(max_length=20, choices=REPORT_STATUS, default='generating')
    
    # Report Parameters
    parameters = models.JSONField(default=dict, blank=True)
    
    # Output
    output_file = models.FileField(upload_to='generated_reports/', blank=True)
    file_type = models.CharField(max_length=10, choices=[('pdf', 'PDF'), ('excel', 'Excel'), ('csv', 'CSV')], default='pdf')
    
    # Metadata
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    file_size = models.BigIntegerField(null=True, blank=True)
    
    error_message = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Generated Report'
        verbose_name_plural = 'Generated Reports'
        ordering = ['-generated_at']
    
    def __str__(self):
        return f"{self.report_name} - {self.generated_at.strftime('%Y-%m-%d %H:%M')}"


class ReportSchedule(models.Model):
    """
    Scheduled Reports
    """
    FREQUENCY_CHOICES = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
    )
    
    report_template = models.ForeignKey(ReportTemplate, on_delete=models.CASCADE, related_name='schedules')
    
    schedule_name = models.CharField(max_length=200)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    
    # Schedule Configuration
    parameters = models.JSONField(default=dict, blank=True)
    recipients = models.JSONField(default=list, blank=True)  # List of email addresses
    
    # Timing
    next_run = models.DateTimeField()
    last_run = models.DateTimeField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Report Schedule'
        verbose_name_plural = 'Report Schedules'
        ordering = ['next_run']
    
    def __str__(self):
        return f"{self.schedule_name} - {self.get_frequency_display()}"


class DashboardWidget(models.Model):
    """
    Dashboard Widget Configuration
    """
    WIDGET_TYPES = (
        ('metric', 'Metric Card'),
        ('chart', 'Chart'),
        ('table', 'Table'),
        ('alert', 'Alert'),
        ('list', 'List'),
    )
    
    CHART_TYPES = (
        ('bar', 'Bar Chart'),
        ('line', 'Line Chart'),
        ('pie', 'Pie Chart'),
        ('scatter', 'Scatter Plot'),
        ('heatmap', 'Heatmap'),
    )
    
    name = models.CharField(max_length=200)
    widget_type = models.CharField(max_length=20, choices=WIDGET_TYPES)
    chart_type = models.CharField(max_length=20, choices=CHART_TYPES, blank=True)
    
    # Widget Configuration
    data_source = models.CharField(max_length=100, verbose_name='Data Source Model')
    query_config = models.JSONField(default=dict, blank=True)
    
    # Display Configuration
    position_x = models.IntegerField(default=0)
    position_y = models.IntegerField(default=0)
    width = models.IntegerField(default=4)
    height = models.IntegerField(default=3)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Dashboard Widget'
        verbose_name_plural = 'Dashboard Widgets'
        ordering = ['position_y', 'position_x']
    
    def __str__(self):
        return self.name


class AnalyticsData(models.Model):
    """
    Cached Analytics Data for Performance
    """
    data_key = models.CharField(max_length=100, unique=True)
    data_value = models.JSONField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Analytics Data'
        verbose_name_plural = 'Analytics Data'
        indexes = [
            models.Index(fields=['data_key']),
            models.Index(fields=['expires_at']),
        ]
    
    def __str__(self):
        return self.data_key
    
    def is_expired(self):
        from django.utils import timezone
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False