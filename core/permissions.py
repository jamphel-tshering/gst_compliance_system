from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.contrib.auth import get_user_model

User = get_user_model()


def permission_required(perm):
    """
    Decorator to check specific granular permission
    Usage: @permission_required('can_view_taxpayers')
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if not hasattr(request.user, perm):
                raise PermissionDenied("You don't have permission to access this resource.")
            
            if not getattr(request.user, perm):
                raise PermissionDenied("You don't have permission to access this resource.")
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def role_required(*roles):
    """
    Decorator to check if user has required role
    Usage: @role_required('administrator', 'section_head')
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role not in roles:
                raise PermissionDenied("You don't have the required role to access this resource.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def api_permission_required(perm):
    """
    Decorator for API endpoints to check permissions
    Returns JSON response for API calls
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return JsonResponse({'error': 'Authentication required'}, status=401)
            
            if not hasattr(request.user, perm):
                return JsonResponse({'error': 'Permission denied'}, status=403)
            
            if not getattr(request.user, perm):
                return JsonResponse({'error': 'Permission denied'}, status=403)
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def module_access_required(module):
    """
    Decorator to check if user has any access to a module
    Usage: @module_access_required('taxpayers')
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.has_module_access(module):
                raise PermissionDenied("You don't have access to this module.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def audit_log_action(action, model_name=None, object_id=None, description=""):
    """
    Decorator to automatically log user actions
    Usage: @audit_log_action('view', 'TaxpayerMaster')
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Execute the view
            response = view_func(request, *args, **kwargs)
            
            # Log the action
            from core.models import AuditLog
            from django.contrib.auth import get_user_model
            
            User = get_user_model()
            
            # Get client IP
            client_ip = request.META.get('REMOTE_ADDR')
            
            # Create audit log
            AuditLog.objects.create(
                user=request.user if request.user.is_authenticated else None,
                action=action,
                model_name=model_name or view_func.__name__,
                object_id=object_id,
                description=description or f"Accessed {view_func.__name__}",
                ip_address=client_ip
            )
            
            return response
        return _wrapped_view
    return decorator


class AuditMixin:
    """
    Mixin for Django admin classes to automatically log changes
    """
    
    def log_audit_action(self, action, obj, description=""):
        """
        Log an audit action for an object
        """
        from core.models import AuditLog
        
        AuditLog.objects.create(
            user=self.request.user if hasattr(self, 'request') and self.request.user.is_authenticated else None,
            action=action,
            model_name=obj.__class__.__name__,
            object_id=obj.id,
            description=description or f"{action} {obj.__class__.__name__}",
            ip_address=self.request.META.get('REMOTE_ADDR') if hasattr(self, 'request') else None
        )
    
    def save_model(self, request, obj, form, change):
        """
        Override save_model to log changes
        """
        action = 'update' if change else 'create'
        description = f"{action} {obj.__class__.__name__}: {obj}"
        
        super().save_model(request, obj, form, change)
        
        # Log the action
        self.log_audit_action(action, obj, description)
    
    def delete_model(self, request, obj):
        """
        Override delete_model to log deletions
        """
        description = f"delete {obj.__class__.__name__}: {obj}"
        
        super().delete_model(request, obj)
        
        # Log the action
        self.log_audit_action('delete', obj, description)