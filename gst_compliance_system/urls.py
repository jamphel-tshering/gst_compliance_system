"""
URL configuration for gst_compliance_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from compliance.admin import compliance_enforcement_dashboard
from audit_refund.admin import audit_refund_dashboard
from core.admin import main_dashboard
from reporting.admin import reporting_dashboard

# Use default admin site with custom app ordering
# Override get_app_list to hide refunds app and order modules correctly
class CustomAdminSite(admin.AdminSite):
    def get_app_list(self, request, app_label=None):
        app_dict = self._build_app_dict(request)
        
        # Hide refunds app from admin panel (RefundRegister now in audit_refund)
        if 'refunds' in app_dict:
            del app_dict['refunds']
        
        # Add Main Dashboard as first item
        main_dashboard_app = {
            'name': 'Main Dashboard',
            'app_label': 'main_dashboard',
            'models': [
                {
                    'name': 'Dashboard',
                    'object_name': 'Dashboard',
                    'admin_url': '/admin/dashboard/',
                    'view_only': True,
                }
            ],
            'has_module_perms': True,
        }
        
        # Custom ordering
        custom_order = [
            'main_dashboard',   # 0) Main Dashboard
            'core',              # 1) Core
            'taxpayers',         # 2) Registration and Enquiry
            'returns',           # 3) Returns
            'compliance',        # 4) Compliance & Enforcement
            'audit_refund',      # 5) Audit & Refund
            'reporting',         # 6) Reporting
        ]
        
        ordered_apps = []
        for app_name in custom_order:
            if app_name == 'main_dashboard':
                ordered_apps.append(main_dashboard_app)
            elif app_name in app_dict:
                ordered_apps.append(app_dict[app_name])
        
        # Add any remaining apps
        for app_name in app_dict:
            if app_name not in custom_order:
                ordered_apps.append(app_dict[app_name])
        
        return ordered_apps

# Override default admin site
admin.site.__class__ = CustomAdminSite

# Customize admin site title and header
admin.site.site_title = "RRCO/GST Mongar Administration"
admin.site.site_header = "RRCO/GST Mongar Administration"
admin.site.index_title = "Welcome to RRCO/GST Mongar Administration"

urlpatterns = [
    path('admin/dashboard/', main_dashboard, name='main_dashboard'),  # Main Dashboard - BEFORE admin routes
    path('admin/', admin.site.urls),
    path('admin/compliance/', compliance_enforcement_dashboard),  # Compliance & Enforcement dashboard
    path('admin/audit_refund/', audit_refund_dashboard),  # Audit & Refund dashboard
    path('admin/reporting/', reporting_dashboard),  # Reporting dashboard
    path('api/taxpayers/', include('taxpayers.urls')),
    path('api/returns/', include('returns.urls')),
    path('api/compliance/', include('compliance.urls')),
    path('', lambda request: redirect('login/')),
    path('', include('core.urls')),
    path('taxpayers/', include('taxpayers.urls')),
    path('returns/', include('returns.urls')),
    path('compliance/', include('compliance.urls')),
    path('audit_refund/', include('audit_refund.urls')),
    path('reports/', include('reporting.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
