from flask import Flask, request, jsonify, Response, render_template_string, redirect, abort
from urllib.parse import urlparse
from html import escape
import json
import os
import yt_dlp
import io

# Pillow is used to generate an Open Graph image on the fly if a static file
# is not present in the repository. This avoids committing a binary image file.
try:
    from PIL import Image, ImageDraw, ImageFont
except Exception:
    Image = None

# Vercel requires a top-level Flask instance named app.
app = Flask(__name__)

SITE_URL = "https://www.vdownloder.xyz"
SITE_NAME = "VDownloader"
CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "uklabelstore@gmail.com").strip()
LAST_UPDATED = "2026-10-17"  # change this date when you add or edit pages

app.config["JSON_SORT_KEYS"] = False

# ---------------- SHARED HTML TEMPLATE ----------------

BASE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ title }}</title>
<meta name="description" content="{{ description }}">
<meta name="robots" content="{{ robots }}">
<link rel="canonical" href="{{ canonical }}">
<meta name="theme-color" content="#111827">

<meta property="og:type" content="website">
<meta property="og:site_name" content="VDownloader">
<meta property="og:title" content="{{ title }}">
<meta property="og:description" content="{{ description }}">
<meta property="og:url" content="{{ canonical }}">
<meta property="og:image" content="{{ og_image }}">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{{ title }}">
<meta name="twitter:description" content="{{ description }}">
<meta name="twitter:image" content="{{ og_image }}">

