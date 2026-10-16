
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import yt_dlp
import os
from datetime import datetime
from urllib.parse import urlparse

app = Flask(__name__)
CORS(app)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>VDownloader - Online Video Downloader</title>
    <meta name="description" content="VDownloader helps you find downloadable videos from supported public links.">
    <meta name="robots" content="index, follow">
    <meta name="theme-color" content="#111827">
    <style>
        * { box-sizing: border-box; }
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f5f7fb;
            color: #172033;
        }
        header {
            background: #111827;
            color: white;
            padding: 20px;
        }
        .nav {
            max-width: 1000px;
            margin: auto;
            font-size: 23px;
            font-weight: bold;
        }
        .brand { color: #60a5fa; }
        main {
            max-width: 850px;
            margin: 65px auto;
            padding: 20px;
        }
        .hero { text-align: center; }
        h1 { font-size: clamp(32px, 6vw, 48px); margin-bottom: 12px; }
        .subtitle {
            color: #64748b;
            font-size: 17px;
            line-height: 1.6;
        }
        .panel {
            margin-top: 30px;
            background: white;
            padding: 24px;
            border-radius: 16px;
            box-shadow: 0 8px 30px #1720330d;
        }
        .input-row {
            display: flex;
            gap: 10px;
        }
        input {
            min-width: 0;
            flex: 1;
            padding: 15px;
            border: 1px solid #cbd5e1;
            border-radius: 9px;
            font-size: 16px;
        }
        button {
            border: 0;
            background: #2563eb;
            color: white;
            font-size: 16px;
            font-weight: bold;
            padding: 15px 22px;
            border-radius: 9px;
            cursor: pointer;
        }
        button:disabled { opacity: .6; cursor: wait; }
        #status {
            margin-top: 18px;
            line-height: 1.6;
            overflow-wrap: anywhere;
        }
        #result { margin-top: 20px; }
        #result img {
            display: block;
            max-width: 100%;
            max-height: 300px;
            margin: 15px auto;
            border-radius: 10px;
        }
        .download-link {
            display: inline-block;
            margin-top: 10px;
            padding: 13px 20px;
            background: #16a34a;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
        }
        .steps {
            margin-top: 28px;
            background: white;
            padding: 24px;
            border-radius: 14px;
            line-height: 1.9;
        }
        footer {
            text-align: center;
            padding: 25px;
            color: #64748b;
            font-size: 14px;
        }
        @media(max-width: 560px) {
            main { margin: 35px auto; padding: 15px; }
            .input-row { flex-direction: column; }
            button { width: 100%; }
            .panel { padding: 18px; }
        }
    </style>
</head>
<body>
<header>
    <div class="nav"><span class="brand">V</span>Downloader</div>
</header>

<main>
    <section class="hero">
        <h1>Online Video Downloader</h1>
        <p class="subtitle">
            Paste a public video link to check whether a downloadable
            video is available.
        </p>
    </section>

    <section class="panel">
        <form id="downloadForm">
            <div class="input-row">
                <input id="videoUrl" type="url"
                    placeholder="Paste video URL here..."
                    aria-label="Video URL" required>
                <button id="submitBtn" type="submit">Get Video</button>
            </div>
        </form>
        <div id="status" role="status" aria-live="polite"></div>
        <div id="result"></div>
    </section>

    <section class="steps">
        <h2>How to use VDownloader</h2>
        <ol>
            <li>Copy the link of a publicly accessible video.</li>
            <li>Paste the link into the box above.</li>
            <li>Click Get Video and wait for the result.</li>
            <li>If a direct download link is available, open it to save the video.</li>
        </ol>
        <p>
            Only download videos you own or have permission to save.
            Website restrictions may apply.
        </p>
    </section>
</main>

<footer>
    &copy; <span id="year"></span> VDownloader. Use responsibly.
</footer>

<script>
document.getElementById("year").textContent = new Date().getFullYear();

