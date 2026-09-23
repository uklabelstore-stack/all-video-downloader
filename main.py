from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import yt_dlp
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>VDownloader - Video Downloader</title>
        <meta name="description" content="Download videos online quickly and easily with VDownloader.">
        <meta name="robots" content="index, follow">
    </head>
    <body>
        <h1>VDownloader</h1>
        <p>Online video downloader.</p>
    </body>
    </html>
    """


@app.route("/robots.txt")
def robots():
    content = """User-agent: *
Allow: /

Sitemap: https://www.vdownloder.xyz/sitemap.xml
"""
    return Response(content, mimetype="text/plain")


@app.route("/sitemap.xml")
def sitemap():
    today = datetime.utcnow().strftime("%Y-%m-%d")

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://www.vdownloder.xyz/</loc>
        <lastmod>{today}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
</urlset>
"""

    return Response(xml, mimetype="application/xml")


@app.route("/download", methods=["POST"])
def download():

    data = request.get_json(silent=True) or {}
    url = data.get("url", "").strip()

    if not url:
        return jsonify({
            "success": False,
            "error": "No URL provided"
        }), 400

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "format": "best",
        "http_headers": {
            "User-Agent": (
                "Mozilla/5.0 (Linux; Android 10) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/126.0 Mobile Safari/537.36"
            )
        },
        "extractor_args": {
            "tiktok": {
                "api_hostname": "api22-normal-c-useast2a.tiktokv.com"
            }
        }
    }

    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        return jsonify({
            "success": True,
            "title": info.get("title", "Video"),
            "thumbnail": info.get("thumbnail"),
            "download_url": info.get("url")
        })

    except yt_dlp.utils.DownloadError as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "error": "Server error: " + str(e)
        }), 200


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )