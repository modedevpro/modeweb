from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route("/")
def home():
    return "Video Links Extractor API is working ✅"

@app.route("/download", methods=["GET"])
def get_video_links():
    url = request.args.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {
        'quiet': True,
        'skip_download': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        formats = info.get("formats", [])
        links = []

        for f in formats:
            if f.get("url"):
                links.append({
                    "quality": f.get("format_note") or f.get("height"),
                    "ext": f.get("ext"),
                    "url": f.get("url")
                })

        return jsonify({
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "links": links
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
