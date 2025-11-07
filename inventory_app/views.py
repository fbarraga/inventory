from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from .models import (
    Inventario, FotoInventario, TipoInventario, Ubicacion,
    HistorialInventario, ConfiguracionSistema
)
from .forms import (
    GenerarEtiquetasForm, CompletarFichaForm, InventarioEditForm,
    FotoInventarioForm, TipoInventarioForm, UbicacionForm,
    ConfiguracionSistemaForm, BusquedaInventarioForm
)
from users.decorators import editor_required, admin_required
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import cm
import io


@login_required
def dashboard(request):
    """Dashboard principal"""
    total_inventarios = Inventario.objects.count()
    fichas_vacias = Inventario.objects.filter(estado_ficha='vacia').count()
    fichas_completadas = Inventario.objects.filter(estado_ficha='completada').count()

    por_tipo = TipoInventario.objects.annotate(
        total=Count('inventarios')
    ).filter(activo=True, total__gt=0)[:5]

    por_ubicacion = Ubicacion.objects.annotate(
        total=Count('inventarios')
    ).filter(activo=True, total__gt=0)[:5]

    ultimos = Inventario.objects.select_related(
        'tipo_inventario', 'ubicacion', 'created_by'
    ).order_by('-created_at')[:10]

    context = {
        'total_inventarios': total_inventarios,
        'fichas_vacias': fichas_vacias,
        'fichas_completadas': fichas_completadas,
        'por_tipo': por_tipo,
        'por_ubicacion': por_ubicacion,
        'ultimos': ultimos,
    }

    return render(request, 'inventory_app/dashboard.html', context)


# ==================== GENERACIÓN DE ETIQUETAS ====================

@login_required
@editor_required
def generar_etiquetas(request):
    """Generar etiquetas QR en lote"""
    if request.method == 'POST':
        form = GenerarEtiquetasForm(request.POST)
        if form.is_valid():
            cantidad = form.cleaned_data['cantidad']
            usar_personalizada = form.cleaned_data['usar_nomenclatura_personalizada']
            nomenclatura_personalizada = form.cleaned_data.get('nomenclatura_personalizada')

            inventarios_creados = []
            config = ConfiguracionSistema.get_config()

            # Guardar nomenclatura temporal si se usa personalizada
            nomenclatura_original = None
            if usar_personalizada and nomenclatura_personalizada:
                nomenclatura_original = config.nomenclatura_default
                config.nomenclatura_default = nomenclatura_personalizada
                config.save()

            # Crear fichas vacías
            for i in range(cantidad):
                inventario = Inventario.objects.create(
                    estado_ficha='vacia',
                    created_by=request.user
                )
                inventarios_creados.append(inventario)

                # Registrar en historial
                HistorialInventario.objects.create(
                    inventario=inventario,
                    accion='generacion_etiqueta',
                    descripcion=f'Etiqueta generada en lote',
                    usuario=request.user
                )

            # Restaurar nomenclatura original
            if nomenclatura_original:
                config.nomenclatura_default = nomenclatura_original
                config.save()

            messages.success(
                request,
                f'¡{cantidad} etiquetas generadas exitosamente! Descarga el PDF para imprimir.'
            )

            # Guardar IDs en sesión para descargar PDF
            request.session['etiquetas_generadas'] = [inv.id for inv in inventarios_creados]

            return redirect('descargar_etiquetas_pdf')
    else:
        form = GenerarEtiquetasForm()

    config = ConfiguracionSistema.get_config()

    context = {
        'form': form,
        'config': config,
    }

    return render(request, 'inventory_app/generar_etiquetas.html', context)


