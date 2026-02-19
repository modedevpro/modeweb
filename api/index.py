# Developer: محمود عادل الغريب

from flask import Flask, request, Response
import requests
import base64
import urllib.parse
import json

app = Flask(__name__)

def deco(text):
    decoded = urllib.parse.unquote(text)
    try:
        if base64.b64encode(base64.b64decode(decoded)).decode() == decoded:
            return base64.b64decode(decoded).decode()
    except:
        pass
    return decoded

def google_translate(text, target_lang="en"):
    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        "client": "gtx",
        "sl": "auto",
        "tl": target_lang,
        "dt": "t",
        "q": text
    }

    response = requests.get(url, params=params)
    result = response.json()

    translated_text = ""
    for item in result[0]:
        translated_text += item[0]

    return translated_text

@app.route("/generate")
def generate():
    text = request.args.get("text")

    if not text:
        return "Error: No text provided", 400

    text = deco(text)
    translated = google_translate(text, "en")

    url = "https://api.websim.com/api/v1/inference/run_image_generation"

    payload = {
        "project_id": "hcrvyemb62atnf29vvhr",
        "prompt": translated,
        "aspect_ratio": "1:1"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 12; SM-A025F Build/SP1A.210812.016) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.7151.61 Mobile Safari/537.36",
        "Content-Type": "application/json",
        "origin": "https://websim.com",
        "referer": "https://websim.com/"
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    if "url" in data:
        image_response = requests.get(data["url"])
        return Response(image_response.content, content_type="image/jpeg")
    else:
        return "لا توجد صوره"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
