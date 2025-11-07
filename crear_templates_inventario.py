"""
Script para crear templates de inventario
Ejecutar con: python crear_templates_inventario.py
"""

import os

os.makedirs('templates/inventory_app', exist_ok=True)

TEMPLATES = {
    'templates/inventory_app/dashboard.html': '''{% extends 'base.html' %}
{% block content %}
<h1><i class="bi bi-speedometer2"></i> Dashboard</h1>
<div class="row mt-4">
    <div class="col-md-4">
        <div class="card text-white" style="background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);">
            <div class="card-body">
                <h5>Total de Activos</h5>
                <h2>{{ total_inventarios }}</h2>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card text-white" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);">
            <div class="card-body">
                <h5>Fichas Vacías</h5>
                <h2>{{ fichas_vacias }}</h2>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card text-white" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);">
            <div class="card-body">
                <h5>Fichas Completadas</h5>
                <h2>{{ fichas_completadas }}</h2>
            </div>
        </div>
    </div>
</div>
<div class="row mt-4">
    <div class="col-md-12">
        <div class="card">
            <div class="card-header d-flex justify-content-between">
                <span><i class="bi bi-clock-history"></i> Últimos Inventarios</span>
                <a href="{% url 'inventario_list' %}" class="btn btn-sm btn-primary">Ver Todos</a>
            </div>
            <div class="card-body">
                {% if ultimos %}
                <table class="table">
                    <thead>
                        <tr>
                            <th>Código</th>
                            <th>Estado</th>
                            <th>Descripción</th>
                            <th>Tipo</th>
                            <th>Ubicación</th>
                            <th>Fecha</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for inv in ultimos %}
                        <tr>
                            <td><a href="{% url 'inventario_detail' inv.pk %}">{{ inv.codigo_inventario }}</a></td>
                            <td>{% if inv.estado_ficha == 'vacia' %}<span class="badge bg-warning">Vacía</span>{% else %}<span class="badge bg-success">Completada</span>{% endif %}</td>
                            <td>{{ inv.descripcion|default:"-"|truncatewords:8 }}</td>
                            <td>{{ inv.tipo_inventario|default:"-" }}</td>
                            <td>{{ inv.ubicacion|default:"-" }}</td>
                            <td>{{ inv.created_at|date:"d/m/Y" }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% else %}
                <p class="text-center text-muted my-4">No hay inventarios registrados</p>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    'templates/inventory_app/generar_etiquetas.html': '''{% extends 'base.html' %}
{% block content %}
<h1><i class="bi bi-qr-code"></i> Generar Etiquetas QR en Lote</h1>
<div class="row mt-4">
    <div class="col-md-8">
        <div class="card">
            <div class="card-header">Formulario de Generación</div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    {{ form.as_p }}
                    <button type="submit" class="btn btn-primary btn-lg">
                        <i class="bi bi-printer"></i> Generar y Descargar PDF
                    </button>
                </form>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card bg-info text-white">
            <div class="card-body">
                <h5>Configuración Actual</h5>
                <p><strong>Nomenclatura:</strong><br>{{ config.nomenclatura_default }}</p>
                <p><strong>Último número:</strong><br>{{ config.ultimo_numero }}</p>
                <p><strong>Próximo código:</strong><br>{{ config.nomenclatura_default }}{{ config.ultimo_numero|add:1|stringformat:"04d" }}</p>
                <a href="{% url 'configuracion_sistema' %}" class="btn btn-light btn-sm">Cambiar Configuración</a>
            </div>
        </div>
        <div class="card mt-3">
            <div class="card-body">
                <h6><i class="bi bi-info-circle"></i> Información</h6>
                <ul class="small">
                    <li>Las etiquetas se generan con fichas vacías</li>
                    <li>Se descargarán en formato PDF (A4)</li>
                    <li>4 etiquetas por página</li>
                    <li>Listas para imprimir y pegar</li>
                </ul>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    'templates/inventory_app/scan_qr.html': '''{% extends 'base.html' %}
{% block content %}
<h1><i class="bi bi-qr-code-scan"></i> Escanear Código QR</h1>
<div class="row justify-content-center mt-4">
    <div class="col-md-8">
        <div class="card">
            <div class="card-body">
                <div id="reader" style="width:100%;"></div>
                <hr>
                <form method="post">
                    {% csrf_token %}
                    <div class="mb-3">
                        <label class="form-label">O ingresa el código manualmente:</label>
                        <input type="text" class="form-control" name="codigo" placeholder="Ej: INV-0001" id="codigo">
                    </div>
                    <button type="submit" class="btn btn-primary w-100"><i class="bi bi-search"></i> Buscar</button>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
{% block extra_js %}
<script src="https://unpkg.com/html5-qrcode"></script>
<script>
function onScanSuccess(decodedText, decodedResult) {
    html5QrcodeScanner.clear();
    document.getElementById('codigo').value = decodedText;
    document.querySelector('form').submit();
}
var html5QrcodeScanner = new Html5QrcodeScanner("reader", { fps: 10, qrbox: 250 });
html5QrcodeScanner.render(onScanSuccess);
</script>
{% endblock %}''',

    'templates/inventory_app/completar_ficha.html': '''{% extends 'base.html' %}
{% block content %}
<h1><i class="bi bi-pencil-square"></i> Completar Ficha de Inventario</h1>
<h3 class="text-primary">{{ inventario.codigo_inventario }}</h3>
<div class="alert alert-info">
    <i class="bi bi-info-circle"></i>
    Esta ficha está vacía. Completa la información y añade una fotografía del activo.
</div>
<div class="card mt-3">
    <div class="card-body">
        <form method="post" enctype="multipart/form-data">
            {% csrf_token %}
            {{ form.as_p }}
            <hr>
            <button type="submit" class="btn btn-success btn-lg">
                <i class="bi bi-check-circle"></i> Completar y Guardar Ficha
            </button>
            <a href="{% url 'dashboard' %}" class="btn btn-secondary">Cancelar</a>
        </form>
    </div>
</div>
{% endblock %}''',

    'templates/inventory_app/inventario_list.html': '''{% extends 'base.html' %}
{% block content %}
<h1><i class="bi bi-list-ul"></i> Inventario</h1>
<div class="card mt-3">
    <div class="card-header">Búsqueda y Filtros</div>
    <div class="card-body">
        <form method="get">
            <div class="row">
                <div class="col-md-3">{{ form.q }}</div>
                <div class="col-md-2">{{ form.tipo_inventario }}</div>
                <div class="col-md-2">{{ form.ubicacion }}</div>
                <div class="col-md-2">{{ form.estado_ficha }}</div>
                <div class="col-md-2">{{ form.estado }}</div>
                <div class="col-md-1">
                    <button type="submit" class="btn btn-primary w-100">Buscar</button>
                </div>
            </div>
        </form>
    </div>
</div>
<div class="card mt-3">
    <div class="card-body">
        <table class="table">
            <thead>
                <tr>
                    <th>Código</th>
                    <th>Estado Ficha</th>
                    <th>Descripción</th>
                    <th>Tipo</th>
                    <th>Ubicación</th>
                    <th>Estado</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                {% for inv in inventarios %}
                <tr>
                    <td><strong>{{ inv.codigo_inventario }}</strong></td>
                    <td>{% if inv.estado_ficha == 'vacia' %}<span class="badge bg-warning">Vacía</span>{% else %}<span class="badge bg-success">Completada</span>{% endif %}</td>
                    <td>{{ inv.descripcion|default:"-"|truncatewords:10 }}</td>
                    <td>{{ inv.tipo_inventario|default:"-" }}</td>
                    <td>{{ inv.ubicacion|default:"-" }}</td>
                    <td>{{ inv.get_estado_display|default:"-" }}</td>
                    <td>
                        <a href="{% url 'inventario_detail' inv.pk %}" class="btn btn-sm btn-outline-primary"><i class="bi bi-eye"></i></a>
                        {% if inv.is_empty and user.can_edit %}
                        <a href="{% url 'completar_ficha' inv.codigo_inventario %}" class="btn btn-sm btn-outline-success"><i class="bi bi-pencil"></i></a>
                        {% endif %}
                    </td>
                </tr>
                {% empty %}
                <tr>
                    <td colspan="7" class="text-center text-muted">No se encontraron inventarios</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}''',

    'templates/inventory_app/inventario_detail.html': '''{% extends 'base.html' %}
{% block content %}
<div class="d-flex justify-content-between align-items-center">
    <h1><i class="bi bi-box-seam"></i> {{ inventario.codigo_inventario }}</h1>
    <div>
        {% if user.can_edit %}
        <a href="{% url 'inventario_edit' inventario.pk %}" class="btn btn-primary"><i class="bi bi-pencil"></i> Editar</a>
        {% endif %}
        {% if user.can_admin %}
        <form method="post" action="{% url 'inventario_delete' inventario.pk %}" style="display:inline;">
            {% csrf_token %}
            <button type="submit" class="btn btn-danger" onclick="return confirm('¿Eliminar?')"><i class="bi bi-trash"></i> Eliminar</button>
        </form>
        {% endif %}
    </div>
</div>
<div class="row mt-3">
    <div class="col-md-8">
        <div class="card">
            <div class="card-header">Información del Activo</div>
            <div class="card-body">
                <p><strong>Estado de Ficha:</strong> {% if inventario.estado_ficha == 'vacia' %}<span class="badge bg-warning">Vacía</span>{% else %}<span class="badge bg-success">Completada</span>{% endif %}</p>
                <p><strong>Descripción:</strong> {{ inventario.descripcion|default:"-" }}</p>
                <p><strong>Tipo:</strong> {{ inventario.tipo_inventario|default:"-" }}</p>
                <p><strong>Ubicación:</strong> {{ inventario.ubicacion|default:"-" }}</p>
                <p><strong>Estado:</strong> {{ inventario.get_estado_display|default:"-" }}</p>
                <p><strong>Fecha de Compra:</strong> {{ inventario.fecha_compra|date:"d/m/Y"|default:"-" }}</p>
                <p><strong>Creado por:</strong> {{ inventario.created_by|default:"-" }}</p>
                <p><strong>Fecha de creación:</strong> {{ inventario.created_at|date:"d/m/Y H:i" }}</p>
                {% if inventario.is_completed %}
                <p><strong>Completado por:</strong> {{ inventario.completed_by|default:"-" }}</p>
                <p><strong>Fecha de completado:</strong> {{ inventario.completed_at|date:"d/m/Y H:i"|default:"-" }}</p>
                {% endif %}
            </div>
        </div>
        {% if fotos %}
        <div class="card mt-3">
            <div class="card-header">Fotografías</div>
            <div class="card-body">
                <div class="row">
                    {% for foto in fotos %}
                    <div class="col-md-4 mb-3">
                        <img src="{{ foto.foto.url }}" class="img-fluid rounded" alt="Foto">
                        {% if foto.es_principal %}<span class="badge bg-primary">Principal</span>{% endif %}
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>
        {% endif %}
    </div>
    <div class="col-md-4">
        <div class="card">
            <div class="card-header">Código QR</div>
            <div class="card-body text-center">
                {% if inventario.qr_code %}
                <img src="{{ inventario.qr_code.url }}" alt="QR" class="img-fluid" style="max-width:200px;">
                {% else %}
                <p class="text-muted">QR no disponible</p>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    'templates/inventory_app/inventario_edit.html': '''{% extends 'base.html' %}
{% block content %}
<h1><i class="bi bi-pencil"></i> Editar Inventario</h1>
<h3 class="text-muted">{{ inventario.codigo_inventario }}</h3>
<div class="card mt-3">
    <div class="card-body">
        <form method="post">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit" class="btn btn-success">Guardar Cambios</button>
            <a href="{% url 'inventario_detail' inventario.pk %}" class="btn btn-secondary">Cancelar</a>
        </form>
    </div>
</div>
{% endblock %}''',

    'templates/inventory_app/tipo_inventario_list.html': '''{% extends 'base.html' %}
{% block content %}
<div class="d-flex justify-content-between align-items-center">
    <h1><i class="bi bi-tags"></i> Tipos de Inventario</h1>
    <a href="{% url 'tipo_inventario_create' %}" class="btn btn-primary"><i class="bi bi-plus"></i> Nuevo Tipo</a>
</div>
<div class="card mt-3">
    <div class="card-body">
        <table class="table">
            <thead>
                <tr><th>Nombre</th><th>Total</th><th>Estado</th><th>Acciones</th></tr>
            </thead>
            <tbody>
                {% for tipo in tipos %}
                <tr>
                    <td>{{ tipo.nombre }}</td>
                    <td><span class="badge bg-info">{{ tipo.total_inventarios }}</span></td>
                    <td>{% if tipo.activo %}<span class="badge bg-success">Activo</span>{% else %}<span class="badge bg-secondary">Inactivo</span>{% endif %}</td>
                    <td><a href="{% url 'tipo_inventario_edit' tipo.pk %}" class="btn btn-sm btn-outline-primary"><i class="bi bi-pencil"></i></a></td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}''',

    'templates/inventory_app/tipo_inventario_form.html': '''{% extends 'base.html' %}
{% block content %}
<h1>{{ action }} Tipo de Inventario</h1>
<div class="card mt-3">
    <div class="card-body">
        <form method="post">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit" class="btn btn-success">Guardar</button>
            <a href="{% url 'tipo_inventario_list' %}" class="btn btn-secondary">Cancelar</a>
        </form>
    </div>
