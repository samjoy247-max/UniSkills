"""
UN-97: Minimum Security Baseline
Password validation, role-based access control, permission checks
"""

from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required, user_passes_test
from functools import wraps


class PasswordValidator:
    """UN-97: Enforce minimum password requirements"""
    
    @staticmethod
    def validate_password_strength(password):
        """Validate password meets security requirements"""
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in password):
            raise ValidationError("Password must contain at least one digit")
        if not any(char.isupper() for char in password):
            raise ValidationError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in password):
            raise ValidationError("Password must contain at least one lowercase letter")
        return True


class RoleBasedAccessControl:
    """UN-97: Role-based access control"""
    
    ROLES = {
        'student': ['view_skills', 'create_booking', 'submit_rating'],
        'provider': ['create_skill', 'view_bookings', 'view_ratings', 'view_sessions'],
        'alumni': ['create_post', 'edit_post', 'delete_post'],
        'admin': ['moderate_posts', 'moderate_skills', 'view_analytics', 'manage_users'],
    }
    
    @staticmethod
    def check_permission(user, permission):
        """Check if user has permission based on role"""
        if not user.is_authenticated:
            return False
        
        user_role = user.role.lower()
        allowed_permissions = RoleBasedAccessControl.ROLES.get(user_role, [])
        return permission in allowed_permissions


def require_role(*allowed_roles):
    """UN-97: Decorator to enforce role-based access on views"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return {'error': 'Authentication required', 'status': 401}
            
            if request.user.role.lower() not in allowed_roles:
                return {'error': 'Permission denied', 'status': 403}
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def check_staff_permission(user):
    """UN-97: Check if user has staff/admin permissions"""
    return user.is_authenticated and user.is_staff


def check_owner_permission(user, obj):
    """UN-97: Check if user owns the object"""
    return hasattr(obj, 'author') and obj.author == user or user.is_staff


def validate_user_input(data, required_fields):
    """UN-97: Validate user input to prevent injection"""
    for field in required_fields:
        if field not in data or not data[field]:
            raise ValidationError(f"{field} is required")
    return True
