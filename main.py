from flask import Flask, request, jsonify, Response, render_template_string, redirect, abort
from werkzeug.middleware.proxy_fix import ProxyFix
from urllib.parse import urlparse
from html import escape
import json
import os
import yt_dlp
import io

# Vercel sits in front of Flask and forwards the original request metadata.
# Trust the proxy headers so canonical redirects and path-based routes behave correctly.
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)

SITE_URL = "https://www.vdownloder.xyz"
SITE_NAME = "VDownloader"
CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "uklabelstore@gmail.com").strip()
LAST_UPDATED = "2026-10-17"  # change this date when you add or edit pages

app.config["JSON_SORT_KEYS"] = False
