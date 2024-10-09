from flask import Flask, render_template, request, send_from_directory
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    playlist_url = request.form['playlist_url']
    download_path = request.form['download_path']

    if not os.path.exists(download_path):
        os.makedirs(download_path)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])
        
        # List files in the download directory
        files = os.listdir(download_path)
        return render_template('download_complete.html', files=files, path=download_path)
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/files/<path:filename>', methods=['GET'])
def get_file(filename):
    directory = os.path.dirname(filename)
    return send_from_directory(directory, os.path.basename(filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
