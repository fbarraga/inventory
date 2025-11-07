"""
Script para traducir templates HTML del español al catalán
"""

import os
import re

# Diccionario de traducciones
TRADUCCIONES = {
    # Títulos y navegación
    'Dashboard': 'Tauler',
    'Sistema de Inventario': "Sistema d'Inventari",
    'Sistema Inventario': 'Sistema Inventari',
    'Inventario': 'Inventari',
    'Generar Etiquetas': 'Generar Etiquetes',
    'Escanear': 'Escanejar',
    'Escanear QR': 'Escanejar QR',
    'Admin': 'Admin',
    'Tipos': 'Tipus',
    'Ubicaciones': 'Ubicacions',
    'Usuarios': 'Usuaris',
    'Configuración': 'Configuració',
    'Salir': 'Sortir',

    # Botones y acciones
    'Crear': 'Crear',
    'Nuevo': 'Nou',
    'Nueva': 'Nova',
    'Editar': 'Editar',
    'Eliminar': 'Eliminar',
    'Guardar': 'Desar',
    'Cancelar': 'Cancel·lar',
    'Buscar': 'Cercar',
    'Ver': 'Veure',
    'Ver Todos': 'Veure Tots',
    'Ver Todas': 'Veure Totes',
    'Añadir': 'Afegir',
    'Descargar': 'Descarregar',
    'Imprimir': 'Imprimir',

    # Estados
    'Activo': 'Actiu',
    'Inactivo': 'Inactiu',
    'Disponible': 'Disponible',
    'En Uso': 'En Ús',
    'En uso': 'en ús',
    'Mantenimiento': 'Manteniment',
    'Estado': 'Estat',

    # Formularios
    'Nombre': 'Nom',
    'Descripción': 'Descripció',
    'Tipo': 'Tipus',
    'Ubicación': 'Ubicació',
    'Fecha': 'Data',
    'Fecha de Compra': 'Data de Compra',
    'Código': 'Codi',
    'Código de Inventario': "Codi d'Inventari",
    'Fotografía': 'Fotografia',
    'Fotografías': 'Fotografies',

    # Listas y tablas
    'Total': 'Total',
    'Acciones': 'Accions',
    'Últimos': 'Últims',
    'Últimas': 'Últimes',
    'Todos': 'Tots',
    'Todas': 'Totes',

    # Tipos de ubicación
    'Aula': 'Aula',
    'Armario': 'Armari',
    'Almacén': 'Magatzem',
    'Oficina': 'Oficina',
    'Laboratorio': 'Laboratori',
    'Otro': 'Altre',
    'Edificio': 'Edifici',
    'Planta': 'Planta',

    # Ficha
    'Ficha Vacía': 'Fitxa Buida',
    'Ficha Completada': 'Fitxa Completada',
    'Completar': 'Completar',
    'Completado': 'Completat',
    'Completada': 'Completada',

    # Etiquetas
    'Etiquetas': 'Etiquetes',
    'Generar y Descargar PDF': 'Generar i Descarregar PDF',
    'Cantidad': 'Quantitat',
    'Cantidad de Etiquetas': "Quantitat d'Etiquetes",

    # Información
    'Información': 'Informació',
    'Información Básica': 'Informació Bàsica',
    'Información del Activo': "Informació de l'Actiu",
    'Esta ficha está vacía': 'Aquesta fitxa està buida',
    'Esta ficha ya está completada': 'Aquesta fitxa ja està completada',

    # Perfil y usuario
    'Mi Perfil': 'El Meu Perfil',
    'Usuario': 'Usuari',
    'Email': 'Correu electrònic',
    'Rol': 'Rol',
    'Contraseña': 'Contrasenya',

    # Mensajes
    'creado exitosamente': 'creat correctament',
    'actualizado exitosamente': 'actualitzat correctament',
    'eliminado exitosamente': 'eliminat correctament',
    'guardado correctamente': 'desat correctament',
    'No hay': 'No hi ha',
    'No se encontró': "No s'ha trobat",
    'No tienes permisos': 'No tens permisos',

    # Configuración del sistema
    'Configuración del Sistema': 'Configuració del Sistema',
    'Nomenclatura': 'Nomenclatura',
    'Nomenclatura por Defecto': 'Nomenclatura per Defecte',
    'Etiquetas por Fila': 'Etiquetes per Fila',
    'Etiquetas por Columna': 'Etiquetes per Columna',
    'Configuración Actual': 'Configuració Actual',
    'Próximo código': 'Proper codi',

    # Estadísticas
    'Total de Activos': "Total d'Actius",
    'Fichas Vacías': 'Fitxes Buides',
    'Fichas Completadas': 'Fitxes Completades',
    'Distribución por Tipo': 'Distribució per Tipus',
    'Distribución por Ubicación': 'Distribució per Ubicació',
    'Últimos Inventarios Añadidos': 'Últims Inventaris Afegits',
    'Últimos Inventarios': 'Últims Inventaris',
    'Resumen del sistema': 'Resum del sistema',

    # Búsqueda
    'Búsqueda y Filtros': 'Cerca i Filtres',
    'Buscar por código, descripción...': 'Cercar per codi, descripció...',
    'Todos los tipos': 'Tots els tipus',
    'Todas las ubicaciones': 'Totes les ubicacions',
    'Todos los estados': 'Tots els estats',

    # Detalles
    'Detalle': 'Detall',
    'Detalles': 'Detalls',
    'Historial': 'Historial',
    'Historial de cambios': 'Historial de canvis',
    'Creado por': 'Creat per',
    'Fecha de creación': 'Data de creació',
    'Última actualización': 'Última actualització',
    'Completado por': 'Completat per',

    # Instrucciones
    'Instrucciones': 'Instruccions',
    'Ejemplo': 'Exemple',
    'Importante': 'Important',
    'Nota': 'Nota',

    # Campos libres
    'Campo Libre 1': 'Camp Lliure 1',
    'Campo Libre 2': 'Camp Lliure 2',
    'Campo Libre 3': 'Camp Lliure 3',
    'Campo Libre 4': 'Camp Lliure 4',
    'Campos Libres': 'Camps Lliures',

    # Gestión de usuarios
    'Gestión de Usuarios': "Gestió d'Usuaris",
    'Nuevo Usuario': 'Nou Usuari',
    'Crear Usuario': 'Crear Usuari',
    'Lista de usuarios': "Llista d'usuaris",

    # General
    'Sí': 'Sí',
    'No': 'No',
    'O ingresa el código manualmente': 'O introdueix el codi manualment',
    'Formulario de Generación': 'Formulari de Generació',

    # HTML específico (más seguro)
    'lang="es"': 'lang="ca"',
}

