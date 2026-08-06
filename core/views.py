from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from taxpayers.models import TaxpayerMaster
from returns.models import GSTReturn
from risk_assessment.models import ComplianceRiskRegister

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
    high_risk_taxpayers = ComplianceRiskRegister.objects.filter(risk_category__in=['critical', 'high']).count()
    
    context = {
        'total_taxpayers': total_taxpayers,
        'total_returns': total_returns,
        'high_risk_taxpayers': high_risk_taxpayers,
        'user': request.user,
    }
    
    return render(request, 'core/dashboard.html', context)