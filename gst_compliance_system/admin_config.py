from django.contrib import admin

class GSTComplianceAdminSite(admin.AdminSite):
    site_header = 'GST Compliance System'
    site_title = 'GST Compliance'
    index_title = 'Dashboard'
    
    def get_app_list(self, request):
        """
        Override to ensure custom module ordering and exclude refunds app
        """
        app_dict = self._build_app_dict(request)
        
        # Exclude refunds app from admin panel (used for data models only)
        if 'refunds' in app_dict:
            del app_dict['refunds']
        
        # Custom ordering as requested
        custom_order = [
            'core',              # 1) Core
            'taxpayers',         # 2) Registration and Enquiry
            'returns',           # 3) Returns
            'compliance',        # 4) Compliance & Enforcement Module
            'audit_refund',      # 5) Audit & Refund Module
            'reporting',         # 6) Reporting
        ]
        
        # Sort app_dict according to custom order
        ordered_apps = []
        for app_name in custom_order:
            if app_name in app_dict:
                ordered_apps.append(app_dict[app_name])
        
        # Add any remaining apps not in custom order
        for app_name in app_dict:
            if app_name not in custom_order:
                ordered_apps.append(app_dict[app_name])
        
        return ordered_apps

# Create custom admin site instance
admin_site = GSTComplianceAdminSite(name='gst_admin')