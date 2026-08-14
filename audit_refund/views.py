from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Q, Sum
from .models import AuditCase, RefundRegister
from compliance.models import ComplianceRiskReferral
from returns.models import GSTReturn
from core.models import User


@login_required
@staff_member_required
def audit_dashboard(request):
    """Audit Dashboard with summary cards and filtering"""
    
    # Summary statistics
    total_cases = AuditCase.objects.count()
    pending_assignment = AuditCase.objects.filter(status='pending_assignment').count()
    assigned = AuditCase.objects.filter(status='assigned').count()
    in_progress = AuditCase.objects.filter(status='in_progress').count()
    completed = AuditCase.objects.filter(status='completed').count()
    closed = AuditCase.objects.filter(status='closed').count()
    
    # Get filter parameters
    from_period = request.GET.get('from_period', '')
    to_period = request.GET.get('to_period', '')
    risk_level = request.GET.get('risk_level', '')
    audit_officer = request.GET.get('audit_officer', '')
    status = request.GET.get('status', '')
    dzongkhag = request.GET.get('dzongkhag', '')
    
    # Build queryset
    queryset = AuditCase.objects.select_related('risk_referral', 'assigned_officer').all()
    
    # Apply filters
    if from_period:
        queryset = queryset.filter(from_tax_period__gte=from_period)
    if to_period:
        queryset = queryset.filter(to_tax_period__lte=to_period)
    if risk_level:
        queryset = queryset.filter(risk_referral__risk_level=risk_level)
    if audit_officer:
        queryset = queryset.filter(assigned_officer__username=audit_officer)
    if status:
        queryset = queryset.filter(status=status)
    if dzongkhag:
        queryset = queryset.filter(dzongkhag__icontains=dzongkhag)
    
    # Get recent cases
    recent_cases = queryset.order_by('-created_at')[:20]
    
    # Get available periods, officers, dzongkhags for filters
    available_periods = AuditCase.objects.values_list('from_tax_period', flat=True).distinct().order_by('from_tax_period')
    available_officers = User.objects.filter(assigned_audit_cases__isnull=False).distinct()
    available_dzongkhags = AuditCase.objects.values_list('dzongkhag', flat=True).distinct().exclude(dzongkhag='').order_by('dzongkhag')
    
    context = {
        'total_cases': total_cases,
        'pending_assignment': pending_assignment,
        'assigned': assigned,
        'in_progress': in_progress,
        'completed': completed,
        'closed': closed,
        'recent_cases': recent_cases,
        'available_periods': available_periods,
        'available_officers': available_officers,
        'available_dzongkhags': available_dzongkhags,
        'filters': {
            'from_period': from_period,
            'to_period': to_period,
            'risk_level': risk_level,
            'audit_officer': audit_officer,
            'status': status,
            'dzongkhag': dzongkhag,
        }
    }
    
    return render(request, 'audit_refund/audit_dashboard.html', context)


@login_required
@staff_member_required
def refund_dashboard(request):
    """Refund Dashboard with summary cards and filtering"""
    
    # Summary statistics
    total_applications = RefundRegister.objects.count()
    pending = RefundRegister.objects.filter(status='submitted').count()
    under_review = RefundRegister.objects.filter(status='under_review').count()
    verification = RefundRegister.objects.filter(status='processing').count()
    approved = RefundRegister.objects.filter(status='approved').count()
    rejected = RefundRegister.objects.filter(status='rejected').count()
    completed = RefundRegister.objects.filter(status__in=['paid', 'closed']).count()
    
    # Financial summaries
    total_claimed = RefundRegister.objects.aggregate(Sum('claimed_amount'))['claimed_amount__sum'] or 0
    total_approved = RefundRegister.objects.aggregate(Sum('refund_approved'))['refund_approved__sum'] or 0
    total_adjusted = RefundRegister.objects.aggregate(Sum('adjustment'))['adjustment__sum'] or 0
    
    # Get filter parameters
    tax_period = request.GET.get('tax_period', '')
    status = request.GET.get('status', '')
    
    # Build queryset
    queryset = RefundRegister.objects.all()
    
    # Apply filters
    if tax_period:
        queryset = queryset.filter(tax_period=tax_period)
    if status:
        queryset = queryset.filter(status=status)
    
    # Get recent refunds (with filters applied)
    recent_refunds = queryset.order_by('-created_at')[:20]
    
    # Get available periods for filters
    available_periods = RefundRegister.objects.values_list('tax_period', flat=True).distinct().order_by('tax_period')
    
    context = {
        'total_applications': total_applications,
        'pending': pending,
        'under_review': under_review,
        'verification': verification,
        'approved': approved,
        'rejected': rejected,
        'completed': completed,
        'total_claimed': total_claimed,
        'total_approved': total_approved,
        'total_adjusted': total_adjusted,
        'recent_refunds': recent_refunds,
        'available_periods': available_periods,
        'filters': {
            'tax_period': tax_period,
            'status': status,
        }
    }
    
    return render(request, 'audit_refund/refund_dashboard.html', context)


@login_required
@staff_member_required
def auto_create_audit_cases(request):
    """Automatically create audit cases from Compliance Risk where Final = AUDIT"""
    from django.utils import timezone
    from django.contrib import messages
    
    # Get all risk referrals with Final = AUDIT that don't have audit cases yet
    audit_risks = ComplianceRiskReferral.objects.filter(final_selection='AUDIT')
    
    created_count = 0
    for risk in audit_risks:
        # Check if audit case already exists
        if not AuditCase.objects.filter(risk_referral=risk).exists():
            # Create audit case
            audit_case = AuditCase.objects.create(
                risk_referral=risk,
                assessment_date=risk.assessment_date,
                from_tax_period=risk.assessment_from_period,
                to_tax_period=risk.assessment_to_period,
                gstin=risk.gstin,
                taxpayer_name=risk.taxpayer_name,
                assessment_type='field_audit',  # Default to field audit
                audit_priority='high' if risk.risk_level in ['Critical', 'High'] else 'medium',
                status='referred',
                assessor=risk.assessor,
            )
            created_count += 1
    
    messages.success(request, f'Created {created_count} audit cases from Compliance Risk referrals.')
    return render(request, 'audit_refund/audit_dashboard.html')


@login_required
@staff_member_required
def audit_case_detail(request, audit_case_id):
    """View detailed audit case information"""
    from django.shortcuts import get_object_or_404
    
    audit_case = get_object_or_404(AuditCase, id=audit_case_id)
    
    context = {
        'audit_case': audit_case,
    }
    
    return render(request, 'audit_refund/audit_case_detail.html', context)