def traducir_archivo(ruta_archivo):
    """Traduce un archivo HTML"""
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()

        contenido_original = contenido

        # Aplicar traducciones
        for esp, cat in TRADUCCIONES.items():
            # Buscar exacto (palabra completa)
            contenido = re.sub(
                r'\b' + re.escape(esp) + r'\b',
                cat,
                contenido,
                flags=re.MULTILINE
            )

        # Si hubo cambios, guardar
        if contenido != contenido_original:
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                f.write(contenido)
            return True
        return False

    except Exception as e:
        print(f"Error en {ruta_archivo}: {e}")
        return False

# Procesar todos los templates
templates_dir = 'templates'
total = 0
traducidos = 0

print("Traduciendo templates HTML al catalán...")
print("=" * 60)

for root, dirs, files in os.walk(templates_dir):
    for file in files:
        if file.endswith('.html'):
            ruta = os.path.join(root, file)
            total += 1
            if traducir_archivo(ruta):
                traducidos += 1
                print(f"[OK] {ruta}")
            else:
                print(f"[--] {ruta} (sin cambios)")

print("=" * 60)
print(f"Procesados: {total} archivos")
print(f"Traducidos: {traducidos} archivos")
print(f"Sin cambios: {total - traducidos} archivos")
print("\nTraduccion completada!")