{% for s in schemas %}<script type="application/ld+json">{{ s | safe }}</script>
{% endfor %}
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
h1 { font-size: clamp(28px, 6vw, 42px); line-height: 1.2; }
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
input, textarea, select {
  padding: 14px;
  border: 1px solid #cbd5e1;
  border-radius: 9px;
  font-size: 16px;
  font-family: inherit;
}
.input-row input { flex: 1; min-width: 0; }
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
.tool input, .tool textarea, .tool select { width: 100%; margin: 6px 0 12px; }
.tool input[type=checkbox] { width: auto; margin: 0 8px 0 0; }
.tool textarea { resize: vertical; }
.lbl { display: block; font-weight: bold; margin-top: 8px; }
.result {
  background: #eef2ff;
  padding: 12px;
  border-radius: 8px;
  margin: 12px 0;
  overflow-wrap: anywhere;
  white-space: pre-wrap;
}
.result img { max-width: 100%; border-radius: 8px; margin-top: 10px; }
.btns button { margin: 4px 6px 8px 0; }
.tool-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
  gap: 12px;
  margin-top: 15px;
}
.tool-grid a {
  display: block;
  background: #f1f5f9;
  padding: 12px 14px;
  border-radius: 10px;
  text-decoration: none;
  color: #172033;
  font-weight: bold;
  font-size: 15px;
}
.tool-grid a:hover { background: #dbeafe; }
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
  .btns button { width: auto; }
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
      <a href="/tools">Free Tools</a>
      <a href="/blog">Blog</a>
      <a href="/how-to-download-facebook-video">Guide</a>
      <a href="/about">About</a>
      <a href="/contact">Contact</a>
    </nav>
  </div>
</header>
<main>{{ body | safe }}</main>
<footer>
  <div>&copy; <span id="year"></span> VDownloader</div>
  <p>
    <a href="/tools">Free Tools</a>
    <a href="/blog">Blog</a>
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


def render_page(title, description, body, path="/", schema=None,
                robots="index,follow"):
    schemas = [{
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": SITE_NAME,
        "url": SITE_URL
    }]
    for item in (schema or []):
        schemas.append(item)

    safe_schemas = [
        json.dumps(s).replace("</", "<\\/") for s in schemas
    ]

    og_image = SITE_URL + "/static/og-image.png"

    return render_template_string(
        BASE_HTML,
        title=title,
        description=description,
        canonical=SITE_URL + path,
        schemas=safe_schemas,
        robots=robots,
        body=body,
        og_image=og_image
    )


# ---------------- FREE TOOLS (all run in the visitor's browser) ----------------

HELPERS = r"""const $=id=>document.getElementById(id);
const on=(ids,fn)=>{ids.split(',').forEach(i=>$(i).addEventListener('input',fn));fn();};
function copyOut(){const o=$('o');const t=o.value!==undefined?o.value:o.textContent;if(navigator.clipboard){navigator.clipboard.writeText(t);}}
"""

COPY_BTN = '<button type="button" onclick="copyOut()">Copy result</button>'
RESULT = '<div id="o" class="result" aria-live="polite"></div>'


def field(i, label, ph="", kind="text", val="", rows=0, ro=False):
    r = " readonly" if ro else ""
    if rows:
        ctl = ('<textarea id="%s" rows="%d" placeholder="%s" aria-label="%s"%s>'
               '</textarea>' % (i, rows, ph, label, r))
    else:
        v = ' value="%s"' % val if val != "" else ""
        ctl = ('<input id="%s" type="%s" placeholder="%s" aria-label="%s"%s%s>'
               % (i, kind, ph, label, v, r))
    return '<label class="lbl" for="%s">%s</label>%s' % (i, label, ctl)


TOOLS = []


def tool(slug, h1, desc, intro, how, html, js):
    TOOLS.append({
        "slug": slug, "h1": h1, "desc": desc,
        "intro": intro, "how": how, "html": html, "js": js
    })


NOTE = " Everything runs inside your browser, so nothing you type is uploaded."

# 1
tool(
    "youtube-thumbnail-downloader",
    "YouTube Thumbnail Downloader",
    "Get the thumbnail image of any YouTube video in HD, SD and HQ sizes. Free and instant.",
    "Paste a YouTube link to see every available thumbnail size and open the "
    "image in full quality." + NOTE,
    "Copy the YouTube video link, paste it in the box, then open the thumbnail "
    "size you want. Long-press (mobile) or right-click (PC) the image to save it. "
    "Thumbnails belong to their creators, so use them responsibly.",
    field("u", "YouTube video link", "https://www.youtube.com/watch?v=...", "url")
    + RESULT,
    r"""function vid(s){const m=s.match(/(?:youtu\.be\/|v=|shorts\/|embed\/|live\/)([A-Za-z0-9_-]{11})/);return m?m[1]:null}
on('u',()=>{const o=$('o');o.replaceChildren();const v=$('u').value.trim();if(!v){return}
const id=vid(v);if(!id){o.textContent='Please enter a valid YouTube link.';return}
[['maxresdefault','Max quality (1280x720)'],['sddefault','SD quality (640x480)'],['hqdefault','HQ quality (480x360)']].forEach(([n,l])=>{
const url='https://img.youtube.com/vi/'+id+'/'+n+'.jpg';
const d=document.createElement('div');d.style.marginBottom='16px';
const i=document.createElement('img');i.src=url;i.alt=l;i.loading='lazy';
const a=document.createElement('a');a.href=url;a.target='_blank';a.rel='noopener noreferrer';a.textContent='Open '+l;
d.append(a,document.createElement('br'),i);o.append(d);});});"""
)

# ... rest of tools and code remain unchanged ...

import extra_tools
extra_tools.add(tool, field, RESULT, COPY_BTN, NOTE)
import more_tools
more_tools.add(tool, field, RESULT, COPY_BTN, NOTE)

TOOLS_BY_SLUG = {t["slug"]: t for t in TOOLS}

import blog
blog.register(app, render_page, TOOLS_BY_SLUG, SITE_URL)


def tools_grid(items=None):
    items = items or TOOLS
    links = "".join(
        '<a href="/tools/%s">%s</a>' % (t["slug"], escape(t["h1"]))
        for t in items
    )
    return '<div class="tool-grid">' + links + "</div>"


def related_tools(slug):
    index = next(n for n, t in enumerate(TOOLS) if t["slug"] == slug)
    items = [TOOLS[(index + k) % len(TOOLS)] for k in range(1, 7)]
    return tools_grid(items)


@app.route("/tools")
def tools_index():
    body = (
        '<section class="content"><h1>Free Online Tools</h1>'
        "<p>Simple, fast tools for video creators and website owners. "
        "No sign-up needed, and every tool runs inside your browser so "
        "your text and files are not uploaded.</p>"
        + tools_grid() + "</section>"
    )
    return render_page(
        "Free Online Tools for Video Creators | VDownloader",
        "50 free online tools: YouTube thumbnail downloader, hashtag "
        "generator, video size calculator, JSON formatter and more.",
        body, "/tools"
    )


@app.route("/tools/<slug>")
def tool_page(slug):
    t = TOOLS_BY_SLUG.get(slug)
    if not t:
        abort(404)

    path = "/tools/" + slug
    body = (
        '<section class="content"><h1>' + escape(t["h1"]) + "</h1><p>"
        + t["intro"] + "</p></section>"
        '<section class="panel tool">' + t["html"] + "</section>"
        '<section class="content"><h2>How to use</h2><p>' + t["how"] + "</p>"
        "<h2>More free tools</h2>" + related_tools(slug) + "</section>"
        "<script>" + HELPERS + t["js"] + "</script>"
    )
    schema = [{
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": t["h1"],
        "url": SITE_URL + path,
        "description": t["desc"],
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "Any",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    }]
    return render_page(t["h1"] + " | VDownloader", t["desc"], body, path, schema)

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
  <p>Need more help? Read our
  <a href="/how-to-download-facebook-video">step-by-step guide and FAQ</a>.</p>

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

<section class="content">
  <h2>Free Tools for Creators</h2>
  <p>Try our free browser-based tools. <a href="/tools">See all tools</a>.</p>
  <!--TOOLS-->
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


@app.route("/")
def home():
    return render_page(
        "VDownloader - Online Video Downloader",
        "Check supported public video links with VDownloader, "
        "a simple online video information tool.",
        HOME_BODY.replace("<!--TOOLS-->", tools_grid(TOOLS[:8])),
        "/"
    )

# ---------------- GUIDE PAGE WITH FAQ ----------------
# (unchanged)

FAQ = [
    ("Is VDownloader free?",
     "Yes. You can use the video link checker and all tools without paying "
     "or creating an account."),
    ("Can I download private videos?",
     "No. Only public videos can be processed. Private or restricted videos "
     "cannot be accessed."),
    ("Does it work on Android and iPhone?",
     "Yes. VDownloader runs in a normal mobile or desktop browser. On some "
     "phones you may need to open the video and use the browser menu to save it."),
    ("Why does a video say it cannot be accessed?",
     "The video may be private, deleted, region-restricted or from an "
     "unsupported platform. Try another public link."),
    ("Is it legal to download videos?",
     "It depends on the video and your country. Only save videos you own or "
     "have permission to download, and follow each platform's terms."),
]


@app.route("/how-to-download-facebook-video")
def guide():
    faq_html = "".join(
        "<h3>%s</h3><p>%s</p>" % (escape(q), escape(a)) for q, a in FAQ
    )
    body = (
        '<section class="content"><h1>How to Download Facebook Videos</h1>'
        "<p>This guide shows how to check and save a public Facebook video "
        "using VDownloader on your phone or computer. The same steps work "
        "for other supported platforms.</p>"
        "<h2>Step by step</h2><ol>"
        "<li>Open the Facebook video and tap <strong>Share</strong>, then "
        "<strong>Copy link</strong>.</li>"
        "<li>Open <a href=\"/\">VDownloader</a> and paste the link into the box.</li>"
        "<li>Press <strong>Get Video</strong> and wait a few seconds.</li>"
        "<li>When the result appears, press <strong>Open Video</strong>. "
        "Use your browser menu to save the video if the option is shown.</li></ol>"
        "<h2>Tips for better results</h2>"
        "<ul><li>Use the full public link, not a screenshot or a private group link.</li>"
        "<li>If one link fails, try again after a short time.</li>"
        "<li>Short links such as fb.watch also work.</li></ul>"
        "<h2>Frequently asked questions</h2>" + faq_html +
        "<h2>Responsible use</h2><p>Only save content you own or have "
        "permission to use. VDownloader does not host or store videos.</p>"
        "<p>Looking for more utilities? Browse our <a href=\"/tools\">free tools</a>.</p>"
        "</section>"
    )
    schema = [{
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a}
        } for q, a in FAQ]
    }]
    return render_page(
        "How to Download Facebook Videos (Step by Step Guide)",
        "Step-by-step guide to check and save public Facebook videos on "
        "Android, iPhone and PC, with answers to common questions.",
        body, "/how-to-download-facebook-video", schema
    )

