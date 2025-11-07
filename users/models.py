from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Modelo de usuario personalizado con sistema de roles
    """
    USER_ROLES = [
        ('viewer', 'Consulta'),
        ('editor', 'Inserción de Datos'),
        ('admin', 'Administrador'),
    ]

    role = models.CharField(
        max_length=20,
        choices=USER_ROLES,
        default='viewer',
        verbose_name='Rol'
    )

    is_google_user = models.BooleanField(
        default=False,
        verbose_name='Usuario de Google'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def can_view(self):
        """Todos los usuarios pueden ver"""
        return True

    def can_edit(self):
        """Solo editores y admins pueden editar"""
        return self.role in ['editor', 'admin']

    def can_admin(self):
        """Solo admins tienen acceso total"""
        return self.role == 'admin'
