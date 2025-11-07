from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Generación de etiquetas QR en lote
    path('etiquetas/generar/', views.generar_etiquetas, name='generar_etiquetas'),
    path('etiquetas/descargar-pdf/', views.descargar_etiquetas_pdf, name='descargar_etiquetas_pdf'),

    # Escaneo QR y completar ficha
    path('scan/', views.scan_qr, name='scan_qr'),
    path('completar/<str:codigo>/', views.completar_ficha, name='completar_ficha'),

    # Inventario
    path('inventario/', views.inventario_list, name='inventario_list'),
    path('inventario/<int:pk>/', views.inventario_detail, name='inventario_detail'),
    path('inventario/<int:pk>/editar/', views.inventario_edit, name='inventario_edit'),
    path('inventario/<int:pk>/eliminar/', views.inventario_delete, name='inventario_delete'),
    path('inventario/<int:pk>/añadir-foto/', views.inventario_add_photo, name='inventario_add_photo'),

    # Tipos de Inventario
    path('tipos/', views.tipo_inventario_list, name='tipo_inventario_list'),
    path('tipos/crear/', views.tipo_inventario_create, name='tipo_inventario_create'),
    path('tipos/<int:pk>/editar/', views.tipo_inventario_edit, name='tipo_inventario_edit'),

    # Ubicaciones
    path('ubicaciones/', views.ubicacion_list, name='ubicacion_list'),
    path('ubicaciones/crear/', views.ubicacion_create, name='ubicacion_create'),
    path('ubicaciones/<int:pk>/editar/', views.ubicacion_edit, name='ubicacion_edit'),

    # Configuración del sistema
    path('configuracion/', views.configuracion_sistema, name='configuracion_sistema'),
]
