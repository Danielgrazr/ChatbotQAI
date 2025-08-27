import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)

# --- Función para conectar y consultar la base de datos ---
def query_db(query, args=(), one=False):
    try:
        conn = sqlite3.connect('chatbot_db.sqlite')
        cursor = conn.cursor()
        cursor.execute(query, args)
        results = cursor.fetchall()
        conn.close()
        return (results[0] if results else None) if one else results
    except sqlite3.Error as e:
        print(f"Error de base de datos: {e}")
        return None

# --- Rutas de la API ---

@app.route('/areas', methods=['GET'])
def get_areas():
    areas_result = query_db("SELECT nombre_area FROM areas")
    if areas_result is None: return jsonify({"error": "Error de base de datos"}), 500
    areas_list = [item[0] for item in areas_result]
    return jsonify(areas_list)

@app.route('/subareas', methods=['GET'])
def get_subareas():
    area_name = request.args.get('area_name')
    if not area_name: return jsonify({"error": "Falta el parámetro 'area_name'"}), 400

    query = """
        SELECT sa.nombre_sub_area FROM sub_areas sa
        JOIN areas a ON sa.id_area = a.id_area WHERE a.nombre_area = ?
    """
    subareas_result = query_db(query, [area_name])
    if subareas_result is None: return jsonify({"error": "Error de base de datos"}), 500
    subareas_list = [item[0] for item in subareas_result]
    return jsonify(subareas_list)

@app.route('/defectos', methods=['GET'])
def get_defectos():
    sub_area_name = request.args.get('sub_area_name')
    if not sub_area_name: return jsonify({"error": "Falta el parámetro 'sub_area_name'"}), 400

    query = """
        SELECT d.nombre_defecto, d.descripcion FROM defectos d
        JOIN subarea_defecto sd ON d.id_defecto = sd.id_defecto
        JOIN sub_areas sa ON sd.id_sub_area = sa.id_sub_area WHERE sa.nombre_sub_area = ?
    """
    defectos_result = query_db(query, [sub_area_name])
    if defectos_result is None: return jsonify({"error": "Error de base de datos"}), 500
    
    # Devolvemos una lista de objetos, cada uno con nombre y descripción
    defectos_list = [{"nombre": item[0], "descripcion": item[1]} for item in defectos_result]
    return jsonify(defectos_list)

# --- Iniciar el Servidor ---
if __name__ == '__main__':
    app.run(debug=True, port=5001) # Usaremos el puerto 5001 para evitar conflictos