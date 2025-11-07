# Sistema de Gestión de Inventario - Institut Sa Palomera

Sistema moderno de gestión de inventario con Django 5.1, generación de etiquetas QR en lote, y diseño responsive mobile-first.

## 🚀 Características Principales

### ✅ Flujo de Trabajo Optimizado

1. **Generación masiva de etiquetas QR** con nomenclatura configurable
2. **Impresión en PDF** de etiquetas en lote
3. **Etiquetado físico** de activos
4. **Escaneo QR** desde móvil o PC
5. **Completar información** con fotografía y datos
6. **Gestión completa** de inventario

### 👥 Sistema de Usuarios

- **Autenticación local** con usuario/contraseña
- **Login con Google OAuth** para cuentas corporativas
- **Tres niveles de permisos**:
  - 🔍 **Consulta**: Ver inventario
  - ✏️ **Inserción**: Crear y modificar
  - 👑 **Administrador**: Control total

### 📦 Gestión de Inventario

- Código único automático con nomenclatura personalizable
- Soporte para fichas vacías (pre-generadas)
- Fotografías múltiples por activo
- Tipos configurables (ordenador, mesa, silla, etc.)
- Ubicaciones organizadas (aulas, armarios, etc.)
- 4 campos libres para integración contable
- Historial completo de cambios
- Búsqueda avanzada y filtros

### 📱 QR y Etiquetas

- Generación en lote con nomenclatura definible
- PDF optimizado para impresión (4 etiquetas por hoja A4)
- Escaneo con cámara desde móvil
- Búsqueda manual por código

### 🎨 Diseño Moderno

- Interfaz responsive mobile-first
- Bootstrap 5 con diseño tecnológico
- Compatible con smartphones y tablets
- Optimizado para uso en campo

## 📋 Requisitos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)

## 🛠️ Instalación

### 1. Preparar el entorno

```bash
# Navegar al directorio del proyecto
cd e:\OneDrive\Desarrollos\Codeworks\inventory

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
venv\Scripts\activate

# Activar entorno virtual (Linux/Mac)
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

```bash
# Copiar archivo de ejemplo
copy .env.example .env

# Editar .env con tus valores
notepad .env
```

Contenido mínimo del archivo `.env`:

```
SECRET_KEY=tu-clave-secreta-muy-segura-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Google OAuth (opcional - dejar vacío si no se usa)
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=
```

### 4. Crear directorios para archivos

```bash
mkdir media
mkdir media\qr_codes
mkdir media\inventario_fotos
mkdir static
```

### 5. Inicializar base de datos

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate
```

### 6. Crear superusuario

```bash
python manage.py createsuperuser
```

Sigue las instrucciones para crear tu usuario administrador.

### 7. Iniciar servidor

```bash
python manage.py runserver
```

Abre tu navegador en: **http://localhost:8000**

## 📖 Guía de Uso

### Configuración Inicial (Administrador)

1. **Login** con el superusuario creado
2. **Configurar nomenclatura** (Configuración → Sistema)
   - Ejemplo: `INV-` generará `INV-0001`, `INV-0002`, etc.
3. **Crear tipos de inventario**
   - Ordenador, Mesa, Silla, Proyector, etc.
4. **Crear ubicaciones**
   - Aulas (A101, A102, etc.)
   - Armarios (ARM-A, ARM-B, etc.)
   - Almacenes, Oficinas, etc.
5. **Crear usuarios** y asignar roles

### Flujo Completo de Inventario

#### Paso 1: Generar Etiquetas QR

1. Ir a **"Generar Etiquetas QR"** en el menú
2. Indicar cantidad de etiquetas (ej: 50)
3. Opcionalmente, usar nomenclatura personalizada
   - Ejemplo: `AULA-A-` para activos del aula A
4. Click en **"Generar"**
5. Descargar PDF automáticamente
6. Imprimir etiquetas

#### Paso 2: Etiquetar Activos

1. Recortar las etiquetas impresas
2. Pegar cada etiqueta en el activo correspondiente

#### Paso 3: Completar Fichas

**Desde móvil o PC:**

1. Ir a **"Escanear QR"**
2. Permitir acceso a la cámara
3. Apuntar al código QR del activo
4. El sistema detecta automáticamente si la ficha está vacía
5. Completar información:
   - 📸 **Fotografía** (obligatoria)
   - 📝 **Descripción**
   - 🏷️ **Tipo de inventario**
   - 📍 **Ubicación**
   - 📅 **Fecha de compra**
   - 📊 **Estado** (Disponible, En uso, etc.)
   - 💼 **Campos libres** (opcional - para contabilidad)
6. Click en **"Guardar"**

Si el código ya tiene información, se mostrará la ficha completa.

#### Paso 4: Gestión Posterior

- **Buscar inventario**: Filtros por tipo, ubicación, estado
- **Ver detalles**: Fotografías, historial, ubicación
- **Editar**: Actualizar información (usuarios con permiso)
- **Añadir fotos**: Fotos adicionales del activo
- **Historial**: Ver todos los cambios realizados

