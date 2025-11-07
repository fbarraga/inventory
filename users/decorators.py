from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def admin_required(view_func):
    """Decorator para verificar que el usuario es administrador"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.can_admin():
            messages.error(request, 'No tienes permisos para acceder a esta página')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


def editor_required(view_func):
    """Decorator para verificar que el usuario puede editar"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.can_edit():
            messages.error(request, 'No tienes permisos para realizar esta acción')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper
