import os
from flask import Flask, request, jsonify

# Aquí importarías tus funciones de cada parser cuando las adaptes, por ejemplo:
# from parser_edesur import procesar_edesur
# from parser_RUS import procesar_rus
# from parser_woker import procesar_woker

app = Flask(__name__)

@app.route('/parsear', methods=['POST'])
def parsear_factura():
    # 1. Verificar si viene un archivo y qué proveedor es
    if 'file' not in request.files:
        return jsonify({"error": "No se envió ningún archivo 'file'"}), 400
    
    file = request.files['file']
    proveedor = request.form.get('proveedor', 'edesur')  # Por defecto edesur o el que elijas
    
    if file.filename == '':
        return jsonify({"error": "El archivo no tiene nombre"}), 400

    # 2. Guardar el PDF temporalmente en la carpeta /tmp
    temp_path = os.path.join("/tmp", file.filename)
    file.save(temp_path)
    
    try:
        resultado = {}
        
        # 3. Ejecutar el parser correspondiente según el proveedor
        if proveedor == 'edesur':
            # Llamar a tu función de edesur pasando temp_path
            # resultado = procesar_edesur(temp_path)
            pass
        elif proveedor == 'rus':
            # resultado = procesar_rus(temp_path)
            pass
        elif proveedor == 'woker':
            # resultado = procesar_woker(temp_path)
            pass
        else:
            return jsonify({"error": f"Proveedor '{proveedor}' no reconocido"}), 400

        # Limpiar el archivo temporal
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        return jsonify({
            "status": "success",
            "proveedor": proveedor,
            "data": resultado
        }), 200

    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
