"""
Script para traducir textos clave al catalán
"""

# Diccionario de traducciones español -> catalán
TRADUCCIONES = {
    # Común
    'Usuario': 'Usuari',
    'Usuarios': 'Usuaris',
    'Email': 'Correu electrònic',
    'Contraseña': 'Contrasenya',
    'Nombre': 'Nom',
    'Descripción': 'Descripció',
    'Activo': 'Actiu',
    'Inactivo': 'Inactiu',
    'Estado': 'Estat',
    'Fecha': 'Data',
    'Acciones': 'Accions',
    'Buscar': 'Cercar',
    'Guardar': 'Desar',
    'Cancelar': 'Cancel·lar',
    'Editar': 'Editar',
    'Eliminar': 'Eliminar',
    'Crear': 'Crear',
    'Ver': 'Veure',
    'Todos': 'Tots',
    'Sí': 'Sí',
    'No': 'No',

    # Sistema
    'Sistema de Inventario': 'Sistema d\'Inventari',
    'Dashboard': 'Tauler',
    'Configuración': 'Configuració',

    # Inventario
    'Inventario': 'Inventari',
    'Código de Inventario': 'Codi d\'Inventari',
    'Tipo de Inventario': 'Tipus d\'Inventari',
    'Tipos de Inventario': 'Tipus d\'Inventari',
    'Ubicación': 'Ubicació',
    'Ubicaciones': 'Ubicacions',
    'Fecha de Compra': 'Data de Compra',
    'Fotografía': 'Fotografia',
    'Fotografías': 'Fotografies',
    'Ficha Vacía': 'Fitxa Buida',
    'Ficha Completada': 'Fitxa Completada',
    'Completar': 'Completar',
    'Generar Etiquetas': 'Generar Etiquetes',
    'Escanear QR': 'Escanejar QR',
    'Código QR': 'Codi QR',

    # Estados
    'Disponible': 'Disponible',
    'En Uso': 'En Ús',
    'En uso': 'En ús',
    'Mantenimiento': 'Manteniment',
    'Dado de Baja': 'Donat de Baixa',
    'Extraviado': 'Extraviat',

    # Tipos
    'Ordenador': 'Ordinador',
    'Mesa': 'Taula',
    'Silla': 'Cadira',
    'Proyector': 'Projector',
    'Aula': 'Aula',
    'Armario': 'Armari',
    'Almacén': 'Magatzem',
    'Oficina': 'Oficina',
    'Laboratorio': 'Laboratori',
    'Otro': 'Altre',

    # Roles
    'Consulta': 'Consulta',
    'Inserción de Datos': 'Inserció de Dades',
    'Administrador': 'Administrador',

    # Mensajes
    'creado exitosamente': 'creat correctament',
    'actualizado exitosamente': 'actualitzat correctament',
    'eliminado exitosamente': 'eliminat correctament',
    'guardado correctamente': 'desat correctament',
    'Error': 'Error',
    'Éxito': 'Èxit',
    'Información': 'Informació',
    'Advertencia': 'Advertència',
}

print("Diccionario de traducciones cargado:")
print(f"Total de traducciones: {len(TRADUCCIONES)}")
print("\nAlgunas traducciones clave:")
for es, ca in list(TRADUCCIONES.items())[:10]:
    print(f"  {es} → {ca}")
