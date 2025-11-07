"""
Script complementario para traducir frases que faltaban en la primera pasada
"""
import os
import re

# Traducciones adicionales que faltaban
TRADUCCIONES_ADICIONALES = {
    # Frases completas que faltaron
    'No hay inventarios registrados': "No hi ha inventaris registrats",
    'inventarios registrados': 'inventaris registrats',
    'Las etiquetas se generan con fichas vacías': 'Les etiquetes es generen amb fitxes buides',
    'Se descargarán en formato PDF': 'Es descarregaran en format PDF',
    'etiquetas por página': 'etiquetes per pàgina',
    'Listas para imprimir y pegar': 'Llistes per imprimir i enganxar',
    'Cambiar Configuración': 'Canviar Configuració',
    'Cambiar': 'Canviar',
    'Último número': 'Últim número',
    'Últimos Inventarios': 'Últims Inventaris',
    'Últimos': 'Últims',
    'Vacía': 'Buida',
    'Completada': 'Completada',
    'registrados': 'registrats',
    'Generar y Descargar PDF': 'Generar i Descarregar PDF',

    # Estado en badges
    'Vacía': 'Buida',

    # Información
    'Información': 'Informació',
}

def traducir_archivo(ruta_archivo):
    """Traduce un archivo HTML con las traducciones adicionales"""
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()

        contenido_original = contenido

        # Aplicar traducciones
        for esp, cat in TRADUCCIONES_ADICIONALES.items():
            # Para frases completas, buscar exacto
            contenido = contenido.replace(esp, cat)

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

print("Traduciendo frases faltantes...")
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
print("\nTraduccion de frases faltantes completada!")
