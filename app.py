from flask import Flask, request, render_template, redirect, url_for
from flask_socketio import SocketIO, emit
import os
from yt_dlp import YoutubeDL
from pathlib import Path
from datetime import datetime
import threading
import re

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/', methods=['GET', 'POST'])
def index():
    print("Index page accessed")
    if request.method == 'POST':
        print("POST request received")
        video_url = request.form['url']
        download_thread = threading.Thread(target=download_video, args=(video_url,))
        download_thread.start()
        return redirect(url_for('progress'))
    return render_template('index.html')

@app.route('/progress')
def progress():
    return render_template('progress.html')

def download_video(video_url):
    download_path = get_default_download_path()
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    ydl_opts = {
        'outtmpl': os.path.join(download_path, f'%(title)s_{now}.%(ext)s'),
        'format': 'bestvideo[ext=mp4]/best',  # Ajuste para formato simples
        'progress_hooks': [progress_hook]
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
    except Exception as e:
        print(f"Error: {e}")

def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d['_percent_str']
        percent_clean = re.sub(r'\x1b\[\d+;\d+m', '', percent)  # Remover códigos de controle
        speed = d['_speed_str']
        eta = d['_eta_str']
        print(f"Progress: {percent_clean} Speed: {speed} ETA: {eta}")
        # Emitir evento de progresso
        socketio.emit('download_progress', {'percent': percent_clean, 'speed': speed, 'eta': eta}, namespace='/')
    elif d['status'] == 'finished':
        print("Download finished")
        socketio.emit('download_finished', {'message': 'Download Concluído!'}, namespace='/')

@app.route('/success')
def success():
    print("Success page accessed")
    return 'Download Concluído! O vídeo foi salvo na pasta de downloads.'

def get_default_download_path():
    if os.name == 'nt':  # Windows
        return str(Path.home() / "Downloads")
    else:  # MacOS e Linux
        return str(Path.home() / "Downloads")

if __name__ == '__main__':
    print("Starting Flask app")
    socketio.run(app, debug=True)
