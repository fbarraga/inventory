"""
URL configuration for inventory project.
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.http import HttpResponse
from inventory_app.views import protected_media


def healthz(request):
    """Healthcheck del contenidor. Públic: no toca la BD ni retorna dades."""
    return HttpResponse("ok", content_type="text/plain")


urlpatterns = [
    path('healthz', healthz, name='healthz'),
    path('auth/', include('social_django.urls', namespace='social')),
    path('users/', include('users.urls')),
    # Fotos i QR: sempre darrere de login (mai servits directament)
    re_path(r'^media/(?P<path>.+)$', protected_media, name='protected_media'),
    path('', include('inventory_app.urls')),
]

if settings.DJANGO_ADMIN_ENABLED:
    urlpatterns.insert(0, path('admin/', admin.site.urls))
