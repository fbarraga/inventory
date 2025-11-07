"""
Script para crear todos los templates HTML necesarios
Ejecutar con: python crear_templates.py
"""

import os
from pathlib import Path

# Crear directorios
os.makedirs('templates/users', exist_ok=True)
os.makedirs('templates/inventory_app', exist_ok=True)

# Definir contenido de cada template
TEMPLATES = {
    'templates/base.html': '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Sistema de Inventario{% endblock %} - Institut Sa Palomera</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; background: #f8fafc; }
        .navbar-custom { background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); }
        .card { border: none; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        .btn { border-radius: 8px; }
    </style>
    {% block extra_css %}{% endblock %}
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark navbar-custom">
        <div class="container">
            <a class="navbar-brand" href="{% url 'dashboard' %}">
                <i class="bi bi-box-seam"></i> Sistema Inventario
            </a>
            {% if user.is_authenticated %}
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link" href="{% url 'dashboard' %}"><i class="bi bi-speedometer2"></i> Dashboard</a></li>
                    <li class="nav-item"><a class="nav-link" href="{% url 'inventario_list' %}"><i class="bi bi-list-ul"></i> Inventario</a></li>
                    {% if user.can_edit %}
                    <li class="nav-item"><a class="nav-link" href="{% url 'generar_etiquetas' %}"><i class="bi bi-qr-code"></i> Generar Etiquetas</a></li>
                    {% endif %}
                    <li class="nav-item"><a class="nav-link" href="{% url 'scan_qr' %}"><i class="bi bi-qr-code-scan"></i> Escanear</a></li>
                    {% if user.can_admin %}
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown"><i class="bi bi-gear"></i> Admin</a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="{% url 'tipo_inventario_list' %}">Tipos</a></li>
                            <li><a class="dropdown-item" href="{% url 'ubicacion_list' %}">Ubicaciones</a></li>
                            <li><a class="dropdown-item" href="{% url 'user_list' %}">Usuarios</a></li>
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item" href="{% url 'configuracion_sistema' %}">Configuración</a></li>
                        </ul>
                    </li>
                    {% endif %}
                    <li class="nav-item"><a class="nav-link" href="{% url 'logout' %}"><i class="bi bi-box-arrow-right"></i> Salir</a></li>
                </ul>
            </div>
            {% endif %}
        </div>
    </nav>

    {% if messages %}
    <div class="container mt-3">
        {% for message in messages %}
        <div class="alert alert-{{ message.tags }} alert-dismissible fade show">
            {{ message }}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
        {% endfor %}
    </div>
    {% endif %}

    <div class="container my-4">
        {% block content %}{% endblock %}
    </div>

    <footer class="bg-white border-top py-3 mt-5">
        <div class="container text-center text-muted">
            <small>&copy; 2025 Institut Sa Palomera - Sistema de Inventario</small>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>''',

    'templates/users/login.html': '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Sistema de Inventario</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
    <style>
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; }
        .login-card { background: white; border-radius: 16px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); padding: 3rem; max-width: 450px; margin: auto; }
        .logo { width: 80px; height: 80px; margin: 0 auto 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 2rem; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <div class="login-card">
            <div class="text-center">
                <div class="logo"><i class="bi bi-box-seam"></i></div>
                <h1 class="h3">Bienvenido</h1>
                <p class="text-muted">Sistema de Inventario</p>
            </div>
            {% if messages %}
            {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">{{ message }}</div>
            {% endfor %}
            {% endif %}
            <form method="post" class="mt-4">
                {% csrf_token %}
                <div class="mb-3">
                    <label class="form-label">Usuario</label>
                    <input type="text" class="form-control" name="username" required autofocus>
                </div>
                <div class="mb-3">
                    <label class="form-label">Contraseña</label>
                    <input type="password" class="form-control" name="password" required>
                </div>
                <button type="submit" class="btn btn-primary w-100">Iniciar Sesión</button>
            </form>
            <div class="text-center mt-3">
                <hr>
                <a href="{% url 'social:begin' 'google-oauth2' %}" class="btn btn-outline-secondary w-100">
                    <i class="bi bi-google"></i> Iniciar con Google
                </a>
            </div>
        </div>
    </div>
</body>
</html>''',

    'templates/users/profile.html': '''{% extends 'base.html' %}
{% block content %}
<h1><i class="bi bi-person-circle"></i> Mi Perfil</h1>
<div class="card mt-3">
    <div class="card-body">
        <p><strong>Usuario:</strong> {{ user.username }}</p>
        <p><strong>Nombre:</strong> {{ user.first_name }} {{ user.last_name }}</p>
        <p><strong>Email:</strong> {{ user.email }}</p>
        <p><strong>Rol:</strong> <span class="badge bg-primary">{{ user.get_role_display }}</span></p>
        <p><strong>Tipo de cuenta:</strong> {% if user.is_google_user %}<span class="badge bg-info">Google</span>{% else %}<span class="badge bg-secondary">Local</span>{% endif %}</p>
    </div>
</div>
{% endblock %}''',

    'templates/users/user_list.html': '''{% extends 'base.html' %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-3">
    <h1><i class="bi bi-people"></i> Gestión de Usuarios</h1>
    <a href="{% url 'user_create' %}" class="btn btn-primary"><i class="bi bi-plus-circle"></i> Nuevo Usuario</a>
</div>
<div class="card">
    <div class="card-body">
        <table class="table">
            <thead>
                <tr>
                    <th>Usuario</th>
                    <th>Nombre</th>
                    <th>Email</th>
                    <th>Rol</th>
                    <th>Estado</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                {% for user in users %}
                <tr>
                    <td>{{ user.username }}</td>
                    <td>{{ user.first_name }} {{ user.last_name }}</td>
                    <td>{{ user.email }}</td>
                    <td><span class="badge bg-info">{{ user.get_role_display }}</span></td>
                    <td>{% if user.is_active %}<span class="badge bg-success">Activo</span>{% else %}<span class="badge bg-secondary">Inactivo</span>{% endif %}</td>
                    <td>
                        <a href="{% url 'user_edit' user.pk %}" class="btn btn-sm btn-outline-primary"><i class="bi bi-pencil"></i></a>
                        <form method="post" action="{% url 'user_delete' user.pk %}" style="display:inline;">
                            {% csrf_token %}
                            <button type="submit" class="btn btn-sm btn-outline-danger" onclick="return confirm('¿Eliminar este usuario?')"><i class="bi bi-trash"></i></button>
                        </form>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}''',

    'templates/users/user_form.html': '''{% extends 'base.html' %}
{% block content %}
<h1><i class="bi bi-person"></i> {{ action }} Usuario</h1>
<div class="card mt-3">
    <div class="card-body">
        <form method="post">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit" class="btn btn-success">Guardar</button>
            <a href="{% url 'user_list' %}" class="btn btn-secondary">Cancelar</a>
        </form>
    </div>
</div>
{% endblock %}''',
}

print("Creando templates...")
print("=" * 50)

for path, content in TEMPLATES.items():
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"OK: {path}")
    except Exception as e:
        print(f"ERROR: {path} - {e}")

print("=" * 50)
print("Templates base creados exitosamente!")
print("\nAhora ejecuta:")
print("1. python manage.py makemigrations")
print("2. python manage.py migrate")
print("3. python manage.py createsuperuser")
print("4. python manage.py runserver")