@login_required
@editor_required
def descargar_etiquetas_pdf(request):
    """Descargar PDF con etiquetas generadas"""
    etiquetas_ids = request.session.get('etiquetas_generadas', [])

    if not etiquetas_ids:
        messages.error(request, 'No hay etiquetas para descargar')
        return redirect('generar_etiquetas')

    inventarios = Inventario.objects.filter(id__in=etiquetas_ids)

    # Crear PDF
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Obtener configuración de etiquetas
    config = ConfiguracionSistema.get_config()
    etiquetas_por_fila = config.etiquetas_por_fila
    etiquetas_por_columna = config.etiquetas_por_columna

    margen_x = 2 * cm
    margen_y = 2 * cm
    espacio_entre_etiquetas_x = 1 * cm
    espacio_entre_etiquetas_y = 1 * cm

    ancho_etiqueta = (width - 2 * margen_x - (etiquetas_por_fila - 1) * espacio_entre_etiquetas_x) / etiquetas_por_fila
    alto_etiqueta = (height - 2 * margen_y - (etiquetas_por_columna - 1) * espacio_entre_etiquetas_y) / etiquetas_por_columna

    contador = 0
    for inventario in inventarios:
        if contador > 0 and contador % (etiquetas_por_fila * etiquetas_por_columna) == 0:
            p.showPage()

        posicion_en_pagina = contador % (etiquetas_por_fila * etiquetas_por_columna)
        fila = posicion_en_pagina // etiquetas_por_fila
        columna = posicion_en_pagina % etiquetas_por_fila

        x = margen_x + columna * (ancho_etiqueta + espacio_entre_etiquetas_x)
        y = height - margen_y - (fila + 1) * alto_etiqueta - fila * espacio_entre_etiquetas_y

        # Dibujar borde de etiqueta
        p.rect(x, y, ancho_etiqueta, alto_etiqueta)

        # Título
        p.setFont("Helvetica-Bold", 10)
        p.drawString(x + 0.5 * cm, y + alto_etiqueta - 1 * cm, "Institut Sa Palomera")

        # Código
        p.setFont("Helvetica-Bold", 14)
        p.drawString(x + 0.5 * cm, y + alto_etiqueta - 2 * cm, inventario.codigo_inventario)

        # QR Code
        if inventario.qr_code:
            try:
                qr_img = ImageReader(inventario.qr_code.path)
                qr_size = min(ancho_etiqueta, alto_etiqueta) - 4 * cm
                qr_x = x + (ancho_etiqueta - qr_size) / 2
                qr_y = y + 1 * cm
                p.drawImage(qr_img, qr_x, qr_y, width=qr_size, height=qr_size)
            except:
                p.setFont("Helvetica", 8)
                p.drawString(x + 0.5 * cm, y + 2 * cm, "QR no disponible")

        contador += 1

    p.showPage()
    p.save()

    buffer.seek(0)

    # Limpiar sesión
    del request.session['etiquetas_generadas']

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="etiquetas_inventario.pdf"'

    return response


# ==================== ESCANEO Y COMPLETAR FICHA ====================

@login_required
def scan_qr(request):
    """Vista para escanear QR"""
    codigo = request.GET.get('codigo') or request.POST.get('codigo')

    if codigo:
        try:
            inventario = Inventario.objects.get(codigo_inventario=codigo)

            if inventario.is_empty():
                # Si la ficha está vacía, redirigir a completar
                return redirect('completar_ficha', codigo=inventario.codigo_inventario)
            else:
                # Si está completada, mostrar detalle
                return redirect('inventario_detail', pk=inventario.pk)

        except Inventario.DoesNotExist:
            messages.error(request, f'No se encontró inventario con código: {codigo}')

    return render(request, 'inventory_app/scan_qr.html')


@login_required
@editor_required
def completar_ficha(request, codigo):
    """Completar una ficha vacía escaneando su QR"""
    inventario = get_object_or_404(Inventario, codigo_inventario=codigo)

    if inventario.is_completed():
        messages.info(request, 'Esta ficha ya está completada')
        return redirect('inventario_detail', pk=inventario.pk)

    if request.method == 'POST':
        form = CompletarFichaForm(request.POST, request.FILES, instance=inventario)

        if form.is_valid():
            inventario = form.save(commit=False)
            inventario.estado_ficha = 'completada'
            inventario.completed_by = request.user
            inventario.completed_at = timezone.now()
            inventario.save()

            # Guardar múltiples fotos
            fotos_data = request.POST.get('fotos_data', '[]')
            import json
            try:
                fotos_list = json.loads(fotos_data)
                for idx, foto_base64 in enumerate(fotos_list):
                    if foto_base64.startswith('data:image'):
                        # Extraer datos de la imagen base64
                        import base64
                        format, imgstr = foto_base64.split(';base64,')
                        ext = format.split('/')[-1]

                        from django.core.files.base import ContentFile
                        foto_file = ContentFile(base64.b64decode(imgstr), name=f'{inventario.codigo_inventario}_foto_{idx+1}.{ext}')

                        FotoInventario.objects.create(
                            inventario=inventario,
                            foto=foto_file,
                            es_principal=(idx == 0),
                            descripcion=f'Foto {idx+1}'
                        )
            except (json.JSONDecodeError, Exception) as e:
                print(f"Error procesando fotos: {e}")

            # Registrar en historial
            HistorialInventario.objects.create(
                inventario=inventario,
                accion='completar_ficha',
                descripcion=f'Ficha completada desde escaneo QR',
                usuario=request.user
            )

            messages.success(request, f'¡Ficha {inventario.codigo_inventario} completada exitosamente!')
            return redirect('inventario_detail', pk=inventario.pk)
    else:
        form = CompletarFichaForm(instance=inventario)

    context = {
        'form': form,
        'inventario': inventario,
    }

    return render(request, 'inventory_app/completar_ficha.html', context)


