from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import os
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    video_url = data.get('url')

    try:
        download_dir = os.path.join(os.getcwd(), "downloads")
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        ydl_opts = {
            'outtmpl': os.path.join(download_dir, '%(id)s.%(ext)s'),
            'format': 'mp4'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            video_id = info_dict.get('id')
            video_ext = info_dict.get('ext')
            video_filename = f"{video_id}.{video_ext}"

        file_path = os.path.join(download_dir, video_filename)

        if os.path.exists(file_path):
            download_link = f'/download_video/{video_filename}'
            return jsonify({'download_link': download_link})
        else:
            return jsonify({'error': 'File not found after download.'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download_video/<filename>')
def download_video(filename):
    download_dir = os.path.join(os.getcwd(), "downloads")
    file_path = os.path.join(download_dir, filename)

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "File not found.", 404

if __name__ == '__main__':
    app.run(debug=True)
