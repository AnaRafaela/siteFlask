from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission

def permission_required(perm):
    def decorator(f):
        @wraps(f)
        def decorator_function(*args, **kwargs):
            if not current_user.has_permission(perm):
                abort(403)
            return f(*args, **kwargs)
        return decorator_function
    return decorator

def admin_required(f):
    return permission_required(Permission.ADMIN)(f)

def mod_required(f):
    return permission_required(Permission.MODERATE)(f)