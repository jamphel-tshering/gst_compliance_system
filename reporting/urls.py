from django.urls import path
from . import views

app_name = 'reporting'

urlpatterns = [
    # Report Landing Page
    path('', views.report_landing, name='report_landing'),
    
    # Report Views (Dynamic routing)
    path('report/<str:report_id>/', views.report_view, name='report_view'),
    
    # Export Routes (to be implemented)
    path('export/<str:report_id>/excel/', views.export_excel, name='export_excel'),
    path('export/<str:report_id>/pdf/', views.export_pdf, name='export_pdf'),
    path('export/<str:report_id>/csv/', views.export_csv, name='export_csv'),
]