</div>
{% endblock %}''',

    'templates/inventory_app/ubicacion_list.html': '''{% extends 'base.html' %}
{% block content %}
<div class="d-flex justify-content-between align-items-center">
    <h1><i class="bi bi-geo-alt"></i> Ubicaciones</h1>
    <a href="{% url 'ubicacion_create' %}" class="btn btn-primary"><i class="bi bi-plus"></i> Nueva Ubicación</a>
</div>
<div class="card mt-3">
    <div class="card-body">
        <table class="table">
            <thead>
                <tr><th>Nombre</th><th>Tipo</th><th>Edificio</th><th>Planta</th><th>Total</th><th>Estado</th><th>Acciones</th></tr>
            </thead>
            <tbody>
                {% for ubicacion in ubicaciones %}
                <tr>
                    <td>{{ ubicacion.nombre }}</td>
                    <td>{{ ubicacion.get_tipo_display }}</td>
                    <td>{{ ubicacion.edificio|default:"-" }}</td>
                    <td>{{ ubicacion.planta|default:"-" }}</td>
                    <td><span class="badge bg-info">{{ ubicacion.total_inventarios }}</span></td>
                    <td>{% if ubicacion.activo %}<span class="badge bg-success">Activo</span>{% else %}<span class="badge bg-secondary">Inactivo</span>{% endif %}</td>
                    <td><a href="{% url 'ubicacion_edit' ubicacion.pk %}" class="btn btn-sm btn-outline-primary"><i class="bi bi-pencil"></i></a></td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}''',

    'templates/inventory_app/ubicacion_form.html': '''{% extends 'base.html' %}
{% block content %}
<h1>{{ action }} Ubicación</h1>
<div class="card mt-3">
    <div class="card-body">
        <form method="post">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit" class="btn btn-success">Guardar</button>
            <a href="{% url 'ubicacion_list' %}" class="btn btn-secondary">Cancelar</a>
        </form>
    </div>
