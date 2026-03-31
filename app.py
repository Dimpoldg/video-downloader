from flask import Flask, request, jsonify, send_from_directory
import yt_dlp

app = Flask(__name__)

# ✅ Homepage route (VERY IMPORTANT)
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

# ✅ Download API
@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')

    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'downloads/%(title)s.%(ext)s'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        return jsonify({
            "success": True,
            "download_url": filename
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

# ✅ Render ke liye correct run
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)