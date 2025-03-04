from flask import Flask, request, jsonify
import yt_dlp
import requests
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)  # Habilitar CORS para evitar bloqueos

def upload_to_quax(file_stream, filename):
    """
    Sube un archivo directamente a qu.ax usando streaming.
    """
    url = "https://qu.ax/upload.php"
    files = {'files[]': (filename, file_stream)}
    response = requests.post(url, files=files)
    if response.status_code == 200:
        return response.json()['files'][0]['url']
    else:
        raise Exception("Error al subir el archivo a qu.ax")

@app.route('/download_audio', methods=['GET'])
def download_audio():
    url = request.args.get('url')

    if not url:
        return jsonify({'error': 'Falta el parámetro URL'}), 400

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'extract_audio': True,
            'audio_format': 'mp3',
            'outtmpl': '%(title)s.%(ext)s',  # Nombre del archivo
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            safe_title = re.sub(r'[^\w\-_.]', '_', info['title'])
            filename = f"{safe_title}.mp3"

            # Descargar el archivo en memoria y enviarlo directamente a qu.ax
            with ydl.urlopen(info['url']) as file_stream:
                file_url = upload_to_quax(file_stream, filename)

        return jsonify({'message': 'Descarga de audio completada', 'file_url': file_url})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download_video', methods=['GET'])
def download_video():
    url = request.args.get('url')

    if not url:
        return jsonify({'error': 'Falta el parámetro URL'}), 400

    try:
        ydl_opts = {
            'format': 'best[height<=360]',  # Calidad máxima 360p
            'outtmpl': '%(title)s.%(ext)s',  # Nombre del archivo
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            safe_title = re.sub(r'[^\w\-_.]', '_', info['title'])
            filename = f"{safe_title}.mp4"

            # Descargar el archivo en memoria y enviarlo directamente a qu.ax
            with ydl.urlopen(info['url']) as file_stream:
                file_url = upload_to_quax(file_stream, filename)

        return jsonify({
            'message': 'Descarga de video completada',
            'file_url': file_url,
            'title': info.get('title', 'Desconocido'),
            'duration': info.get('duration', 0),
            'quality': '360p',
            'views': info.get('view_count', 0),
            'likes': info.get('like_count', 0),
            'comments': info.get('comment_count', 0)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')