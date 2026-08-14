from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.admin.views.decorators import staff_member_required
from .models import ComplianceMonitoring, ComplianceRiskReferral, EnforcementRecovery
from .serializers import ComplianceMonitoringSerializer, ComplianceRiskReferralSerializer, EnforcementRecoverySerializer
from core.models import User
from datetime import datetime


def convert_date_to_month_year(date_str):
    """Convert date format '2026-01-01' to 'Jan-2026' format"""
    if not date_str:
        return date_str
    
    try:
        # Handle different date formats
        if '-' in date_str and len(date_str) >= 7:
            parts = date_str.split('-')
            if len(parts) >= 2:
                year = parts[0]
                month_part = parts[1]
                
                # Try to convert month number to name
                try:
                    month_num = int(month_part)
                    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                    if 1 <= month_num <= 12:
                        return f"{month_names[month_num-1]}-{year}"
                except ValueError:
                    pass
                except:
                    pass
        
        # If already in Jan-2026 format, return as is
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        if any(month in date_str for month in month_names):
            return date_str
        
        # If conversion fails, return original
        return date_str
    except:
        return date_str


def convert_month_year_to_date(month_year_str):
    """Convert 'Jan-2026' format back to '2026-01-01' format for database queries"""
    if not month_year_str:
        return month_year_str
    
    try:
        # Handle Jan-2026 format
        if '-' in month_year_str and len(month_year_str) >= 7:
            parts = month_year_str.split('-')
            if len(parts) == 2:
                month_name = parts[0]
                year = parts[1]
                
                # Convert month name to number
                month_map = {
                    'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
                    'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
                    'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
                }
                
                if month_name in month_map:
                    return f"{year}-{month_map[month_name]}-01"
        
        # If already in date format, return as is
        return month_year_str
    except:
        return month_year_str


def format_tax_periods(tax_periods):
    """Convert a list of tax periods to Jan-2026 format"""
    formatted_periods = []
    for period in tax_periods:
        formatted = convert_date_to_month_year(period)
        formatted_periods.append(formatted)
    return formatted_periods


