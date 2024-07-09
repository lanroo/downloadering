from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import os
from yt_dlp import YoutubeDL
from pathlib import Path

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form['url']
        download_path = request.form['download_path']
        if not download_path:
            download_path = get_default_download_path()
        
        ydl_opts = {
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            'format': 'best'
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
    return 'Download Concluído! O vídeo foi salvo no diretório especificado.'

@app.route('/select_directory', methods=['GET'])
def select_directory():
    root_path = Path.home()
    directories = [d for d in root_path.iterdir() if d.is_dir()]
    return render_template('select_directory.html', directories=directories, current_path=root_path)

@app.route('/navigate_directory', methods=['POST'])
def navigate_directory():
    selected_directory = request.form['selected_directory']
    directories = [d for d in Path(selected_directory).iterdir() if d.is_dir()]
    return render_template('select_directory.html', directories=directories, current_path=selected_directory)

def get_default_download_path():
    if os.name == 'nt':  # Windows
        return str(Path.home() / "Downloads")
    else:  # MacOS e Linux
        return str(Path.home() / "Downloads")

if __name__ == '__main__':
    app.run(debug=True)