### Permisos por Rol

| Acción | Consulta | Inserción | Administrador |
|--------|:--------:|:---------:|:-------------:|
| Ver inventario | ✅ | ✅ | ✅ |
| Escanear QR | ✅ | ✅ | ✅ |
| Generar etiquetas | ❌ | ✅ | ✅ |
| Completar fichas | ❌ | ✅ | ✅ |
| Editar inventario | ❌ | ✅ | ✅ |
| Eliminar inventario | ❌ | ❌ | ✅ |
| Gestionar tipos/ubicaciones | ❌ | ❌ | ✅ |
| Gestionar usuarios | ❌ | ❌ | ✅ |
| Configurar sistema | ❌ | ❌ | ✅ |

## 🔧 Configuración de Google OAuth (Opcional)

Si deseas permitir login con cuentas de Google del instituto:

1. Ir a [Google Cloud Console](https://console.cloud.google.com/)
2. Crear nuevo proyecto
3. Habilitar "Google+ API"
4. Crear credenciales OAuth 2.0
5. Añadir URIs de redirección:
   - `http://localhost:8000/auth/complete/google-oauth2/`
   - `https://tudominio.com/auth/complete/google-oauth2/` (producción)
6. Copiar Client ID y Client Secret
7. Añadir al archivo `.env`:

```
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=tu-client-id-aqui
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=tu-client-secret-aqui
```

## 📁 Estructura del Proyecto

```
inventory/
├── config/                     # Configuración Django
│   ├── settings.py            # Configuración principal
│   ├── urls.py                # URLs principales
│   ├── wsgi.py                # Servidor WSGI
│   └── asgi.py                # Servidor ASGI
├── users/                     # App de usuarios
│   ├── models.py              # Modelo CustomUser con roles
│   ├── views.py               # Autenticación y gestión
│   ├── forms.py               # Formularios de usuario
│   ├── decorators.py          # Decoradores de permisos
│   ├── admin.py               # Admin de usuarios
│   └── urls.py                # URLs de usuarios
├── inventory_app/             # App principal de inventario
│   ├── models.py              # Modelos (Inventario, Tipo, Ubicación, etc.)
│   ├── views.py               # Vistas principales
│   ├── forms.py               # Formularios
│   ├── admin.py               # Panel de administración
│   └── urls.py                # URLs de inventario
├── templates/                 # Plantillas HTML
│   ├── base.html              # Template base
│   ├── users/                 # Templates de usuarios
│   └── inventory_app/         # Templates de inventario
├── media/                     # Archivos subidos
│   ├── qr_codes/              # Códigos QR generados
│   └── inventario_fotos/      # Fotografías de activos
├── static/                    # Archivos estáticos
├── requirements.txt           # Dependencias Python
├── manage.py                  # Script de gestión Django
├── .env.example               # Ejemplo de configuración
├── .gitignore                 # Archivos a ignorar en git
└── README.md                  # Este archivo
```

## 🧪 Datos de Prueba

Para probar el sistema rápidamente:

```bash
# Crear tipos de inventario de prueba
python manage.py shell
```

```python
from inventory_app.models import TipoInventario, Ubicacion

# Crear tipos
TipoInventario.objects.create(nombre="Ordenador", descripcion="Equipos informáticos")
TipoInventario.objects.create(nombre="Mesa", descripcion="Mobiliario - Mesas")
TipoInventario.objects.create(nombre="Silla", descripcion="Mobiliario - Sillas")
TipoInventario.objects.create(nombre="Proyector", descripcion="Equipos audiovisuales")

# Crear ubicaciones
Ubicacion.objects.create(nombre="Aula A-101", tipo="aula", edificio="Edificio A", planta="1")
Ubicacion.objects.create(nombre="Aula A-102", tipo="aula", edificio="Edificio A", planta="1")
Ubicacion.objects.create(nombre="Armario Principal", tipo="armario", edificio="Edificio A")
Ubicacion.objects.create(nombre="Almacén General", tipo="almacen")

print("✓ Datos de prueba creados")
```

## 🚀 Despliegue en Producción

Antes de desplegar en producción:

1. **Cambiar SECRET_KEY** a un valor aleatorio seguro
2. **Establecer DEBUG=False**
3. **Configurar ALLOWED_HOSTS** con tu dominio
4. **Usar base de datos PostgreSQL/MySQL** (opcional)
5. **Configurar servidor web** (Nginx + Gunicorn)
6. **Habilitar HTTPS**
7. **Configurar copias de seguridad** de la base de datos

## 📞 Soporte

Para dudas o problemas:

- **Instituto**: Institut Sa Palomera
- **Web**: https://www.sapalomera.cat
- **Documentación Django**: https://docs.djangoproject.com/es/5.1/

## 📄 Licencia

Copyright © 2025 Institut Sa Palomera. Todos los derechos reservados.

---

**Desarrollado con ❤️ para Institut Sa Palomera**
