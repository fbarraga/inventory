# 🚀 Inicio Rápido - 5 Minutos

Esta guía te permite tener el sistema funcionando en menos de 5 minutos.

## Requisitos Previos

- Python 3.10 o superior instalado
- Conexión a Internet (para descargar dependencias)

## Pasos de Instalación

### 1. Abrir terminal en la carpeta del proyecto

```bash
cd e:\OneDrive\Desarrollos\Codeworks\inventory
```

### 2. Crear y activar entorno virtual

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar entorno

```bash
copy .env.example .env
```

### 5. Crear directorios

```bash
mkdir media
mkdir media\qr_codes
mkdir media\inventario_fotos
mkdir static
```

### 6. Inicializar base de datos

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Crear superusuario

```bash
python manage.py createsuperuser
```

Ejemplo:
- **Username**: admin
- **Email**: admin@sapalomera.cat
- **Password**: (tu contraseña segura)

### 8. ¡Iniciar servidor!

```bash
python manage.py runserver
```

### 9. Abrir en navegador

Ir a: **http://localhost:8000**

## ✅ Primer Uso

### 1. Login

- Usuario: admin (o el que creaste)
- Contraseña: (la que definiste)

### 2. Configurar el Sistema

**a) Crear Tipos de Inventario** (Admin → Tipos de Inventario → Crear)

Ejemplos:
- Ordenador
- Mesa
- Silla
- Proyector
- Pizarra

**b) Crear Ubicaciones** (Admin → Ubicaciones → Crear)

Ejemplos:
- Aula A-101 (tipo: Aula, Edificio: A, Planta: 1)
- Aula A-102 (tipo: Aula, Edificio: A, Planta: 1)
- Armario A (tipo: Armario)
- Almacén Principal (tipo: Almacén)

### 3. Generar Etiquetas de Prueba

1. Ir a **"Generar Etiquetas QR"**
2. Cantidad: **10**
3. Click en **"Generar"**
4. Se descarga automáticamente el PDF
5. Imprimir PDF

### 4. Probar Escaneo

1. Desde móvil o PC, ir a **"Escanear QR"**
2. Escanear una etiqueta impresa (o ingresar código manualmente: `INV-0001`)
3. Completar información:
   - Subir una foto
   - Descripción: "Ordenador portátil HP"
   - Tipo: Ordenador
   - Ubicación: Aula A-101
   - Fecha de compra: (seleccionar fecha)
4. **Guardar**

### 5. Ver Inventario

- Ir a **"Inventario"**
- Ver lista completa
- Click en código para ver detalle

## 🎯 Resumen del Flujo

```
1. GENERAR ETIQUETAS QR
   ↓
2. IMPRIMIR PDF
   ↓
3. PEGAR ETIQUETAS EN ACTIVOS
   ↓
4. ESCANEAR QR CON MÓVIL
   ↓
5. COMPLETAR INFORMACIÓN + FOTO
   ↓
6. ¡LISTO! Activo inventariado
```

## 🆘 Solución de Problemas

### Error: "Django no está instalado"
```bash
# Asegúrate de estar en el entorno virtual
venv\Scripts\activate
pip install -r requirements.txt
```

### Error: "No such table: users_customuser"
```bash
python manage.py makemigrations
python manage.py migrate
```

### Error al acceder a la cámara en móvil
- Asegúrate de dar permisos a la cámara
- Usa HTTPS en producción (HTTP solo funciona en localhost)

### No se generan los códigos QR
```bash
# Verificar que existe el directorio
mkdir media\qr_codes
```

## 📱 Uso desde Móvil

1. Asegúrate de que el PC y móvil están en la misma red
2. Averigua la IP del PC:
   ```bash
   ipconfig
   ```
3. En el móvil, acceder a: `http://[IP-DEL-PC]:8000`
   Ejemplo: `http://192.168.1.100:8000`

## 🔑 Credenciales por Defecto

**Usuario Admin**:
- Username: admin
- Password: (el que definiste al crear el superusuario)

**Roles disponibles**:
- Consulta: Solo ver
- Inserción: Ver y crear/editar
- Administrador: Control total

## 📞 ¿Necesitas Ayuda?

- Lee el README.md completo
- Revisa la documentación de Django: https://docs.djangoproject.com/es/
- Contacta al administrador del sistema

---

**¡Ya está todo listo! Comienza a inventariar 🎉**
