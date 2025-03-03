from flask import Flask, request, jsonify
import yt_dlp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilitar CORS para evitar bloqueos

# Ruta para obtener el enlace del audio
@app.route('/get_audio', methods=['GET'])
def get_audio():
    url = request.args.get('url')

    if not url:
        return jsonify({'error': 'Falta el parámetro URL'}), 400

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info['url']  # Enlace directo al audio

        return jsonify({'message': 'Enlace de audio obtenido', 'audio_url': audio_url})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para obtener el enlace del video
@app.route('/get_video', methods=['GET'])
def get_video():
    url = request.args.get('url')

    if not url:
        return jsonify({'error': 'Falta el parámetro URL'}), 400

    try:
        ydl_opts = {
            'format': 'best[height<=360]',  # Calidad máxima 360p
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info['url']  # Enlace directo al video

        return jsonify({
            'message': 'Enlace de video obtenido',
            'title': info.get('title', 'Desconocido'),
            'duration': info.get('duration', 0),
            'quality': '360p',
            'views': info.get('view_count', 0),
            'likes': info.get('like_count', 0),
            'comments': info.get('comment_count', 0),
            'video_url': video_url
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')