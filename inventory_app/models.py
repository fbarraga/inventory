from django.db import models
from django.conf import settings
import qrcode
from io import BytesIO
from django.core.files import File


class ConfiguracionSistema(models.Model):
    """Configuración global del sistema - nomenclatura de etiquetas"""
    nomenclatura_default = models.CharField(
        max_length=50,
        default='INV-',
        verbose_name='Nomenclatura por Defecto',
        help_text='Prefijo para los códigos de inventario. Ej: INV-'
    )

    ultimo_numero = models.IntegerField(
        default=0,
        verbose_name='Último Número Generado',
        help_text='Contador para generar códigos únicos'
    )

    digitos_numeracion = models.IntegerField(
        default=4,
        verbose_name='Dígitos de Numeración',
        help_text='Número de dígitos para la parte numérica. Ej: 4 = 0001, 0002...'
    )

    etiquetas_por_fila = models.IntegerField(
        default=2,
        verbose_name='Etiquetas por Fila',
        help_text='Número de etiquetas horizontales en el PDF'
    )

    etiquetas_por_columna = models.IntegerField(
        default=2,
        verbose_name='Etiquetas por Columna',
        help_text='Número de etiquetas verticales en el PDF'
    )

    class Meta:
        verbose_name = 'Configuración del Sistema'
        verbose_name_plural = 'Configuración del Sistema'

    def __str__(self):
        return 'Configuración del Sistema'

    def generar_codigo(self):
        """Genera el siguiente código de inventario"""
        self.ultimo_numero += 1
        self.save()
        numero_str = str(self.ultimo_numero).zfill(self.digitos_numeracion)
        return f"{self.nomenclatura_default}{numero_str}"

    @classmethod
    def get_config(cls):
        """Obtiene o crea la configuración del sistema"""
        config, created = cls.objects.get_or_create(pk=1)
        return config


class TipoInventario(models.Model):
    """Tipos de inventario: ordenador, mesa, silla, etc."""
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    activo = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tipo de Inventario'
        verbose_name_plural = 'Tipos de Inventario'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Ubicacion(models.Model):
    """Ubicaciones: aula, armario, etc."""
    TIPO_UBICACION = [
        ('aula', 'Aula'),
        ('armario', 'Armario'),
        ('almacen', 'Almacén'),
        ('oficina', 'Oficina'),
        ('laboratorio', 'Laboratorio'),
        ('otro', 'Otro'),
    ]

    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    tipo = models.CharField(max_length=20, choices=TIPO_UBICACION, default='otro', verbose_name='Tipo')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    edificio = models.CharField(max_length=100, blank=True, verbose_name='Edificio')
    planta = models.CharField(max_length=50, blank=True, verbose_name='Planta')
    activo = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Ubicación'
        verbose_name_plural = 'Ubicaciones'
        ordering = ['edificio', 'planta', 'nombre']

    def __str__(self):
        ubicacion = self.nombre
        if self.edificio:
            ubicacion = f"{self.edificio} - {ubicacion}"
        if self.planta:
            ubicacion = f"{ubicacion} (Planta {self.planta})"
        return ubicacion


