from functools import wraps
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages


def role_required(allowed_roles, redirect_name='home', message="Vous n'avez pas accès à cette page."):
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not hasattr(request.user, 'role') or request.user.role not in allowed_roles:
                messages.error(request, message)
                return redirect(redirect_name)
            return view_func(request, *args, **kwargs)

        return _wrapped_view
    return decorator


def admin_or_gestionnaire_required(view_func):
    return role_required(['ADMIN', 'GESTIONNAIRE'])(view_func)


def admin_required(view_func):
    return role_required(['ADMIN'])(view_func)
