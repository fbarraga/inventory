# Sistema de Gestió d'Inventari - Institut Sa Palomera

Sistema modern de gestió d'inventari amb Django 5.1, generació d'etiquetes QR en lot, i disseny responsive mobile-first.

## Característiques Principals

### Flux de Treball Optimitzat

1. **Generació massiva d'etiquetes QR** amb nomenclatura configurable
2. **Impressió en PDF** d'etiquetes en lot
3. **Etiquetatge físic** d'actius
4. **Escaneig QR** des de mòbil o PC
5. **Completar informació** amb fotografia i dades
6. **Gestió completa** d'inventari

### Sistema d'Usuaris

- **Autenticació local** amb usuari/contrasenya
- **Login amb Google OAuth** per a comptes corporatius
- **Tres nivells de permisos**:
  - **Consulta**: Veure inventari
  - **Inserció**: Crear i modificar
  - **Administrador**: Control total

### Gestió d'Inventari

- Codi únic automàtic amb nomenclatura personalitzable
- Suport per a fitxes buides (pre-generades)
- Fotografies múltiples per actiu
- Tipus configurables (ordinador, taula, cadira, etc.)
- Ubicacions organitzades (aules, armaris, etc.)
- 4 camps lliures per a integració comptable
- Historial complet de canvis
- Cerca avançada i filtres

### QR i Etiquetes

- Generació en lot amb nomenclatura definible
- PDF optimitzat per a impressió (4 etiquetes per full A4)
- Escaneig amb càmera des de mòbil
- Cerca manual per codi

### Disseny Modern

- Interfície responsive mobile-first
- Bootstrap 5 amb disseny tecnològic
- Compatible amb smartphones i tablets
- Optimitzat per a ús al camp

## Requisits

- Python 3.10 o superior
- pip (gestor de paquets de Python)

## Instal·lació

### 1. Preparar l'entorn

```bash
# Navegar al directori del projecte


# Crear entorn virtual
python -m venv venv

# Activar entorn virtual (Windows)
venv\Scripts\activate

# Activar entorn virtual (Linux/Mac)
source venv/bin/activate
```

### 2. Instal·lar dependències

```bash
pip install -r requirements.txt
```

### 3. Configurar variables d'entorn

```bash
# Copiar arxiu d'exemple
copy .env.example .env

# Editar .env amb els teus valors
notepad .env
```

Contingut mínim de l'arxiu `.env`:

```
SECRET_KEY=la-teva-clau-secreta-molt-segura-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Google OAuth (opcional - deixar buit si no s'utilitza)
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=
```

### 4. Crear directoris per als arxius

```bash
mkdir media
mkdir media\qr_codes
mkdir media\inventario_fotos
mkdir static
```

### 5. Inicialitzar base de dades

```bash
# Crear migracions
python manage.py makemigrations

# Aplicar migracions
python manage.py migrate
```

### 6. Crear superusuari

```bash
python manage.py createsuperuser
```

Segueix les instruccions per crear el teu usuari administrador.

### 7. Iniciar servidor

```bash
python manage.py runserver
```

Obre el teu navegador a: **http://localhost:8000**

## Guia d'Ús

### Configuració Inicial (Administrador)

1. **Login** amb el superusuari creat
2. **Configurar nomenclatura** (Configuració → Sistema)
   - Exemple: `INV-` generarà `INV-0001`, `INV-0002`, etc.
3. **Crear tipus d'inventari**
   - Ordinador, Taula, Cadira, Projector, etc.
4. **Crear ubicacions**
   - Aules (A101, A102, etc.)
   - Armaris (ARM-A, ARM-B, etc.)
   - Magatzems, Oficines, etc.
5. **Crear usuaris** i assignar rols

### Flux Complet d'Inventari

#### Pas 1: Generar Etiquetes QR

1. Anar a **"Generar Etiquetes QR"** al menú
2. Indicar quantitat d'etiquetes (ex: 50)
3. Opcionalment, utilitzar nomenclatura personalitzada
   - Exemple: `AULA-A-` per a actius de l'aula A
4. Click a **"Generar"**
5. Descarregar PDF automàticament
6. Imprimir etiquetes

#### Pas 2: Etiquetar Actius

1. Retallar les etiquetes impreses
2. Enganxar cada etiqueta a l'actiu corresponent

#### Pas 3: Completar Fitxes

**Des de mòbil o PC:**

1. Anar a **"Escanejar QR"**
2. Permetre accés a la càmera
3. Apuntar al codi QR de l'actiu
4. El sistema detecta automàticament si la fitxa està buida
5. Completar informació:
   - **Fotografia** (obligatòria)
   - **Descripció**
   - **Tipus d'inventari**
   - **Ubicació**
   - **Data de compra**
   - **Estat** (Disponible, En ús, etc.)
   - **Camps lliures** (opcional - per a comptabilitat)
6. Click a **"Guardar"**

Si el codi ja té informació, es mostrarà la fitxa completa.

#### Pas 4: Gestió Posterior

