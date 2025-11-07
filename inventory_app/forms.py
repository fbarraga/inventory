from django import forms
from .models import Inventario, FotoInventario, TipoInventario, Ubicacion, ConfiguracionSistema


class GenerarEtiquetasForm(forms.Form):
    """Formulario para generar etiquetas en lote"""
    cantidad = forms.IntegerField(
        min_value=1,
        max_value=1000,
        initial=10,
        label='Cantidad de Etiquetas',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    usar_nomenclatura_personalizada = forms.BooleanField(
        required=False,
        label='Usar nomenclatura personalizada',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    nomenclatura_personalizada = forms.CharField(
        required=False,
        max_length=50,
        label='Nomenclatura Personalizada',
        help_text='Ej: AULA-2025- o ORD-',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: AULA-2025-'
        })
    )


class CompletarFichaForm(forms.ModelForm):
    """Formulario para completar una ficha vacía"""

    class Meta:
        model = Inventario
        fields = [
            'descripcion', 'tipo_inventario', 'fecha_compra', 'ubicacion',
            'estado', 'campo_libre_1', 'campo_libre_2', 'campo_libre_3', 'campo_libre_4'
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción detallada del activo',
                'required': True
            }),
            'tipo_inventario': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'fecha_compra': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'ubicacion': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'campo_libre_1': forms.TextInput(attrs={'class': 'form-control'}),
            'campo_libre_2': forms.TextInput(attrs={'class': 'form-control'}),
            'campo_libre_3': forms.TextInput(attrs={'class': 'form-control'}),
            'campo_libre_4': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class InventarioEditForm(forms.ModelForm):
    """Formulario para editar inventario existente"""

    class Meta:
        model = Inventario
        fields = [
            'descripcion', 'tipo_inventario', 'fecha_compra', 'ubicacion',
            'estado', 'campo_libre_1', 'campo_libre_2', 'campo_libre_3', 'campo_libre_4'
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tipo_inventario': forms.Select(attrs={'class': 'form-select'}),
            'fecha_compra': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'ubicacion': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'campo_libre_1': forms.TextInput(attrs={'class': 'form-control'}),
            'campo_libre_2': forms.TextInput(attrs={'class': 'form-control'}),
            'campo_libre_3': forms.TextInput(attrs={'class': 'form-control'}),
            'campo_libre_4': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class FotoInventarioForm(forms.ModelForm):
    """Formulario para añadir fotos adicionales"""

    class Meta:
        model = FotoInventario
        fields = ['foto', 'descripcion', 'es_principal']
        widgets = {
            'foto': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'capture': 'environment'
            }),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'es_principal': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class TipoInventarioForm(forms.ModelForm):
    """Formulario para tipos de inventario"""

    class Meta:
        model = TipoInventario
        fields = ['nombre', 'descripcion', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class UbicacionForm(forms.ModelForm):
    """Formulario para ubicaciones"""

    class Meta:
        model = Ubicacion
        fields = ['nombre', 'tipo', 'edificio', 'planta', 'descripcion', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'edificio': forms.TextInput(attrs={'class': 'form-control'}),
            'planta': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ConfiguracionSistemaForm(forms.ModelForm):
    """Formulario para configuración del sistema"""

    class Meta:
        model = ConfiguracionSistema
        fields = ['nomenclatura_default', 'digitos_numeracion', 'etiquetas_por_fila', 'etiquetas_por_columna']
        widgets = {
            'nomenclatura_default': forms.TextInput(attrs={'class': 'form-control'}),
            'digitos_numeracion': forms.NumberInput(attrs={'class': 'form-control'}),
            'etiquetas_por_fila': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '10'}),
            'etiquetas_por_columna': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '10'}),
        }


class BusquedaInventarioForm(forms.Form):
    """Formulario de búsqueda de inventario"""
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por código, descripción...'
        })
    )
    tipo_inventario = forms.ModelChoiceField(
        queryset=TipoInventario.objects.filter(activo=True),
        required=False,
        empty_label='Todos los tipos',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    ubicacion = forms.ModelChoiceField(
        queryset=Ubicacion.objects.filter(activo=True),
        required=False,
        empty_label='Todas las ubicaciones',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    estado_ficha = forms.ChoiceField(
        choices=[('', 'Todos'), ('vacia', 'Ficha Vacía'), ('completada', 'Ficha Completada')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    estado = forms.ChoiceField(
        choices=[('', 'Todos los estados')] + Inventario.ESTADO_ACTIVO,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
