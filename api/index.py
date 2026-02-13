from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route("/download")
def download():
    url = request.args.get("url")

    if not url:
        return jsonify({"error": "Missing url parameter"}), 400

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'format': '18/22/best',
        'extractor_args': {
            'youtube': {
                'player_client': ['web']
            }
        },
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            return jsonify({
                "title": info.get("title"),
                "download_url": info.get("url")
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
