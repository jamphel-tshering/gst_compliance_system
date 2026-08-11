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

# Use default admin site to avoid circular import issues
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/taxpayers/', include('taxpayers.urls')),
    path('api/returns/', include('returns.urls')),
    path('api/risk-assessment/', include('risk_assessment.urls')),
    path('', lambda request: redirect('login/')),
    path('', include('core.urls')),
    path('taxpayers/', include('taxpayers.urls')),
    path('returns/', include('returns.urls')),
    path('refunds/', include('refunds.urls')),
    path('risk/', include('risk_assessment.urls')),
    path('reports/', include('reporting.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
