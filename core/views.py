from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Sum
from taxpayers.models import TaxpayerMaster
from returns.models import GSTReturn
from compliance.models import ComplianceRiskReferral

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name()}!')
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

@login_required
def dashboard(request):
    # Get dashboard statistics
    total_taxpayers = TaxpayerMaster.objects.count()
    total_returns = GSTReturn.objects.count()
    high_risk_taxpayers = ComplianceRiskReferral.objects.filter(risk_level__in=['Critical', 'High']).count()
    open_audits = ComplianceRiskReferral.objects.filter(selection='Audit').count()
    
    # Get financial metrics using correct field names
    total_revenue = GSTReturn.objects.aggregate(total=Sum('declared_sales'))['total'] or 0
    
    # Get counts by status
    active_taxpayers = TaxpayerMaster.objects.filter(status='Active').count()
    filed_returns = GSTReturn.objects.filter(filing_status='Filed On Time').count()
    not_filed_returns = GSTReturn.objects.filter(filing_status='Overdue / Non-Filer').count()
    
    context = {
        'total_taxpayers': total_taxpayers,
        'active_taxpayers': active_taxpayers,
        'total_returns': total_returns,
        'filed_returns': filed_returns,
        'not_filed_returns': not_filed_returns,
        'high_risk_taxpayers': high_risk_taxpayers,
        'open_audits': open_audits,
        'total_revenue': total_revenue,
        'user': request.user,
    }
    
    return render(request, 'core/dashboard.html', context)