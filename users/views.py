from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .decorators import admin_required
from django.conf import settings
from django.core.cache import cache
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
import logging

security_logger = logging.getLogger('django.security.login')


def _client_ip(request):
    """IP real del client. El proxy nginx posa X-Real-IP; la connexió directa ve del proxy."""
    return request.META.get('HTTP_X_REAL_IP') or request.META.get('REMOTE_ADDR', '')


def _login_keys(request, username):
    """Claus del comptador d'intents fallits amb el seu límit: (clau, màxim)."""
    keys = [(f'login-fail:ip:{_client_ip(request)}', settings.LOGIN_MAX_ATTEMPTS)]
    if username:
        keys.append((f'login-fail:user:{username.lower()[:150]}', settings.LOGIN_MAX_ATTEMPTS_PER_USER))
    return keys


def _login_blocked(keys):
    return any(cache.get(k, 0) >= limit for k, limit in keys)


def _register_failure(keys):
    for k, _ in keys:
        cache.add(k, 0, settings.LOGIN_LOCKOUT_SECONDS)
        try:
            cache.incr(k)
        except ValueError:
            cache.set(k, 1, settings.LOGIN_LOCKOUT_SECONDS)


@sensitive_post_parameters('password')
@never_cache
def login_view(request):
    """Vista de login amb límit d'intents per IP i per usuari"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    status = 200
    if request.method == 'POST':
        username = (request.POST.get('username') or '').strip()
        password = request.POST.get('password') or ''
        keys = _login_keys(request, username)

        if _login_blocked(keys):
            security_logger.warning('Login bloquejat per massa intents ip=%s', _client_ip(request))
            messages.error(request, 'Massa intents fallits. Torna-ho a provar d\'aquí a uns minuts.')
            return render(request, 'users/login.html', status=429)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            for k, _ in keys:
                cache.delete(k)
            login(request, user)
            messages.success(request, f'¡Bienvenido, {user.first_name or user.username}!')
            return redirect('dashboard')

        _register_failure(keys)
        security_logger.warning('Login fallit ip=%s', _client_ip(request))
        messages.error(request, 'Usuario o contraseña incorrectos')
        # 401: el proxy i fail2ban ho compten com a error (un 200 passava desapercebut)
        status = 401

    return render(request, 'users/login.html', status=status)


@login_required
@require_http_methods(["POST"])
def logout_view(request):
    """Vista de logout (només POST, per evitar logouts forçats amb enllaços)"""
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente')
    return redirect('login')


@login_required
@admin_required
def user_list(request):
    """Lista de usuarios (solo administradores)"""
    users = CustomUser.objects.all().order_by('-date_joined')
    return render(request, 'users/user_list.html', {'users': users})


@login_required
@admin_required
def user_create(request):
    """Crear nuevo usuario (solo administradores)"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Usuario {user.username} creado exitosamente')
            return redirect('user_list')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/user_form.html', {'form': form, 'action': 'Crear'})


@login_required
@admin_required
def user_edit(request, pk):
    """Editar usuario (solo administradores)"""
    user = get_object_or_404(CustomUser, pk=pk)

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Usuario {user.username} actualizado exitosamente')
            return redirect('user_list')
    else:
        form = CustomUserChangeForm(instance=user)

    return render(request, 'users/user_form.html', {'form': form, 'action': 'Editar', 'user_obj': user})


@login_required
@admin_required
@require_http_methods(["POST"])
def user_delete(request, pk):
    """Eliminar usuario (solo administradores)"""
    user = get_object_or_404(CustomUser, pk=pk)

    if user == request.user:
        messages.error(request, 'No puedes eliminar tu propio usuario')
    else:
        username = user.username
        user.delete()
        messages.success(request, f'Usuario {username} eliminado exitosamente')

    return redirect('user_list')


@login_required
def profile_view(request):
    """Ver perfil del usuario actual"""
    return render(request, 'users/profile.html', {'user': request.user})