# ==================== GESTIÓN DE INVENTARIO ====================

@login_required
def inventario_list(request):
    """Lista de inventarios con búsqueda y filtros"""
    inventarios = Inventario.objects.select_related(
        'tipo_inventario', 'ubicacion', 'created_by'
    ).all()

    form = BusquedaInventarioForm(request.GET)

    if form.is_valid():
        q = form.cleaned_data.get('q')
        if q:
            inventarios = inventarios.filter(
                Q(codigo_inventario__icontains=q) |
                Q(descripcion__icontains=q) |
                Q(campo_libre_1__icontains=q) |
                Q(campo_libre_2__icontains=q) |
                Q(campo_libre_3__icontains=q)
            )

        tipo = form.cleaned_data.get('tipo_inventario')
        if tipo:
            inventarios = inventarios.filter(tipo_inventario=tipo)

        ubicacion = form.cleaned_data.get('ubicacion')
        if ubicacion:
            inventarios = inventarios.filter(ubicacion=ubicacion)

        estado_ficha = form.cleaned_data.get('estado_ficha')
        if estado_ficha:
            inventarios = inventarios.filter(estado_ficha=estado_ficha)

        estado = form.cleaned_data.get('estado')
        if estado:
            inventarios = inventarios.filter(estado=estado)

    inventarios = inventarios.order_by('-created_at')

    context = {
        'inventarios': inventarios,
        'form': form,
    }

    return render(request, 'inventory_app/inventario_list.html', context)


@login_required
def inventario_detail(request, pk):
    """Detalle de un inventario"""
    inventario = get_object_or_404(
        Inventario.objects.select_related('tipo_inventario', 'ubicacion', 'created_by', 'completed_by'),
        pk=pk
    )
    fotos = inventario.fotos.all()
    historial = inventario.historial.select_related('usuario').all()[:10]

    context = {
        'inventario': inventario,
        'fotos': fotos,
        'historial': historial,
    }

    return render(request, 'inventory_app/inventario_detail.html', context)


@login_required
@editor_required
def inventario_edit(request, pk):
    """Editar inventario existente"""
    inventario = get_object_or_404(Inventario, pk=pk)

    if request.method == 'POST':
        form = InventarioEditForm(request.POST, instance=inventario)

        if form.is_valid():
            form.save()

            # Registrar en historial
            HistorialInventario.objects.create(
                inventario=inventario,
                accion='edicion',
                descripcion=f'Inventario actualizado',
                usuario=request.user
            )

            messages.success(request, f'Inventario {inventario.codigo_inventario} actualizado')
            return redirect('inventario_detail', pk=inventario.pk)
    else:
        form = InventarioEditForm(instance=inventario)

    context = {
        'form': form,
        'inventario': inventario,
        'action': 'Editar'
    }

    return render(request, 'inventory_app/inventario_edit.html', context)


@login_required
@admin_required
@require_http_methods(["POST"])
def inventario_delete(request, pk):
    """Eliminar inventario (solo administradores)"""
    inventario = get_object_or_404(Inventario, pk=pk)
    codigo = inventario.codigo_inventario
    inventario.delete()

    messages.success(request, f'Inventario {codigo} eliminado exitosamente')
    return redirect('inventario_list')


