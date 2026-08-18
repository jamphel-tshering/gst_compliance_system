from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.db.models import Count, Sum, Avg
from taxpayers.models import TaxpayerMaster
from returns.models import GSTReturn
from compliance.models import ComplianceRiskReferral, EnforcementRecovery
from django.utils import timezone
from datetime import timedelta
import json
import os
from django.conf import settings
from django.core.management import call_command
from django.contrib import messages


@staff_member_required
def dashboard_view(request):
    """Custom dashboard with KPIs and charts"""
    
    # KPIs
    total_taxpayers = TaxpayerMaster.objects.filter(is_primary_license=True).count()
    active_taxpayers = TaxpayerMaster.objects.filter(status='Active', is_primary_license=True).count()
    deregistered_taxpayers = TaxpayerMaster.objects.filter(status='Deregistered', is_primary_license=True).count()
    
    # Returns statistics
    total_returns = GSTReturn.objects.count()
    try:
        filed_returns = GSTReturn.objects.filter(filing_status='Filed').count()
        pending_returns = GSTReturn.objects.filter(filing_status='Not Filed').count()
    except:
        filed_returns = GSTReturn.objects.count()
        pending_returns = 0
    
    # Risk statistics
    high_risk_count = ComplianceRiskReferral.objects.filter(overall_overall_risk_level='High').count()
    medium_risk_count = ComplianceRiskReferral.objects.filter(overall_overall_risk_level='Medium').count()
    low_risk_count = ComplianceRiskReferral.objects.filter(overall_overall_risk_level='Low').count()
    
    # Audit statistics
    total_audits = EnforcementRecovery.objects.count()
    try:
        completed_audits = EnforcementRecovery.objects.filter(status='Completed').count()
        pending_audits = EnforcementRecovery.objects.filter(status='Pending').count()
    except:
        completed_audits = 0
        pending_audits = total_audits
    
    # Organisation type breakdown
    org_type_data = TaxpayerMaster.objects.filter(is_primary_license=True).values('organisation_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    org_type_labels = [item['organisation_type'] for item in org_type_data]
    org_type_counts = [item['count'] for item in org_type_data]
    
    # Dzongkhag breakdown
    dzongkhag_data = TaxpayerMaster.objects.filter(is_primary_license=True).values('dzongkhag').annotate(
        count=Count('id')
    ).order_by('-count')
    
    dzongkhag_labels = [item['dzongkhag'] for item in dzongkhag_data]
    dzongkhag_counts = [item['count'] for item in dzongkhag_data]
    
    # Frequency breakdown
    frequency_data = TaxpayerMaster.objects.filter(is_primary_license=True).values('frequency').annotate(
        count=Count('id')
    ).order_by('-count')
    
    frequency_labels = [item['frequency'] for item in frequency_data]
    frequency_counts = [item['count'] for item in frequency_data]
    
    # Status breakdown
    status_data = TaxpayerMaster.objects.filter(is_primary_license=True).values('status').annotate(
        count=Count('id')
    ).order_by('-count')
    
    status_labels = [item['status'] for item in status_data]
    status_counts = [item['count'] for item in status_data]
    
    # Monthly filing trend (last 6 months) - simplified to avoid errors
    try:
        six_months_ago = timezone.now() - timedelta(days=180)
        monthly_data = GSTReturn.objects.filter(
            tax_period__gte=six_months_ago
        ).values('tax_period').annotate(
            count=Count('id')
        ).order_by('tax_period')
        
        monthly_labels = [str(item['tax_period']) for item in monthly_data]
        monthly_counts = [item['count'] for item in monthly_data]
    except:
        monthly_labels = []
        monthly_counts = []
    
    context = {
        'title': 'Dashboard',
        'kpi_cards': [
            {
                'title': 'Total Taxpayers',
                'value': total_taxpayers,
                'icon': 'fa fa-users',
                'color': 'primary',
                'trend': '+5%',
                'trend_up': True
            },
            {
                'title': 'Active Taxpayers',
                'value': active_taxpayers,
                'icon': 'fa fa-user-check',
                'color': 'success',
                'trend': '+3%',
                'trend_up': True
            },
            {
                'title': 'Pending Returns',
                'value': pending_returns,
                'icon': 'fa fa-clock',
                'color': 'warning',
                'trend': '-2%',
                'trend_up': False
            },
            {
                'title': 'High Risk Cases',
                'value': high_risk_count,
                'icon': 'fa fa-exclamation-triangle',
                'color': 'danger',
                'trend': '+8%',
                'trend_up': True
            },
        ],
        'charts': {
            'org_type_chart': {
                'type': 'bar',
                'data': {
                    'labels': org_type_labels,
                    'datasets': [{
                        'label': 'Taxpayers by Organisation Type',
                        'data': org_type_counts,
                        'backgroundColor': 'rgba(54, 162, 235, 0.8)',
                        'borderColor': 'rgba(54, 162, 235, 1)',
                        'borderWidth': 1
                    }]
                }
            },
            'dzongkhag_chart': {
                'type': 'pie',
                'data': {
                    'labels': dzongkhag_labels,
                    'datasets': [{
                        'data': dzongkhag_counts,
                        'backgroundColor': [
                            'rgba(255, 99, 132, 0.8)',
                            'rgba(54, 162, 235, 0.8)',
                            'rgba(255, 206, 86, 0.8)',
                            'rgba(75, 192, 192, 0.8)'
                        ]
                    }]
                }
            },
            'frequency_chart': {
                'type': 'doughnut',
                'data': {
                    'labels': frequency_labels,
                    'datasets': [{
                        'data': frequency_counts,
                        'backgroundColor': [
                            'rgba(153, 102, 255, 0.8)',
                            'rgba(255, 159, 64, 0.8)',
                            'rgba(255, 99, 132, 0.8)'
                        ]
                    }]
                }
            },
            'status_chart': {
                'type': 'bar',
                'data': {
                    'labels': status_labels,
                    'datasets': [{
                        'label': 'Taxpayers by Status',
                        'data': status_counts,
                        'backgroundColor': 'rgba(75, 192, 192, 0.8)',
                        'borderColor': 'rgba(75, 192, 192, 1)',
                        'borderWidth': 1
                    }]
                }
            },
            'monthly_trend_chart': {
                'type': 'line',
                'data': {
                    'labels': monthly_labels,
                    'datasets': [{
                        'label': 'Monthly Returns Filed',
                        'data': monthly_counts,
                        'fill': True,
                        'backgroundColor': 'rgba(54, 162, 235, 0.2)',
                        'borderColor': 'rgba(54, 162, 235, 1)',
                        'borderWidth': 2
                    }]
                }
            }
        },
        'risk_summary': {
            'high': high_risk_count,
            'medium': medium_risk_count,
            'low': low_risk_count
        },
        'audit_summary': {
            'total': total_audits,
            'completed': completed_audits,
            'pending': pending_audits
        }
    }
    
    return render(request, 'admin/dashboard.html', context)


@staff_member_required
def jazzmin_dashboard(request):
    """Custom Jazzmin dashboard with KPIs and charts"""
    
    # KPIs
    total_taxpayers = TaxpayerMaster.objects.filter(is_primary_license=True).count()
    active_taxpayers = TaxpayerMaster.objects.filter(status='Active', is_primary_license=True).count()
    
    # Returns statistics
    try:
        pending_returns = GSTReturn.objects.filter(filing_status='Not Filed').count()
    except:
        pending_returns = 0
    
    # Risk statistics
    high_risk_count = ComplianceRiskReferral.objects.filter(overall_overall_risk_level='High').count()
    medium_risk_count = ComplianceRiskReferral.objects.filter(overall_overall_risk_level='Medium').count()
    low_risk_count = ComplianceRiskReferral.objects.filter(overall_overall_risk_level='Low').count()
    
    # Audit statistics
    total_audits = EnforcementRecovery.objects.count()
    try:
        completed_audits = EnforcementRecovery.objects.filter(status='Completed').count()
        pending_audits = EnforcementRecovery.objects.filter(status='Pending').count()
    except:
        completed_audits = 0
        pending_audits = total_audits
    
    # Organisation type breakdown
    org_type_data = TaxpayerMaster.objects.filter(is_primary_license=True).values('organisation_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    org_type_labels = [item['organisation_type'] for item in org_type_data]
    org_type_counts = [item['count'] for item in org_type_data]
    
    # Dzongkhag breakdown
    dzongkhag_data = TaxpayerMaster.objects.filter(is_primary_license=True).values('dzongkhag').annotate(
        count=Count('id')
    ).order_by('-count')
    
    dzongkhag_labels = [item['dzongkhag'] for item in dzongkhag_data]
    dzongkhag_counts = [item['count'] for item in dzongkhag_data]
    
    # Frequency breakdown
    frequency_data = TaxpayerMaster.objects.filter(is_primary_license=True).values('frequency').annotate(
        count=Count('id')
    ).order_by('-count')
    
    frequency_labels = [item['frequency'] for item in frequency_data]
    frequency_counts = [item['count'] for item in frequency_data]
    
    # Status breakdown
    status_data = TaxpayerMaster.objects.filter(is_primary_license=True).values('status').annotate(
        count=Count('id')
    ).order_by('-count')
    
    status_labels = [item['status'] for item in status_data]
    status_counts = [item['count'] for item in status_data]
    
    # Monthly filing trend
    try:
        six_months_ago = timezone.now() - timedelta(days=180)
        monthly_data = GSTReturn.objects.filter(
            tax_period__gte=six_months_ago
        ).values('tax_period').annotate(
            count=Count('id')
        ).order_by('tax_period')
        
        monthly_labels = [str(item['tax_period']) for item in monthly_data]
        monthly_counts = [item['count'] for item in monthly_data]
    except:
        monthly_labels = []
        monthly_counts = []
    
    context = {
        'kpi_total_taxpayers': total_taxpayers,
        'kpi_active_taxpayers': active_taxpayers,
        'kpi_pending_returns': pending_returns,
        'kpi_high_risk': high_risk_count,
        'risk_high': high_risk_count,
        'risk_medium': medium_risk_count,
        'risk_low': low_risk_count,
        'audit_total': total_audits,
        'audit_completed': completed_audits,
        'audit_pending': pending_audits,
        'org_type_chart_data': {
            'labels': org_type_labels,
            'datasets': [{
                'label': 'Taxpayers',
                'data': org_type_counts,
                'backgroundColor': 'rgba(54, 162, 235, 0.8)',
                'borderColor': 'rgba(54, 162, 235, 1)',
                'borderWidth': 1
            }]
        },
        'dzongkhag_chart_data': {
            'labels': dzongkhag_labels,
            'datasets': [{
                'data': dzongkhag_counts,
                'backgroundColor': [
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(255, 206, 86, 0.8)',
                    'rgba(75, 192, 192, 0.8)'
                ]
            }]
        },
        'frequency_chart_data': {
            'labels': frequency_labels,
            'datasets': [{
                'data': frequency_counts,
                'backgroundColor': [
                    'rgba(153, 102, 255, 0.8)',
                    'rgba(255, 159, 64, 0.8)',
                    'rgba(255, 99, 132, 0.8)'
                ]
            }]
        },
        'status_chart_data': {
            'labels': status_labels,
            'datasets': [{
                'label': 'Taxpayers',
                'data': status_counts,
                'backgroundColor': 'rgba(75, 192, 192, 0.8)',
                'borderColor': 'rgba(75, 192, 192, 1)',
                'borderWidth': 1
            }]
        },
        'monthly_trend_data': {
            'labels': monthly_labels,
            'datasets': [{
                'label': 'Returns Filed',
                'data': monthly_counts,
                'fill': True,
                'backgroundColor': 'rgba(54, 162, 235, 0.2)',
                'borderColor': 'rgba(54, 162, 235, 1)',
                'borderWidth': 2
            }]
        }
    }
    
    return render(request, 'jazzmin/index.html', context)


@staff_member_required
def backup_database(request):
    """Create a backup of the SQLite database"""
    if request.method == 'POST':
        try:
            call_command('backup_db')
            messages.success(request, 'Database backup created successfully!')
        except Exception as e:
            messages.error(request, f'Backup failed: {str(e)}')
        return redirect('admin:index')
    
    # List existing backups
    backup_dir = os.path.join(settings.BASE_DIR, 'backups')
    backups = []
    if os.path.exists(backup_dir):
        backups = sorted([f for f in os.listdir(backup_dir) if f.startswith('gst_compliance_backup_')], reverse=True)
    
    context = {
        'backups': backups,
        'backup_count': len(backups)
    }
    return render(request, 'admin/backup_database.html', context)


@staff_member_required
def restore_database(request):
    """Restore database from a backup"""
    if request.method == 'POST':
        backup_file = request.POST.get('backup_file')
        if backup_file:
            try:
                call_command('restore_db', backup_file)
                messages.success(request, f'Database restored from {backup_file} successfully!')
                return redirect('admin:index')
            except Exception as e:
                messages.error(request, f'Restore failed: {str(e)}')
        else:
            messages.error(request, 'Please select a backup file to restore')
    
    # List existing backups
    backup_dir = os.path.join(settings.BASE_DIR, 'backups')
    backups = []
    if os.path.exists(backup_dir):
        backups = sorted([f for f in os.listdir(backup_dir) if f.startswith('gst_compliance_backup_')], reverse=True)
    
    context = {
        'backups': backups,
        'backup_count': len(backups)
    }
    return render(request, 'admin/restore_database.html', context)