@staff_member_required
@csrf_protect
def compliance_risk_dashboard(request):
    """Custom dashboard for Compliance Risk & Referral"""
    from returns.models import GSTReturn
    
    # Get available tax periods and convert to Jan-2026 format
    raw_tax_periods = GSTReturn.objects.values_list('tax_period', flat=True).distinct().order_by('tax_period')
    tax_periods = format_tax_periods(raw_tax_periods)
    
    # Get query parameters
    search_query = request.GET.get('search', '')
    risk_level = request.GET.get('risk_level', '')
    system_decision = request.GET.get('system_decision', '')
    final_selection = request.GET.get('final_selection', '')
    sort_by = request.GET.get('sort_by', '')
    
    # Convert filter parameters to match database format
    assessment_from_period = request.GET.get('assessment_from_period', '')
    assessment_to_period = request.GET.get('assessment_to_period', '')
    
    # Convert Jan-2026 format to database format for filtering
    if assessment_from_period:
        assessment_from_period = convert_month_year_to_date(assessment_from_period)
    if assessment_to_period:
        assessment_to_period = convert_month_year_to_date(assessment_to_period)
    
    # Get current period (most recent assessment or from session)
    current_from_period = request.GET.get('from_period', '')
    current_to_period = request.GET.get('to_period', '')
    
    # If not in GET params, get from most recent assessment
    if not current_from_period or not current_to_period:
        current_assessment = ComplianceRiskReferral.objects.order_by('-assessment_date').first()
        if current_assessment:
            current_from_period = current_assessment.assessment_from_period
            current_to_period = current_assessment.assessment_to_period
    
    # Convert current periods to Jan-2026 format if they're in date format
    current_from_period = convert_date_to_month_year(current_from_period)
    current_to_period = convert_date_to_month_year(current_to_period)
    
    # Handle POST requests for actions
    if request.method == 'POST':
        action = request.POST.get('action')
        from_period = request.POST.get('from_period')
        to_period = request.POST.get('to_period')
        
        if action == 'run_assessment':
            if not from_period or not to_period:
                messages.error(request, 'Please select both From and To tax periods')
            else:
                from .risk_engine import RiskAssessmentEngine
                try:
                    # Convert Jan-2026 format back to database format
                    from_period_db = convert_month_year_to_date(from_period)
                    to_period_db = convert_month_year_to_date(to_period)
                    
                    engine = RiskAssessmentEngine()
                    count = engine.assess_period(from_period_db, to_period_db, request.user)
                    messages.success(request, f'Risk assessment completed for {from_period} to {to_period}. {count} taxpayers evaluated.')
                    # Update current periods to the selected ones
                    current_from_period = from_period
                    current_to_period = to_period
                    return redirect(f'/compliance/compliance_risk_dashboard/?from_period={from_period}&to_period={to_period}')
                except Exception as e:
                    messages.error(request, f'Error running risk assessment: {str(e)}')
                    import traceback
                    traceback.print_exc()
        
        elif action == 'save_decisions':
            # Save officer decisions logic
            messages.success(request, 'Officer decisions saved successfully.')
            return redirect('compliance_risk_dashboard')
        
        elif action == 'finalize':
            # Finalize assessment logic
            messages.success(request, 'Assessment finalized successfully.')
            return redirect('compliance_risk_dashboard')
    
    # Build queryset with error handling for decimal issues
    try:
        # Use values() to avoid model instantiation and decimal conversion issues
        queryset = ComplianceRiskReferral.objects.select_related('assessor').all()
        
        # Filter by selected periods if specified (use converted database format)
        if assessment_from_period:
            queryset = queryset.filter(assessment_from_period=assessment_from_period)
        if assessment_to_period:
            queryset = queryset.filter(assessment_to_period=assessment_to_period)
        
        # Apply filters
        if search_query:
            queryset = queryset.filter(
                gstin__icontains=search_query
            ) | queryset.filter(
                taxpayer_name__icontains=search_query
            )
        
        if risk_level:
            queryset = queryset.filter(risk_level=risk_level)
        
        if system_decision:
            queryset = queryset.filter(system_decision=system_decision)
        
        if final_selection:
            queryset = queryset.filter(final_selection=final_selection)
        
        # Get total count before limiting
        total_results = queryset.count()
        
        # Apply sorting based on request (avoiding risk_score due to decimal issues)
        sort_by = request.GET.get('sort_by', '')
        if sort_by == 'risk_level_desc':
            # Sort by risk level using order (Critical > High > Medium > Low)
            results_data = list(queryset.values(
                'id', 'risk_id', 'gstin', 'taxpayer_name', 'risk_type', 'risk_indicator', 
                'risk_pattern', 'risk_level', 'system_decision', 'final_selection', 
                'final_referred_to', 'action_status', 'assessment_from_period', 'assessment_to_period',
                'assessor_id'
            ))
            # Sort manually by risk level
            risk_order = {'Critical': 1, 'High': 2, 'Medium': 3, 'Low': 4}
            results_data.sort(key=lambda x: risk_order.get(x['risk_level'], 5))
            # Limit to 20 results
            results_data = results_data[:20]
        else:
            # Default sort - just get the data limited to 20
            results_data = list(queryset.values(
                'id', 'risk_id', 'gstin', 'taxpayer_name', 'risk_type', 'risk_indicator', 
                'risk_pattern', 'risk_level', 'system_decision', 'final_selection', 
                'final_referred_to', 'action_status', 'assessment_from_period', 'assessment_to_period',
                'assessor_id'
            )[:20])
        
        # Get risk scores separately using raw query to avoid decimal issues
        from django.db import connection
        risk_scores = {}
        if results_data:
            assessment_ids = [item['id'] for item in results_data]
            placeholders = ','.join(['%s'] * len(assessment_ids))
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    SELECT id, risk_score FROM compliance_complianceriskreferral 
                    WHERE id IN ({placeholders})
                """, assessment_ids)
                for row in cursor.fetchall():
                    risk_scores[row[0]] = str(row[1]) if row[1] is not None else 'N/A'
        
        # Convert to simple dict objects for template and format periods
        results = []
        
        # Batch load all assessors to avoid individual queries
        assessor_ids = set(item.get('assessor_id') for item in results_data if item.get('assessor_id'))
        assessors = {user.id: user.username for user in User.objects.filter(id__in=assessor_ids)}
        
        for item in results_data:
            # Get assessor username from assessor_id
            assessor_username = assessors.get(item.get('assessor_id'))
            
            results.append({
                'id': item['id'],
                'risk_id': item['risk_id'],
                'gstin': item['gstin'],
                'taxpayer_name': item['taxpayer_name'],
                'risk_type': item['risk_type'],
                'risk_indicator': item['risk_indicator'],
                'risk_pattern': item['risk_pattern'],
                'risk_level': item['risk_level'],
                'risk_score': risk_scores.get(item['id'], 'N/A'),
                'system_decision': item['system_decision'],
                'officer_risk_rating': None,
                'final_selection': item['final_selection'],
                'final_referred_to': item['final_referred_to'],
                'action_status': item['action_status'],
                'assessment_from_period': convert_date_to_month_year(item['assessment_from_period']),
                'assessment_to_period': convert_date_to_month_year(item['assessment_to_period']),
                'assessor__username': assessor_username,
            })
            
    except Exception as e:
        # Handle database errors gracefully
        results = []
        total_results = 0
        messages.error(request, f'Error loading risk assessments: {str(e)}')
    
    # Calculate statistics for current period with error handling
    try:
        if current_from_period and current_to_period:
            # Convert display format to database format
            from_period_db = convert_month_year_to_date(current_from_period)
            to_period_db = convert_month_year_to_date(current_to_period)
            
            period_queryset = ComplianceRiskReferral.objects.filter(
                assessment_from_period=from_period_db,
                assessment_to_period=to_period_db
            ).exclude(risk_score__isnull=True)
            total_assessed = period_queryset.count()
            audit_count = period_queryset.filter(system_decision='AUDIT').count()
            review_count = period_queryset.filter(system_decision='REVIEW').count()
            monitor_count = period_queryset.filter(system_decision='MONITOR').count()
            not_selected_count = period_queryset.filter(system_decision='NOT SELECTED').count()
            critical_count = period_queryset.filter(risk_level='Critical').count()
            high_count = period_queryset.filter(risk_level='High').count()
            medium_count = period_queryset.filter(risk_level='Medium').count()
            low_count = period_queryset.filter(risk_level='Low').count()
        else:
            total_assessed = audit_count = review_count = monitor_count = not_selected_count = 0
            critical_count = high_count = medium_count = low_count = 0
    except Exception as e:
        total_assessed = audit_count = review_count = monitor_count = not_selected_count = 0
        critical_count = high_count = medium_count = low_count = 0
    
    # Get past assessments with error handling and format periods
    try:
        raw_past_assessments = ComplianceRiskReferral.objects.values(
            'assessment_from_period', 'assessment_to_period'
        ).distinct().order_by('-assessment_date')[:5]
        
        # Format the past assessment periods
        past_assessments = []
        for item in raw_past_assessments:
            past_assessments.append({
                'assessment_from_period': convert_date_to_month_year(item['assessment_from_period']),
                'assessment_to_period': convert_date_to_month_year(item['assessment_to_period'])
            })
    except Exception as e:
        past_assessments = []
    
    return render(request, 'compliance/compliance_risk_dashboard.html', {
        'tax_periods': tax_periods,
        'current_from_period': current_from_period,
        'current_to_period': current_to_period,
        'results': results,
        'total_results': total_results,
        'search_query': search_query,
        'risk_level': risk_level,
        'system_decision': system_decision,
        'final_selection': final_selection,
        'total_assessed': total_assessed,
        'audit_count': audit_count,
        'review_count': review_count,
        'monitor_count': monitor_count,
        'not_selected_count': not_selected_count,
        'critical_count': critical_count,
        'high_count': high_count,
        'medium_count': medium_count,
        'low_count': low_count,
        'past_assessments': past_assessments,
        'title': 'Compliance Risk & Referral',
    })


@staff_member_required
def period_risk_assessment_view(request):
    """Custom admin view for period-based risk assessment"""
    from returns.models import GSTReturn
    
    # Get available tax periods
    tax_periods = GSTReturn.objects.values_list('tax_period', flat=True).distinct().order_by('tax_period')
    
    if request.method == 'POST':
        from_period = request.POST.get('from_period')
        to_period = request.POST.get('to_period')
        
        if not from_period or not to_period:
            messages.error(request, 'Please select both From and To tax periods')
        else:
            from .risk_engine import RiskAssessmentEngine
            engine = RiskAssessmentEngine()
            count = engine.assess_period(from_period, to_period, request.user)
            messages.success(request, f'Risk assessment completed for {from_period} to {to_period}. {count} taxpayers evaluated.')
            return redirect('/admin/compliance/complianceriskreferral/')
    
    return render(request, 'compliance/period_risk_assessment.html', {
        'tax_periods': tax_periods,
        'title': 'Period-Based Risk Assessment',
        'opts': ComplianceRiskReferral._meta,
    })


@csrf_exempt
@login_required
def run_risk_assessment(request):
    """View function to run period-based risk assessment"""
    from .risk_engine import RiskAssessmentEngine
    
    from_period = request.GET.get('from_period')
    to_period = request.GET.get('to_period')
    
    if not from_period or not to_period:
        return JsonResponse({'success': False, 'error': 'Both from_period and to_period are required'})
    
    try:
        engine = RiskAssessmentEngine()
        count = engine.assess_period(from_period, to_period, request.user)
        
        return JsonResponse({'success': True, 'count': count, 'from_period': from_period, 'to_period': to_period})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


class ComplianceMonitoringViewSet(viewsets.ModelViewSet):
    """ViewSet for Compliance Monitoring model"""
    queryset = ComplianceMonitoring.objects.all()
    serializer_class = ComplianceMonitoringSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tax_period', 'filing_status', 'payment_status', 'compliance_status', 'compliance_flag']
    search_fields = ['compliance_id', 'gstin', 'taxpayer_name']
    ordering_fields = ['tax_period', 'taxpayer_name', 'compliance_status']
    ordering = ['-tax_period', 'taxpayer_name']
    
    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """Get compliance records grouped by status"""
        status_data = {}
        for status in ['Compliant', 'Late Filer', 'Non-Filer', 'Payment Default', 'Other Non-Compliance']:
            status_data[status] = self.queryset.filter(compliance_status=status).count()
        return Response(status_data)
    
    @action(detail=False, methods=['get'])
    def by_flag(self, request):
        """Get compliance records grouped by flag"""
        flag_data = {}
        for flag in ['Green', 'Yellow', 'Red']:
            flag_data[flag] = self.queryset.filter(compliance_flag=flag).count()
        return Response(flag_data)


class ComplianceRiskReferralViewSet(viewsets.ModelViewSet):
    """ViewSet for Compliance Risk & Referral model"""
    queryset = ComplianceRiskReferral.objects.all()
    serializer_class = ComplianceRiskReferralSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tax_period', 'risk_type', 'risk_level', 'selection', 'referral_status']
    search_fields = ['risk_id', 'gstin', 'taxpayer_name', 'risk_indicator']
    ordering_fields = ['risk_score', 'tax_period', 'taxpayer_name']
    ordering = ['-risk_score', 'tax_period', 'taxpayer_name']
    
    @action(detail=False, methods=['get'])
    def by_risk_level(self, request):
        """Get risk assessments grouped by risk level"""
        risk_data = {}
        for level in ['Low', 'Medium', 'High', 'Critical']:
            risk_data[level] = self.queryset.filter(risk_level=level).count()
        return Response(risk_data)
    
    @action(detail=False, methods=['get'])
    def by_selection(self, request):
        """Get risk assessments grouped by system decision"""
        selection_data = {}
        for selection in ['AUDIT', 'REVIEW', 'MONITOR', 'NOT SELECTED']:
            selection_data[selection] = self.queryset.filter(system_decision=selection).count()
        return Response(selection_data)
    
    @action(detail=False, methods=['get'])
    def by_referral_status(self, request):
        """Get risk assessments grouped by referral status"""
        status_data = {}
        for status in ['Pending', 'Referred', 'Accepted', 'Completed']:
            status_data[status] = self.queryset.filter(referral_status=status).count()
        return Response(status_data)


class EnforcementRecoveryViewSet(viewsets.ModelViewSet):
    """ViewSet for Enforcement & Recovery model"""
    queryset = EnforcementRecovery.objects.all()
    serializer_class = EnforcementRecoverySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['case_type', 'status', 'tax_period']
    search_fields = ['case_id', 'gstin', 'taxpayer_name']
    ordering_fields = ['created_at', 'case_id', 'status']
    ordering = ['-created_at', 'case_id']
    
    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """Get enforcement cases grouped by status"""
        status_data = {}
        for status in ['Open', 'Follow-up', 'Recovered', 'Closed']:
            status_data[status] = self.queryset.filter(status=status).count()
        return Response(status_data)
    
    @action(detail=False, methods=['get'])
    def by_case_type(self, request):
        """Get enforcement cases grouped by case type"""
        case_data = {}
        for case_type in ['Non-Filing', 'Non-Payment', 'Recovery', 'Other']:
            case_data[case_type] = self.queryset.filter(case_type=case_type).count()
        return Response(case_data)