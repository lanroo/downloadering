from flask import Flask, request, render_template, redirect, url_for, send_file
from flask_socketio import SocketIO, emit
import os
from yt_dlp import YoutubeDL
from datetime import datetime
import threading
import re

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Diretório fixo para armazenar arquivos baixados
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

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

class MyLogger:
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)

def download_video(video_url):
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    download_path = os.path.join(DOWNLOAD_FOLDER, f'{now}')
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    ydl_opts = {
        'outtmpl': os.path.join(download_path, f'%(title)s_{now}.%(ext)s'),
        'format': 'bestvideo[ext=mp4]/best',
        'progress_hooks': [progress_hook],
        'verbose': True,
        'logger': MyLogger()
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        for file in os.listdir(download_path):
            file_path = os.path.join(download_path, file)
            relative_file_path = os.path.relpath(file_path, DOWNLOAD_FOLDER)
            socketio.emit('download_finished', {'file_path': relative_file_path}, namespace='/')
    except Exception as e:
        print(f"Error: {e}")

def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d['_percent_str']
        percent_clean = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', percent)
        speed = d['_speed_str']
        eta = d['_eta_str']
        print(f"Progress: {percent_clean} Speed: {speed} ETA: {eta}")
        socketio.emit('download_progress', {'percent': percent_clean, 'speed': speed, 'eta': eta}, namespace='/')
    elif d['status'] == 'finished':
        print("Download finished")

@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "Arquivo não encontrado", 404

if __name__ == '__main__':
    print("Starting Flask app")
    socketio.run(app, debug=True, port=5000)
