import yt_dlp
import uuid
import json

def handler(request):
    if request.method != "POST":
        return {
            "statusCode": 405,
            "body": "Method Not Allowed"
        }

    data = request.get_json()
    url = data.get("url")

    if not url:
        return {
            "statusCode": 400,
            "body": "No URL provided"
        }

    output_path = f"/tmp/{uuid.uuid4()}.mp4"

    ydl_opts = {
        'format': 'best',
        'outtmpl': output_path,
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        with open(output_path, "rb") as f:
            file_data = f.read()

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/octet-stream"
            },
            "body": file_data
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }
