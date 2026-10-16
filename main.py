
from flask import Flask, request, jsonify, Response, render_template_string
from urllib.parse import urlparse
from datetime import datetime, timezone
from html import escape
import json
import os
import yt_dlp

# Vercel requires a top-level Flask instance named app.
app = Flask(__name__)

SITE_URL = "https://vdownloder.xyz"
SITE_NAME = "VDownloader"
CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "").strip()

app.config["JSON_SORT_KEYS"] = False

# ---------------- SHARED HTML TEMPLATE ----------------

BASE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ title }}</title>
<meta name="description" content="{{ description }}">
<meta name="robots" content="index,follow">
<link rel="canonical" href="{{ canonical }}">
<meta name="theme-color" content="#111827">

<meta property="og:type" content="website">
<meta property="og:site_name" content="VDownloader">
<meta property="og:title" content="{{ title }}">
<meta property="og:description" content="{{ description }}">
<meta property="og:url" content="{{ canonical }}">

<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{{ title }}">
<meta name="twitter:description" content="{{ description }}">

<script type="application/ld+json">{{ schema | safe }}</script>

<style>
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: Arial, Helvetica, sans-serif;
  line-height: 1.7;
  background: #f5f7fb;
  color: #172033;
}
header { background: #111827; padding: 18px 20px; }
.nav {
  max-width: 1050px;
  margin: auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 15px;
}
.brand {
  color: #60a5fa;
  font-size: 24px;
  font-weight: bold;
  text-decoration: none;
}
nav { display: flex; flex-wrap: wrap; gap: 15px; }
nav a { color: white; text-decoration: none; font-size: 14px; }
nav a:hover { color: #60a5fa; }
main { max-width: 900px; min-height: 60vh; margin: 40px auto; padding: 0 18px; }
.hero { text-align: center; }
h1 { font-size: clamp(30px, 6vw, 46px); line-height: 1.2; }
h2 { line-height: 1.35; }
.subtitle { color: #64748b; font-size: 17px; }
.panel, .content {
  background: white;
  margin-top: 25px;
  padding: 25px;
  border-radius: 14px;
  box-shadow: 0 8px 30px #1720330d;
}
.input-row { display: flex; gap: 10px; }
input {
  flex: 1;
  min-width: 0;
  padding: 14px;
  border: 1px solid #cbd5e1;
  border-radius: 9px;
  font-size: 16px;
}
button {
  padding: 14px 22px;
  background: #2563eb;
  border: 0;
  border-radius: 9px;
  color: white;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
}
button:disabled { opacity: .6; cursor: wait; }
#status { margin-top: 15px; overflow-wrap: anywhere; }
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
  background: #16a34a;
  color: white;
  padding: 12px 18px;
  margin-top: 10px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: bold;
}
a { overflow-wrap: anywhere; }
footer {
  text-align: center;
  padding: 25px 15px;
  color: #64748b;
  font-size: 14px;
}
footer a { color: #475569; margin: 0 7px; }
@media (max-width: 600px) {
  main { margin: 25px auto; }
  .input-row { flex-direction: column; }
  button { width: 100%; }
  .panel, .content { padding: 18px; }
}
</style>
</head>
<body>
<header>
  <div class="nav">
    <a class="brand" href="/">VDownloader</a>
    <nav aria-label="Main navigation">
      <a href="/">Home</a>
      <a href="/about">About</a>
      <a href="/contact">Contact</a>
      <a href="/privacy-policy">Privacy</a>
      <a href="/terms">Terms</a>
    </nav>
  </div>
</header>
<main>{{ body | safe }}</main>
<footer>
  <div>&copy; <span id="year"></span> VDownloader</div>
  <p>
    <a href="/about">About Us</a>
    <a href="/contact">Contact</a>
    <a href="/privacy-policy">Privacy Policy</a>
    <a href="/terms">Terms of Service</a>
  </p>
</footer>
<script>
document.getElementById("year").textContent = new Date().getFullYear();
</script>
</body>
</html>
"""

# ---------------- HOME PAGE ----------------

HOME_BODY = """
<section class="hero">
  <h1>Online Video Downloader</h1>
  <p class="subtitle">
    Check supported public video links with VDownloader.
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

<section class="content">
  <h2>How to Use VDownloader</h2>
  <ol>
    <li>Copy a supported public video URL.</li>
    <li>Paste the link into the box above.</li>
    <li>Click Get Video and wait for the result.</li>
    <li>Open the video link if one is available.</li>
  </ol>

  <h2>Supported Video Platforms</h2>
  <p>
    VDownloader supports compatible public links from YouTube,
    Facebook, Instagram, TikTok, Vimeo and Dailymotion.
    Availability depends on the platform and video restrictions.
  </p>

  <h2>Use Videos Responsibly</h2>
  <p>
    Only save videos you own or have permission to download.
    Copyright laws and platform restrictions may apply.
    VDownloader does not host the videos it processes.
  </p>
</section>

<script>
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
      throw new Error("Invalid URL");
    }
  } catch (error) {
    statusBox.textContent = "Please enter a valid video URL.";
    return;
  }

  button.disabled = true;
  button.textContent = "Checking...";
  statusBox.textContent = "Checking video. Please wait.";

  try {
    const response = await fetch("/download", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({url: url})
    });

    const data = await response.json();

    if (!response.ok || !data.success) {
      throw new Error(data.error || "Unable to process this video.");
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
        "A direct video link is unavailable for this video.";
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
"""

# ---------------- SEO AND INFORMATION PAGES ----------------

PAGES = {
    "/about": {
        "title": "About VDownloader",
        "description": "Learn about VDownloader and its online video link tool.",
        "body": """
        <section class="content">
          <h1>About VDownloader</h1>
          <p>VDownloader helps users check supported public video links
          and view available video information.</p>
          <p>VDownloader does not host video content. Use the service
          only with content you own or are permitted to save.</p>
        </section>
        """
    },
    "/contact": {
        "title": "Contact VDownloader",
        "description": "Contact the VDownloader website team.",
        "body": None
    },
    "/privacy-policy": {
        "title": "Privacy Policy | VDownloader",
        "description": "Read how VDownloader processes submitted video links.",
        "body": """
        <section class="content">
          <h1>Privacy Policy</h1>
          <p>When you submit a video URL, the service processes it
          to retrieve available video information.</p>
          <p>Please do not submit private, confidential or sensitive links.</p>
          <p>The hosting provider may process technical request logs
          to operate and protect the website.</p>
          <p>This policy must be updated if the website uses analytics,
          advertising cookies, third-party tracking or other data
          collection services. Contact the website operator with
          privacy-related questions.</p>
        </section>
        """
    },
    "/terms": {
        "title": "Terms of Service | VDownloader",
        "description": "Terms for using the VDownloader online video tool.",
        "body": """
        <section class="content">
          <h1>Terms of Service</h1>
          <p>Use VDownloader only for lawful purposes and with videos
          you own or have permission to save.</p>
          <p>You are responsible for complying with copyright law
          and the terms of third-party platforms.</p>
          <p>The service is provided on an availability basis.
          Some videos may not be accessible or supported.</p>
          <p>Do not use this website to violate another person's
          rights or bypass access restrictions.</p>
        </section>
        """
    }
}

def render_page(title, description, body, path="/"):
    schema = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": SITE_NAME,
        "url": SITE_URL,
        "description": description
    }

    return render_template_string(
        BASE_HTML,
        title=title,
        description=description,
        canonical=SITE_URL + path,
        schema=json.dumps(schema),
        body=body
    )

@app.route("/")
def home():
    return render_page(
        "VDownloader - Online Video Downloader",
        "Check supported public video links with VDownloader, "
        "a simple online video information tool.",
        HOME_BODY,
        "/"
    )

@app.route("/about")
@app.route("/contact")
@app.route("/privacy-policy")
@app.route("/terms")
def information_page():
    path = request.path
    page = PAGES[path]

    if path == "/contact":
        if CONTACT_EMAIL:
            contact_text = (
                '<p>Email: <a href="mailto:' +
                escape(CONTACT_EMAIL, quote=True) + '">' +
                escape(CONTACT_EMAIL) + '</a></p>'
            )
        else:
            contact_text = (
                "<p>For contact details, the website operator must "
                "configure the CONTACT_EMAIL environment variable.</p>"
            )

        body = (
            '<section class="content"><h1>Contact VDownloader</h1>' +
            contact_text +
            "<p>For privacy questions or website feedback, contact "
            "the website operator using the email provided above.</p>"
            "</section>"
        )
    else:
        body = page["body"]

    return render_page(
        page["title"],
        page["description"],
        body,
        path
    )

# ---------------- ROBOTS AND SITEMAP ----------------

@app.route("/robots.txt")
def robots():
    content = (
        "User-agent: *\n"
        "Allow: /\n\n"
        "Sitemap: " + SITE_URL + "/sitemap.xml\n"
    )
    return Response(content, mimetype="text/plain")

@app.route("/sitemap.xml")
def sitemap():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    paths = ["/", "/about", "/contact", "/privacy-policy", "/terms"]

    entries = []
    for path in paths:
        entries.append(
            "<url><loc>" + SITE_URL + path + "</loc>"
            "<lastmod>" + today + "</lastmod></url>"
        )

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + "".join(entries) +
        "</urlset>"
    )
    return Response(xml, mimetype="application/xml")

# ---------------- VIDEO DOWNLOAD API ----------------

@app.route("/download", methods=["POST"])
def download():
    data = request.get_json(silent=True) or {}
    url = data.get("url", "")

    if not isinstance(url, str) or not url.strip():
        return jsonify({
            "success": False,
            "error": "Please enter a video URL."
        }), 400

    url = url.strip()

    try:
        parsed = urlparse(url)

        if parsed.scheme not in ("http", "https") or not parsed.hostname:
            return jsonify({
                "success": False,
                "error": "Please enter a valid HTTP or HTTPS URL."
            }), 400

        host = parsed.hostname.lower().rstrip(".")

        allowed_domains = (
            "youtube.com", "youtu.be", "youtube-nocookie.com",
            "facebook.com", "fb.watch", "instagram.com",
            "tiktok.com", "vimeo.com", "dailymotion.com"
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
            "socket_timeout": 15
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        video_url = info.get("url")

        if not video_url and info.get("formats"):
            formats = [
                item for item in info["formats"]
                if item.get("url") and item.get("vcodec") != "none"
            ]
            if formats:
                video_url = formats[-1].get("url")

        if not video_url:
            return jsonify({
                "success": False,
                "error": "No direct video link is available."
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
                "restricted, or unsupported."
            )
        }), 200

    except Exception:
        app.logger.exception("Video processing failed")
        return jsonify({
            "success": False,
            "error": "Server error. Please try again later."
        }), 500

# Local development only. Vercel imports the app above.
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