@login_required
@editor_required
def inventario_add_photo(request, pk):
    """Añadir foto adicional a un inventario"""
    inventario = get_object_or_404(Inventario, pk=pk)

    if request.method == 'POST':
        form = FotoInventarioForm(request.POST, request.FILES)
        if form.is_valid():
            foto = form.save(commit=False)
            foto.inventario = inventario
            foto.save()

            messages.success(request, 'Foto añadida correctamente')
            return redirect('inventario_detail', pk=inventario.pk)
    else:
        form = FotoInventarioForm()

    context = {
        'form': form,
        'inventario': inventario,
    }

    return render(request, 'inventory_app/foto_form.html', context)


# ==================== TABLAS AUXILIARES ====================

@login_required
@admin_required
def tipo_inventario_list(request):
    """Lista de tipos de inventario"""
    tipos = TipoInventario.objects.annotate(
        total_inventarios=Count('inventarios')
    ).order_by('nombre')

    return render(request, 'inventory_app/tipo_inventario_list.html', {'tipos': tipos})


@login_required
@admin_required
def tipo_inventario_create(request):
    """Crear tipo de inventario"""
    if request.method == 'POST':
        form = TipoInventarioForm(request.POST)
        if form.is_valid():
            tipo = form.save()
            messages.success(request, f'Tipo "{tipo.nombre}" creado exitosamente')
            return redirect('tipo_inventario_list')
    else:
        form = TipoInventarioForm()

    return render(request, 'inventory_app/tipo_inventario_form.html', {'form': form, 'action': 'Crear'})


@login_required
@admin_required
def tipo_inventario_edit(request, pk):
    """Editar tipo de inventario"""
    tipo = get_object_or_404(TipoInventario, pk=pk)

    if request.method == 'POST':
        form = TipoInventarioForm(request.POST, instance=tipo)
        if form.is_valid():
            form.save()
            messages.success(request, f'Tipo "{tipo.nombre}" actualizado')
            return redirect('tipo_inventario_list')
    else:
        form = TipoInventarioForm(instance=tipo)

    return render(request, 'inventory_app/tipo_inventario_form.html', {
        'form': form,
        'tipo': tipo,
        'action': 'Editar'
    })


@login_required
@admin_required
def ubicacion_list(request):
    """Lista de ubicaciones"""
    ubicaciones = Ubicacion.objects.annotate(
        total_inventarios=Count('inventarios')
    ).order_by('edificio', 'planta', 'nombre')

    return render(request, 'inventory_app/ubicacion_list.html', {'ubicaciones': ubicaciones})


@login_required
@admin_required
def ubicacion_create(request):
    """Crear ubicación"""
    if request.method == 'POST':
        form = UbicacionForm(request.POST)
        if form.is_valid():
            ubicacion = form.save()
            messages.success(request, f'Ubicación "{ubicacion.nombre}" creada exitosamente')
            return redirect('ubicacion_list')
    else:
        form = UbicacionForm()

    return render(request, 'inventory_app/ubicacion_form.html', {'form': form, 'action': 'Crear'})


@login_required
@admin_required
def ubicacion_edit(request, pk):
    """Editar ubicación"""
    ubicacion = get_object_or_404(Ubicacion, pk=pk)

    if request.method == 'POST':
        form = UbicacionForm(request.POST, instance=ubicacion)
        if form.is_valid():
            form.save()
            messages.success(request, f'Ubicación "{ubicacion.nombre}" actualizada')
            return redirect('ubicacion_list')
    else:
        form = UbicacionForm(instance=ubicacion)

    return render(request, 'inventory_app/ubicacion_form.html', {
        'form': form,
        'ubicacion': ubicacion,
        'action': 'Editar'
    })


@login_required
@admin_required
def configuracion_sistema(request):
    """Configuración del sistema"""
    config = ConfiguracionSistema.get_config()

    if request.method == 'POST':
        form = ConfiguracionSistemaForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, 'Configuración actualizada exitosamente')
            return redirect('configuracion_sistema')
    else:
        form = ConfiguracionSistemaForm(instance=config)

    return render(request, 'inventory_app/configuracion_sistema.html', {
        'form': form,
        'config': config
    })
