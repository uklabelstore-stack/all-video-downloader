from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import json

app = Flask(__name__)
CORS(app)  # Yeh browser blocking (CORS) ko khatam karega

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    video_url = data.get('url')
    
    if not video_url:
        return jsonify({'error': 'URL is required'}), 400
        
    try:
        command = ['yt-dlp', '-j', video_url]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        meta = json.loads(result.stdout)
        
        download_url = meta.get('url')
        title = meta.get('title')
        thumbnail = meta.get('thumbnail')
        
        return jsonify({
            'success': True,
            'title': title,
            'thumbnail': thumbnail,
            'download_url': download_url
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