# ---------------- INFORMATION PAGES ----------------

PAGES = {
    "/about": {
        "title": "About VDownloader",
        "description": "Learn about VDownloader, its video link tool and free utilities.",
        "body": """
        <section class="content">
          <h1>About VDownloader</h1>
          <p>VDownloader helps users check supported public video links
          and view available video information. We also publish free
          browser-based tools for video creators and website owners.</p>
          <p>VDownloader does not host video content. Use the service
          only with content you own or are permitted to save.</p>
          <p>Questions or feedback? Visit our <a href="/contact">contact page</a>.</p>
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
          <p>Our free tools run in your browser. The text you type into
          them is not sent to our server.</p>
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
            contact_text = "<p>Please use the email provided by the site owner.</p>"

        body = (
            '<section class="content"><h1>Contact VDownloader</h1>' +
            contact_text +
            "<p>For privacy questions, copyright requests, bug reports or "
            "website feedback, send us an email and we will reply as soon "
            "as possible.</p></section>"
        )
    else:
        body = page["body"]

    return render_page(page["title"], page["description"], body, path)


# ---------------- ROBOTS, SITEMAP, 404, REDIRECTS ----------------

@app.before_request
def ensure_www():
    # Redirect requests for the apex (non-www) domain to the preferred
    # www canonical domain using 308 to preserve method and body where applicable.
    host = request.host.split(":")[0].lower()
    if host == "vdownloder.xyz":
        # preserve path and query string
        target = SITE_URL + request.full_path.rstrip("?")
        return redirect(target, code=308)


@app.errorhandler(404)
def not_found(_error):
    body = (
        '<section class="content"><h1>Page not found</h1>'
        '<p>Go to the <a href="/">home page</a> or browse our '
        '<a href="/tools">free tools</a>.</p></section>'
    )
    html = render_page(
        "Page Not Found | VDownloader",
        "The page you requested was not found.",
        body, request.path, robots="noindex,follow"
    )
    return html, 404


@app.route("/robots.txt")
def robots():
    content = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /download\n\n"

        "Sitemap: " + SITE_URL + "/sitemap.xml\n"
    )
    return Response(content, mimetype="text/plain")


@app.route("/sitemap.xml")
def sitemap():
    paths = [
        "/", "/tools", "/how-to-download-facebook-video",
        "/about", "/contact", "/privacy-policy", "/terms"
    ]
    paths += ["/tools/" + t["slug"] for t in TOOLS]
    paths += ["/blog"] + ["/blog/" + p["slug"] for p in blog.POSTS]

    # remove duplicates while preserving order
    seen = set()
    deduped = []
    for p in paths:
        if p not in seen:
            seen.add(p)
            # exclude any empty or non-indexable endpoints
            if p and p != "/download":
                deduped.append(p)

    entries = [
        "<url><loc>" + SITE_URL + p + "</loc>"
        "<lastmod>" + LAST_UPDATED + "</lastmod></url>"
        for p in deduped
    ]

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + "".join(entries) +
        "</urlset>"
    )
    return Response(xml, mimetype="application/xml")


# Serve an Open Graph image at /static/og-image.png. If Pillow is available
# we generate a simple 1200x630 PNG on the fly. This avoids committing a binary
# image file while ensuring the URL exists for social previews.
@app.route("/static/og-image.png")
def og_image():
    if Image is None:
        # Pillow not installed or failed to import; return 1x1 transparent PNG
        transparent_png = (
            b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0bIDATx\x9cc`\x00\x00\x00\x02\x00\x01\xe2!\xbc\x33\x00\x00\x00\x[...]"
        )
        return Response(transparent_png, mimetype="image/png")

    width, height = 1200, 630
    img = Image.new("RGB", (width, height), color=(17,24,39))
    draw = ImageDraw.Draw(img)

    # Draw title text in the centre. Use a default font if truetype is unavailable.
    try:
        font = ImageFont.truetype("arial.ttf", 72)
    except Exception:
        font = ImageFont.load_default()

    text = "VDownloader"
    w, h = draw.textsize(text, font=font)
    draw.text(((width - w) / 2, (height - h) / 2 - 10), text, font=font, fill=(96,165,250))

    subtitle = "Online Video Downloader"
    try:
        font2 = ImageFont.truetype("arial.ttf", 32)
    except Exception:
        font2 = ImageFont.load_default()

    w2, h2 = draw.textsize(subtitle, font=font2)
    draw.text(((width - w2) / 2, (height - h2) / 2 + 50), subtitle, font=font2, fill=(226,232,240))

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return Response(buf.read(), mimetype="image/png")


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
