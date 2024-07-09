from flask import Flask, request, render_template, redirect, url_for
import os
from yt_dlp import YoutubeDL
from pathlib import Path

app = Flask(__name__)

def get_download_path():
    if os.name == 'nt':  # Windows
        return str(Path.home() / "Downloads")
    else:  # MacOS e Linux
        return str(Path.home() / "Downloads")

def get_best_format(video_url):
    ydl_opts = {'listformats': True}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        formats = info.get('formats', [info])
        # Filtra apenas os formatos com extensão mp4
        mp4_formats = [f for f in formats if f.get('ext') == 'mp4']
        if not mp4_formats:
            return None  # Nenhum formato mp4 disponível
        return mp4_formats[-1]['format_id']  # Seleciona o melhor formato mp4 disponível

@app.route('/', methods=['GET', 'POST'])
def index():
    print("Index page accessed")
    if request.method == 'POST':
        print("POST request received")
        video_url = request.form['url']
        download_path = get_download_path()
        best_format = get_best_format(video_url)
        if best_format is None:
            return "Erro: Nenhum formato mp4 disponível para o vídeo."
        ydl_opts = {
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            'format': best_format,
            'cookiefile': 'cookies.txt'  # Adicione o caminho para o arquivo de cookies
        }
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            return redirect(url_for('success'))
        except Exception as e:
            print(f"Error: {e}")
            return str(e)
    return render_template('index.html')

@app.route('/success')
def success():
    print("Success page accessed")
    return 'Download Concluído! O vídeo foi salvo no diretório de Downloads.'

if __name__ == '__main__':
    print("Starting Flask app")
    app.run(debug=True)
