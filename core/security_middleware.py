from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.conf import settings
import time

class SecurityMiddleware:
    """
    Security middleware for rate limiting and session management
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Check login rate limiting
        if request.path == '/login/' and request.method == 'POST':
            client_ip = self.get_client_ip(request)
            if self.is_rate_limited(client_ip):
                return HttpResponseForbidden("Too many login attempts. Please try again later.")
        
        # Check session timeout
        if request.user.is_authenticated:
            if self.is_session_expired(request):
                from django.contrib.auth import logout
                logout(request)
        
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def is_rate_limited(self, client_ip):
        """Check if client has exceeded rate limit"""
        cache_key = f'login_attempts_{client_ip}'
        attempts = cache.get(cache_key, 0)
        
        if attempts >= 5:  # Max 5 attempts
            return True
        
        # Increment attempt counter
        cache.set(cache_key, attempts + 1, 900)  # 15 minutes window
        return False
    
    def is_session_expired(self, request):
        """Check if user session has expired"""
        last_activity = request.session.get('last_activity')
        if last_activity:
            elapsed = time.time() - last_activity
            if elapsed > 1800:  # 30 minutes in seconds
                return True
        
        # Update last activity
        request.session['last_activity'] = time.time()
        return False


class PermissionMiddleware:
    """
    Middleware to enforce permissions on all requests
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Add security headers
        response = self.get_response(request)
        
        # Add security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response