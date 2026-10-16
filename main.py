from flask import Flask, request, jsonify, Response, render_template_string
from flask_cors import CORS
from datetime import datetime, timezone
from urllib.parse import urlparse
from html import escape
import json
import os
import yt_dlp

app = Flask(__name__)
CORS(app)

SITE_URL = "https://vdownloder.xyz"
SITE_NAME = "VDownloader"
CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "").strip()

# ---------------- HTML TEMPLATE ----------------

BASE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>{{ title }}</title>
    <meta name="description" content="{{ description }}">
    <meta name="robots" content="index, follow">
    <meta name="theme-color" content="#111827">

    <link rel="canonical" href="{{ canonical }}">

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
            background: #f5f7fb;
            color: #172033;
            line-height: 1.7;
        }

        header {
            background: #111827;
            padding: 18px 20px;
            color: white;
        }

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

        nav {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
        }

        nav a {
            color: white;
            text-decoration: none;
            font-size: 14px;
        }

        nav a:hover { color: #60a5fa; }

        main {
            max-width: 900px;
            min-height: 60vh;
            margin: 45px auto;
            padding: 0 18px;
        }

        .hero { text-align: center; }

        h1 {
            font-size: clamp(30px, 6vw, 46px);
            line-height: 1.2;
        }

        h2 { line-height: 1.35; }

        .subtitle {
            color: #64748b;
            font-size: 17px;
        }

        .panel, .content {
            background: white;
            margin-top: 25px;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 8px 30px #1720330d;
        }

        .input-row {
            display: flex;
            gap: 10px;
        }

        input {
            flex: 1;
            min-width: 0;
            padding: 15px;
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

        button:disabled {
            opacity: 0.6;
            cursor: wait;
        }

        #status {
            margin-top: 15px;
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
            background: #16a34a;
            color: white;
            text-decoration: none;
            padding: 12px 18px;
            margin-top: 10px;
            border-radius: 8px;
            font-weight: bold;
        }

        a { overflow-wrap: anywhere; }

        footer {
            text-align: center;
            padding: 25px 15px;
            color: #64748b;
            font-size: 14px;
        }

        footer a {
            color: #475569;
            margin: 0 7px;
        }

        @media (max-width: 600px) {
            main { margin: 28px auto; }
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

<main>
    {{ body | safe }}
</main>

<footer>
    <div>
        &copy; <span id="year"></span> VDownloader
    </div>

    <p>
        <a href="/about">About Us</a>
        <a href="/contact">Contact</a>
        <a href="/privacy-policy">Privacy Policy</a>
        <a href="/terms">Terms of Service</a>
    </p>
</footer>

<script>
document.getElementById("year").textContent =
    new Date().getFullYear();
</script>
</body>
</html>
"""

# ---------------- HOME PAGE ----------------

HOME_BODY = """
<section class="hero">
    <h1>Online Video Downloader</h1>

    <p class="subtitle">
        Paste a supported public video link to check video availability.
    </p>
</section>

<section class="panel">
    <form id="downloadForm">
        <div class="input-row">
            <input
                id="videoUrl"
                type="url"
                placeholder="Paste video URL here..."
                aria-label="Video URL"
                required
            >

            <button id="submitBtn" type="submit">
                Get Video
            </button>
        </div>
    </form>

    <div id="status" role="status" aria-live="polite"></div>
    <div id="result"></div>
</section>

<section class="content">
    <h2>How to Use VDownloader</h2>

    <ol>
        <li>Copy a supported public video URL.</li>
        <li>Paste the link into the input box.</li>
        <li>Click Get Video and wait for the result.</li>
        <li>Open the returned video link if available.</li>
    </ol>

    <h2>Use Videos Responsibly</h2>

    <p>
        Only download videos you own or have permission to save.
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
            throw new Error(
                data.error || "Unable to process this video."
            );
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

            link.href = data
