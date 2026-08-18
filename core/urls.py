from django.urls import path
from . import views
from .admin_views import dashboard_view, jazzmin_dashboard, backup_database, restore_database

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/', dashboard_view, name='admin_dashboard'),
    path('jazzmin-dashboard/', jazzmin_dashboard, name='jazzmin_dashboard'),
    path('backup-database/', backup_database, name='backup_database'),
    path('restore-database/', restore_database, name='restore_database'),
]