class Inventario(models.Model):
    """Modelo principal de inventario - Soporta fichas vacías"""
    ESTADO_FICHA = [
        ('vacia', 'Ficha Vacía'),
        ('completada', 'Ficha Completada'),
    ]

    ESTADO_ACTIVO = [
        ('disponible', 'Disponible'),
        ('en_uso', 'En Uso'),
        ('mantenimiento', 'Mantenimiento'),
        ('baja', 'Dado de Baja'),
        ('extraviado', 'Extraviado'),
    ]

    # Código único de inventario (siempre obligatorio)
    codigo_inventario = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Código de Inventario',
        editable=False
    )

    # Estado de la ficha
    estado_ficha = models.CharField(
        max_length=20,
        choices=ESTADO_FICHA,
        default='vacia',
        verbose_name='Estado de Ficha'
    )

    # Información básica (opcional hasta completar)
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción')
    tipo_inventario = models.ForeignKey(
        TipoInventario,
        on_delete=models.PROTECT,
        related_name='inventarios',
        verbose_name='Tipo',
        blank=True,
        null=True
    )

    # Fecha de compra (opcional hasta completar)
    fecha_compra = models.DateField(blank=True, null=True, verbose_name='Fecha de Compra')

    # Ubicación (opcional hasta completar)
    ubicacion = models.ForeignKey(
        Ubicacion,
        on_delete=models.PROTECT,
        related_name='inventarios',
        verbose_name='Ubicación',
        blank=True,
        null=True
    )

    # Estado del activo (opcional hasta completar)
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_ACTIVO,
        default='disponible',
        verbose_name='Estado',
        blank=True
    )

    # Campos libres para contabilidad u otros usos
    campo_libre_1 = models.CharField(max_length=200, blank=True, verbose_name='Campo Libre 1')
    campo_libre_2 = models.CharField(max_length=200, blank=True, verbose_name='Campo Libre 2')
    campo_libre_3 = models.CharField(max_length=200, blank=True, verbose_name='Campo Libre 3')
    campo_libre_4 = models.TextField(blank=True, verbose_name='Campo Libre 4')

    # Código QR
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, verbose_name='Código QR')

    # Metadatos
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='inventarios_creados',
        verbose_name='Creado por'
    )
    completed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='inventarios_completados',
        verbose_name='Completado por'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de completado')

    class Meta:
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'
        ordering = ['-created_at']

    def __str__(self):
        if self.estado_ficha == 'vacia':
            return f"{self.codigo_inventario} - Ficha Vacía"
        return f"{self.codigo_inventario} - {self.descripcion[:50] if self.descripcion else 'Sin descripción'}"

    def save(self, *args, **kwargs):
        """Generar código de inventario único y QR al guardar"""
        if not self.codigo_inventario:
            # Generar código único usando la configuración del sistema
            config = ConfiguracionSistema.get_config()
            self.codigo_inventario = config.generar_codigo()

        # Guardar primero para tener el ID
        super().save(*args, **kwargs)

        # Generar QR si no existe
        if not self.qr_code:
            self.generate_qr_code()
            # Guardar nuevamente con el QR
            super().save(update_fields=['qr_code'])

    def generate_qr_code(self):
        """Genera el código QR para el inventario"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        # El QR contendrá el código de inventario
        qr.add_data(self.codigo_inventario)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Guardar en BytesIO
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)

        # Guardar en el campo qr_code
        filename = f'qr_{self.codigo_inventario}.png'
        self.qr_code.save(filename, File(buffer), save=False)

    def is_empty(self):
        """Verifica si la ficha está vacía"""
        return self.estado_ficha == 'vacia'

    def is_completed(self):
        """Verifica si la ficha está completada"""
        return self.estado_ficha == 'completada'


class FotoInventario(models.Model):
    """Fotografías del inventario"""
    inventario = models.ForeignKey(
        Inventario,
        on_delete=models.CASCADE,
        related_name='fotos',
        verbose_name='Inventario'
    )
    foto = models.ImageField(upload_to='inventario_fotos/', verbose_name='Fotografía')
    descripcion = models.CharField(max_length=200, blank=True, verbose_name='Descripción')
    es_principal = models.BooleanField(default=False, verbose_name='Foto Principal')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Fotografía de Inventario'
        verbose_name_plural = 'Fotografías de Inventario'
        ordering = ['-es_principal', '-created_at']

    def __str__(self):
        return f"Foto de {self.inventario.codigo_inventario}"

    def save(self, *args, **kwargs):
        """Si es principal, quitar el flag de otras fotos"""
        if self.es_principal:
            FotoInventario.objects.filter(
                inventario=self.inventario,
                es_principal=True
            ).update(es_principal=False)
        super().save(*args, **kwargs)


class HistorialInventario(models.Model):
    """Historial de cambios del inventario"""
    inventario = models.ForeignKey(
        Inventario,
        on_delete=models.CASCADE,
        related_name='historial',
        verbose_name='Inventario'
    )
    accion = models.CharField(max_length=50, verbose_name='Acción')
    descripcion = models.TextField(verbose_name='Descripción')
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Usuario'
    )
    fecha = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')

    class Meta:
        verbose_name = 'Historial de Inventario'
        verbose_name_plural = 'Historiales de Inventario'
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.inventario.codigo_inventario} - {self.accion} - {self.fecha}"