const form = document.getElementById("downloadForm");
const input = document.getElementById("videoUrl");
const button = document.getElementById("submitBtn");
const statusBox = document.getElementById("status");
const result = document.getElementById("result");

form.addEventListener("submit", async function(event) {
    event.preventDefault();
    statusBox.textContent = "";
    result.replaceChildren();

    const url = input.value.trim();

    try {
        const parsed = new URL(url);
        if (!["http:", "https:"].includes(parsed.protocol)) {
            throw new Error("Please enter a valid HTTP or HTTPS URL.");
        }
    } catch (e) {
        statusBox.textContent = "Please enter a valid video link.";
        return;
    }

    button.disabled = true;
    button.textContent = "Checking...";
    statusBox.textContent = "Checking video availability. Please wait.";

    try {
        const response = await fetch("/download", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({url: url})
        });

        const data = await response.json();

        if (!data.success) {
            throw new Error(data.error || "This video could not be processed.");
        }

        statusBox.textContent = "Video information found.";

        const title = document.createElement("h2");
        title.textContent = data.title || "Video";
        result.appendChild(title);

        if (data.thumbnail) {
            const img = document.createElement("img");
            img.src = data.thumbnail;
            img.alt = "Video thumbnail";
            img.referrerPolicy = "no-referrer";
            result.appendChild(img);
        }

        if (data.download_url) {
            const link = document.createElement("a");
            link.href = data.download_url;
            link.target = "_blank";
            link.rel = "noopener noreferrer";
            link.className = "download-link";
            link.textContent = "Open Video";
            result.appendChild(link);

            const note = document.createElement("p");
            note.textContent =
                "If the video opens in your browser, use its menu to save it if available.";
            result.appendChild(note);
        } else {
            statusBox.textContent =
                "Video found, but a direct download link is unavailable.";
        }
    } catch (error) {
        statusBox.textContent =
            error.message || "Something went wrong. Please try again.";
    } finally {
        button.disabled = false;
        button.textContent = "Get Video";
    }
});
</script>
</body>
</html>
"""


@app.route("/")
def home():
    return HTML


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
    url = data.get("url", "")

    if not isinstance(url, str):
        return jsonify({"success": False, "error": "Invalid URL"}), 400

    url = url.strip()

    if not url:
        return jsonify({
            "success": False,
            "error": "Please enter a video URL."
        }), 400

    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https") or not parsed.hostname:
            return jsonify({
                "success": False,
                "error": "Please enter a valid HTTP or HTTPS URL."
            }), 400

        # Only allow common public video platforms.
        host = parsed.hostname.lower().rstrip(".")
        allowed_domains = (
            "youtube.com", "youtu.be", "youtube-nocookie.com",
            "facebook.com", "fb.watch",
            "instagram.com",
            "tiktok.com",
            "vimeo.com",
            "dailymotion.com",
        )

        if not any(
            host == domain or host.endswith("." + domain)
            for domain in allowed_domains
        ):
            return jsonify({
                "success": False,
                "error": "This video platform is not supported."
            }), 400

        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
            "format": "best",
            "socket_timeout": 15,
            "http_headers": {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/126.0.0.0 Safari/537.36"
                )
            },
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        video_url = info.get("url")
        if not video_url and info.get("formats"):
            formats = [
                f for f in info["formats"]
                if f.get("url") and f.get("vcodec") != "none"
            ]
            if formats:
                video_url = formats[-1].get("url")

        if not video_url:
            return jsonify({
                "success": False,
                "error": "No direct video link is available for this video."
            }), 200

        return jsonify({
            "success": True,
            "title": info.get("title") or "Video",
            "thumbnail": info.get("thumbnail"),
            "download_url": video_url
        })

    except yt_dlp.utils.DownloadError:
        return jsonify({
            "success": False,
            "error": (
                "Could not access this video. It may be private, "
                "restricted, or unsupported. Please try another public link."
            )
        }), 200

    except Exception:
        app.logger.exception("Video processing failed")
        return jsonify({
            "success": False,
            "error": "Server error. Please try again later."
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
