from flask import Flask, send_from_directory
import os

app = Flask(__name__)

# Ruta base donde se encuentra la carpeta alyadocs
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
ALYADOCS_DIR = os.path.join(BASE_DIR, 'alyadocs')

@app.route('/<path:filename>')
def serve_file(filename):
    # Construye la ruta completa al archivo
    file_path = os.path.join(ALYADOCS_DIR, filename)
    
    # Verifica si el archivo existe
    if os.path.isfile(file_path):
        return send_from_directory(ALYADOCS_DIR, filename)
    else:
        return "Archivo no encontrado", 404

@app.route('/')
def index():
    # Puedes servir un archivo index.html si existe, o listar los archivos
    index_file = os.path.join(ALYADOCS_DIR, 'index.html')
    if os.path.isfile(index_file):
        return send_from_directory(ALYADOCS_DIR, 'index.html')
    else:
        # Listar archivos y directorios si no hay index.html
        files = os.listdir(ALYADOCS_DIR)
        return "<br>".join(files)

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')