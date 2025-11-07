from django.contrib import admin
from .models import (
    ConfiguracionSistema, TipoInventario, Ubicacion,
    Inventario, FotoInventario, HistorialInventario
)


@admin.register(ConfiguracionSistema)
class ConfiguracionSistemaAdmin(admin.ModelAdmin):
    list_display = ['nomenclatura_default', 'ultimo_numero', 'digitos_numeracion']

    def has_add_permission(self, request):
        # Solo debe haber una configuración
        return not ConfiguracionSistema.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # No se puede eliminar la configuración
        return False


@admin.register(TipoInventario)
class TipoInventarioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo', 'created_at']
    list_filter = ['activo']
    search_fields = ['nombre', 'descripcion']


@admin.register(Ubicacion)
class UbicacionAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'edificio', 'planta', 'activo', 'created_at']
    list_filter = ['tipo', 'activo', 'edificio']
    search_fields = ['nombre', 'edificio', 'descripcion']


class FotoInventarioInline(admin.TabularInline):
    model = FotoInventario
    extra = 1
    fields = ['foto', 'descripcion', 'es_principal']


class HistorialInventarioInline(admin.TabularInline):
    model = HistorialInventario
    extra = 0
    readonly_fields = ['accion', 'descripcion', 'usuario', 'fecha']
    can_delete = False


@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ['codigo_inventario', 'estado_ficha', 'descripcion_corta', 'tipo_inventario', 'ubicacion', 'estado', 'created_at']
    list_filter = ['estado_ficha', 'estado', 'tipo_inventario', 'ubicacion']
    search_fields = ['codigo_inventario', 'descripcion', 'campo_libre_1', 'campo_libre_2', 'campo_libre_3']
    readonly_fields = ['codigo_inventario', 'qr_code', 'created_at', 'updated_at', 'completed_at']
    inlines = [FotoInventarioInline, HistorialInventarioInline]

    fieldsets = (
        ('Información Básica', {
            'fields': ('codigo_inventario', 'estado_ficha', 'descripcion', 'tipo_inventario', 'estado')
        }),
        ('Ubicación y Fecha', {
            'fields': ('ubicacion', 'fecha_compra')
        }),
        ('Campos Libres', {
            'fields': ('campo_libre_1', 'campo_libre_2', 'campo_libre_3', 'campo_libre_4'),
            'classes': ('collapse',)
        }),
        ('Código QR', {
            'fields': ('qr_code',)
        }),
        ('Metadatos', {
            'fields': ('created_by', 'completed_by', 'created_at', 'updated_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )

    def descripcion_corta(self, obj):
        if obj.descripcion:
            return obj.descripcion[:50] + '...' if len(obj.descripcion) > 50 else obj.descripcion
        return '-'
    descripcion_corta.short_description = 'Descripción'


@admin.register(FotoInventario)
class FotoInventarioAdmin(admin.ModelAdmin):
    list_display = ['inventario', 'descripcion', 'es_principal', 'created_at']
    list_filter = ['es_principal', 'created_at']
    search_fields = ['inventario__codigo_inventario', 'descripcion']


@admin.register(HistorialInventario)
class HistorialInventarioAdmin(admin.ModelAdmin):
    list_display = ['inventario', 'accion', 'usuario', 'fecha']
    list_filter = ['accion', 'fecha']
    search_fields = ['inventario__codigo_inventario', 'descripcion']
    readonly_fields = ['inventario', 'accion', 'descripcion', 'usuario', 'fecha']
