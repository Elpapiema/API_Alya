from flask import Flask, request, jsonify, send_file, url_for, send_from_directory
import yt_dlp
import os
import re
from flask_cors import CORS
import shutil

app = Flask(__name__)
CORS(app)  # Habilitar CORS para evitar bloqueos

# Carpeta de descargas
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), "tmp")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Archivo de cookies (debe estar en la misma carpeta que el script)
COOKIES_FILE = os.path.join(os.getcwd(), "cookies.txt")

# Ruta para servir el favicon
@app.route('/favicon.png')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'web'),
        'icon.png',
        mimetype='image/png'
    )

# Limpieza de la carpeta tmp al iniciar la aplicación
def clean_tmp_folder():
    if os.path.exists(DOWNLOAD_FOLDER):
        for filename in os.listdir(DOWNLOAD_FOLDER):
            file_path = os.path.join(DOWNLOAD_FOLDER, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Eliminar archivos o enlaces simbólicos
                    print(f"Archivo eliminado: {file_path}")
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Eliminar directorios
                    print(f"Directorio eliminado: {file_path}")
            except Exception as e:
                print(f"Error al eliminar {file_path}: {e}")

# Ruta para servir archivos descargados
@app.route('/tmp/<path:filename>')
def serve_file(filename):
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)

    if not os.path.exists(file_path):
        return jsonify({"error": "Archivo no encontrado"}), 404

    return send_file(file_path, as_attachment=True)

# Ruta para descargar audio
@app.route('/download_audio', methods=['GET'])
def download_audio():
    url = request.args.get('url')

    if not url:
        return jsonify({'error': 'Falta el parámetro URL'}), 400

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'cookiefile': COOKIES_FILE  # Se añade el uso de cookies
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

            # Detectar automáticamente el archivo descargado
            downloaded_files = os.listdir(DOWNLOAD_FOLDER)
            downloaded_files.sort(key=lambda x: os.path.getctime(os.path.join(DOWNLOAD_FOLDER, x)), reverse=True)
            original_filename = downloaded_files[0]

            # Generar un nombre seguro para la URL
            safe_title = re.sub(r'[^\w\-_.]', '_', info['title'])
            new_filename = f"{safe_title}.mp3"
            old_path = os.path.join(DOWNLOAD_FOLDER, original_filename)
            new_path = os.path.join(DOWNLOAD_FOLDER, new_filename)

            if old_path != new_path:
                os.rename(old_path, new_path)

        file_url = url_for('serve_file', filename=new_filename, _external=True)

        return jsonify({'message': 'Descarga de audio completada', 'file_url': file_url})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para descargar video
@app.route('/download_video', methods=['GET'])
def download_video():
    url = request.args.get('url')

    if not url:
        return jsonify({'error': 'Falta el parámetro URL'}), 400

    try:
        ydl_opts = {
            'format': 'best[height<=360]',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'cookiefile': COOKIES_FILE  # Se añade el uso de cookies
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

            # Detectar automáticamente el archivo descargado
            downloaded_files = os.listdir(DOWNLOAD_FOLDER)
            downloaded_files.sort(key=lambda x: os.path.getctime(os.path.join(DOWNLOAD_FOLDER, x)), reverse=True)
            original_filename = downloaded_files[0]

            safe_title = re.sub(r'[^\w\-_.]', '_', info['title'])
            new_filename = f"{safe_title}.mp4"
            old_path = os.path.join(DOWNLOAD_FOLDER, original_filename)
            new_path = os.path.join(DOWNLOAD_FOLDER, new_filename)

            if old_path != new_path:
                os.rename(old_path, new_path)

        file_url = url_for('serve_file', filename=new_filename, _external=True)

        return jsonify({
            'message': 'Descarga de video completada',
            'title': info.get('title', 'Desconocido'),
            'duration': info.get('duration', 0),
            'quality': '360p',
            'views': info.get('view_count', 0),
            'likes': info.get('like_count', 0),
            'comments': info.get('comment_count', 0),
            'file_url': file_url
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Nueva ruta para servir el archivo HTML
@app.route('/')
def index():
    return send_from_directory('web', 'index2.html')

# Llamar al script de limpieza antes de iniciar el servidor
if __name__ == '__main__':
    print("Iniciando limpieza de la carpeta tmp...")
    clean_tmp_folder()
    app.run(debug=True, port=10000, host='0.0.0.0')
