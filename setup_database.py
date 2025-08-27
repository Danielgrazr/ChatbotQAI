import sqlite3

# --- TUS DATOS ORGANIZADOS CON SUB-AREAS ---
AREAS = ["Moldeo", "Kinera"]

SUB_AREAS = {
    "Moldeo": ["Proceso", "Calidad"],
    "Kinera": ["Dragon Shield", "Otras Marcas"]
}

DEFECTOS = {
    "Alabeo": "Defecto donde la pieza se deforma o tuerce al enfriarse.",
    "Rebaba": "Exceso de material en los bordes de la pieza.",
    "Falta de filo": "El borde del escudo no tiene la agudeza requerida.",
    "Color incorrecto": "El tono del escudo no coincide con el estándar."
}

# --- RELACIONES (Qué defecto va en qué SUB-ÁREA) ---
RELACIONES = [
    ("Proceso", "Rebaba"),
    ("Calidad", "Alabeo"),
    ("Dragon Shield", "Color incorrecto"),
    ("Dragon Shield", "Falta de filo")
]

# --- CREACIÓN DE LA BASE DE DATOS ---
try:
    conn = sqlite3.connect('chatbot_db.sqlite')
    cursor = conn.cursor()
    print("Conectado a la base de datos.")

    # 1. Crear tabla de AREAS
    cursor.execute('CREATE TABLE IF NOT EXISTS areas (id_area INTEGER PRIMARY KEY, nombre_area TEXT NOT NULL UNIQUE)')
    print("Tabla 'areas' lista.")

    # 2. (NUEVA) Crear tabla de SUB_AREAS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sub_areas (
            id_sub_area INTEGER PRIMARY KEY,
            nombre_sub_area TEXT NOT NULL UNIQUE,
            id_area INTEGER,
            FOREIGN KEY (id_area) REFERENCES areas (id_area)
        )
    ''')
    print("Tabla 'sub_areas' lista.")

    # 3. Crear tabla de DEFECTOS
    cursor.execute('CREATE TABLE IF NOT EXISTS defectos (id_defecto INTEGER PRIMARY KEY, nombre_defecto TEXT NOT NULL UNIQUE, descripcion TEXT NOT NULL)')
    print("Tabla 'defectos' lista.")
    
    # 4. (MODIFICADA) Crear tabla de UNIÓN (subarea_defecto)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subarea_defecto (
            id_sub_area INTEGER,
            id_defecto INTEGER,
            FOREIGN KEY (id_sub_area) REFERENCES sub_areas (id_sub_area),
            FOREIGN KEY (id_defecto) REFERENCES defectos (id_defecto),
            PRIMARY KEY (id_sub_area, id_defecto)
        )
    ''')
    print("Tabla 'subarea_defecto' lista.")

    # --- POBLAR LAS TABLAS ---
    # Insertar Areas
    for area in AREAS:
        cursor.execute("INSERT OR IGNORE INTO areas (nombre_area) VALUES (?)", (area,))
    
    # Insertar Sub-Areas
    for area_nombre, sub_areas_lista in SUB_AREAS.items():
        cursor.execute("SELECT id_area FROM areas WHERE nombre_area = ?", (area_nombre,))
        id_area = cursor.fetchone()[0]
        for sub_area in sub_areas_lista:
            cursor.execute("INSERT OR IGNORE INTO sub_areas (nombre_sub_area, id_area) VALUES (?, ?)", (sub_area, id_area))

    # Insertar Defectos
    for nombre, desc in DEFECTOS.items():
        cursor.execute("INSERT OR IGNORE INTO defectos (nombre_defecto, descripcion) VALUES (?, ?)", (nombre, desc))

    # Insertar Relaciones
    for sub_area_nombre, defecto_nombre in RELACIONES:
        cursor.execute("SELECT id_sub_area FROM sub_areas WHERE nombre_sub_area = ?", (sub_area_nombre,))
        id_sub_area = cursor.fetchone()[0]
        cursor.execute("SELECT id_defecto FROM defectos WHERE nombre_defecto = ?", (defecto_nombre,))
        id_defecto = cursor.fetchone()[0]
        cursor.execute("INSERT OR IGNORE INTO subarea_defecto (id_sub_area, id_defecto) VALUES (?, ?)", (id_sub_area, id_defecto))

    conn.commit()
    print("Base de datos jerárquica estructurada y poblada exitosamente.")

except sqlite3.Error as e:
    print(f"Error en la base de datos: {e}")
finally:
    if conn:
        conn.close()