- **Cercar inventari**: Filtres per tipus, ubicació, estat
- **Veure detalls**: Fotografies, historial, ubicació
- **Editar**: Actualitzar informació (usuaris amb permís)
- **Afegir fotos**: Fotos addicionals de l'actiu
- **Historial**: Veure tots els canvis realitzats

### Permisos per Rol

| Acció | Consulta | Inserció | Administrador |
|--------|:--------:|:---------:|:-------------:|
| Veure inventari | Sí | Sí | Sí |
| Escanejar QR | Sí | Sí | Sí |
| Generar etiquetes | No | Sí | Sí |
| Completar fitxes | No | Sí | Sí |
| Editar inventari | No | Sí | Sí |
| Eliminar inventari | No | No | Sí |
| Gestionar tipus/ubicacions | No | No | Sí |
| Gestionar usuaris | No | No | Sí |
| Configurar sistema | No | No | Sí |

## Configuració de Google OAuth (Opcional)

Si vols permetre login amb comptes de Google de l'institut:

1. Anar a [Google Cloud Console](https://console.cloud.google.com/)
2. Crear nou projecte
3. Habilitar "Google+ API"
4. Crear credencials OAuth 2.0
5. Afegir URIs de redirecció:
   - `http://localhost:8000/auth/complete/google-oauth2/`
   - `https://teudomini.com/auth/complete/google-oauth2/` (producció)
6. Copiar Client ID i Client Secret
7. Afegir a l'arxiu `.env`:

```
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=el-teu-client-id-aqui
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=el-teu-client-secret-aqui
```

## Estructura del Projecte

```
inventory/
├── config/                     # Configuració Django
│   ├── settings.py            # Configuració principal
│   ├── urls.py                # URLs principals
│   ├── wsgi.py                # Servidor WSGI
│   └── asgi.py                # Servidor ASGI
├── users/                     # App d'usuaris
│   ├── models.py              # Model CustomUser amb rols
│   ├── views.py               # Autenticació i gestió
│   ├── forms.py               # Formularis d'usuari
│   ├── decorators.py          # Decoradors de permisos
│   ├── admin.py               # Admin d'usuaris
│   └── urls.py                # URLs d'usuaris
├── inventory_app/             # App principal d'inventari
│   ├── models.py              # Models (Inventari, Tipus, Ubicació, etc.)
│   ├── views.py               # Vistes principals
│   ├── forms.py               # Formularis
│   ├── admin.py               # Panell d'administració
│   └── urls.py                # URLs d'inventari
├── templates/                 # Plantilles HTML
│   ├── base.html              # Template base
│   ├── users/                 # Templates d'usuaris
│   └── inventory_app/         # Templates d'inventari
├── media/                     # Arxius pujats
│   ├── qr_codes/              # Codis QR generats
│   └── inventario_fotos/      # Fotografies d'actius
├── static/                    # Arxius estàtics
├── requirements.txt           # Dependències Python
├── manage.py                  # Script de gestió Django
├── .env.example               # Exemple de configuració
├── .gitignore                 # Arxius a ignorar en git
└── README.md                  # Aquest arxiu
```

## Dades de Prova

Per provar el sistema ràpidament:

```bash
# Crear tipus d'inventari de prova
python manage.py shell
```

```python
from inventory_app.models import TipoInventario, Ubicacion

# Crear tipus
TipoInventario.objects.create(nombre="Ordenador", descripcion="Equipos informáticos")
TipoInventario.objects.create(nombre="Mesa", descripcion="Mobiliario - Mesas")
TipoInventario.objects.create(nombre="Silla", descripcion="Mobiliario - Sillas")
TipoInventario.objects.create(nombre="Proyector", descripcion="Equipos audiovisuales")

# Crear ubicacions
Ubicacion.objects.create(nombre="Aula A-101", tipo="aula", edificio="Edificio A", planta="1")
Ubicacion.objects.create(nombre="Aula A-102", tipo="aula", edificio="Edificio A", planta="1")
Ubicacion.objects.create(nombre="Armario Principal", tipo="armario", edificio="Edificio A")
Ubicacion.objects.create(nombre="Almacén General", tipo="almacen")

print("Dades de prova creades")
```

## Desplegament en Producció

Abans de desplegar en producció:

1. **Canviar SECRET_KEY** a un valor aleatori segur
2. **Establir DEBUG=False**
3. **Configurar ALLOWED_HOSTS** amb el teu domini
4. **Utilitzar base de dades PostgreSQL/MySQL** (opcional)
5. **Configurar servidor web** (Nginx + Gunicorn)
6. **Habilitar HTTPS**
7. **Configurar còpies de seguretat** de la base de dades

## Suport

Per a dubtes o problemes:

- **Institut**: Institut Sa Palomera
- **Web**: https://www.sapalomera.cat
- **Documentació Django**: https://docs.djangoproject.com/es/5.1/

## Llicència

Copyright © 2025 Institut Sa Palomera. Tots els drets reservats.

---

**Desenvolupat per a l'Institut Sa Palomera**