</div>
{% endblock %}''',

    'templates/inventory_app/configuracion_sistema.html': '''{% extends 'base.html' %}
{% block content %}
<h1><i class="bi bi-gear"></i> Configuración del Sistema</h1>
<div class="card mt-3">
    <div class="card-header">Nomenclatura de Etiquetas</div>
    <div class="card-body">
        <form method="post">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit" class="btn btn-success">Guardar Configuración</button>
        </form>
        <hr>
        <div class="alert alert-info">
            <strong>Ejemplo:</strong> Si la nomenclatura es "INV-" y los dígitos son 4, se generarán códigos como: INV-0001, INV-0002, INV-0003, etc.
        </div>
    </div>
</div>
{% endblock %}''',

    'templates/inventory_app/foto_form.html': '''{% extends 'base.html' %}
{% block content %}
<h1>Añadir Fotografía</h1>
<div class="card mt-3">
    <div class="card-body">
        <form method="post" enctype="multipart/form-data">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit" class="btn btn-success">Añadir Foto</button>
            <a href="{% url 'inventario_detail' inventario.pk %}" class="btn btn-secondary">Cancelar</a>
        </form>
    </div>
</div>
{% endblock %}''',
}

print("Creando templates de inventario...")
print("=" * 50)

for path, content in TEMPLATES.items():
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"OK: {path}")
    except Exception as e:
        print(f"ERROR: {path} - {e}")

print("=" * 50)
print("¡Todos los templates creados exitosamente!")
print("\n¡La aplicacion esta completa! Ahora:")
print("1. python manage.py makemigrations")
print("2. python manage.py migrate")
print("3. python manage.py createsuperuser")
print("4. python manage.py runserver")
