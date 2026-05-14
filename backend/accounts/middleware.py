"""
Multi-user session middleware for local development.
Allows switching between student and admin sessions without logout.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

User = get_user_model()


class MultiSessionMiddleware:
    """
    Allows storing and retrieving multiple user sessions.
    Student can access /admin/ without logging out of student account.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Store current user context
        current_user_id = request.session.get('_current_user_id')
        admin_user_id = request.session.get('_admin_user_id')
        
        # If going to admin panel, switch to admin user
        if request.path.startswith('/admin/'):
            if admin_user_id and not current_user_id:
                try:
                    admin_user = User.objects.get(id=admin_user_id)
                    if admin_user.is_staff and admin_user.is_superuser:
                        # Switch context to admin
                        request.session['_current_user_id'] = request.user.id if request.user.is_authenticated else None
                        request.session['_admin_user_id'] = admin_user_id
                        # Manually set request.user to admin user
                        request.user = admin_user
                except User.DoesNotExist:
                    pass
        else:
            # If leaving admin panel, restore student session
            if current_user_id and admin_user_id:
                try:
                    student_user = User.objects.get(id=current_user_id)
                    request.user = student_user
                    # Clear admin context
                    request.session['_current_user_id'] = None
                except User.DoesNotExist:
                    request.user = AnonymousUser()
        
        response = self.get_response(request)
        return response
