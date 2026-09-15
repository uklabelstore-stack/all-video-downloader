from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import json
import os
import re

app = Flask(__name__)

# Allow Blogger / browser requests
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "success": True,
        "message": "All Video Downloader API is running",
        "endpoint": "/download"
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "success": True,
        "status": "online"
    })


@app.route("/download", methods=["POST", "OPTIONS"])
def download():

    # Browser CORS preflight
    if request.method == "OPTIONS":
        return "", 204

    try:
        data = request.get_json(silent=True) or {}
        video_url = data.get("url", "").strip()

        if not video_url:
            return jsonify({
                "success": False,
                "error": "URL is required"
            }), 400

        # Basic URL validation
        if not re.match(r"^https?://", video_url, re.IGNORECASE):
            return jsonify({
                "success": False,
                "error": "Please enter a valid video URL"
            }), 400

        # yt-dlp command
        command = [
            "yt-dlp",

            # Return JSON only
            "--dump-single-json",

            # Do not download at this stage
            "--skip-download",

            # Prefer MP4-compatible formats
            "-f",
            "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/b",

            # No playlist downloads
            "--no-playlist",

            # Ignore certificate issues
            "--no-check-certificates",

            # Don't use local config files
            "--ignore-config",

            video_url
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=90
        )

        if result.returncode != 0:

            error_message = (
                result.stderr.strip()
                or result.stdout.strip()
                or "Unable to fetch this video."
            )

            return jsonify({
                "success": False,
                "error": error_message[-2000:]
            }), 500

        if not result.stdout.strip():
            return jsonify({
                "success": False,
                "error": "yt-dlp returned no video information."
            }), 500

        meta = json.loads(result.stdout)

        title = meta.get("title") or "Video"
        thumbnail = meta.get("thumbnail")
        download_url = meta.get("url")

        # Sometimes yt-dlp returns formats instead of a top-level URL
        if not download_url:

            formats = meta.get("formats") or []

            # Prefer MP4 video/audio capable format
            mp4_formats = [
                f for f in formats
                if f.get("url")
                and (
                    f.get("ext") == "mp4"
                    or f.get("container") == "mp4"
                )
            ]

            if mp4_formats:
                # Highest quality MP4 format available
                mp4_formats.sort(
                    key=lambda f: (
                        f.get("height") or 0,
                        f.get("tbr") or 0
                    ),
                    reverse=True
                )

                download_url = mp4_formats[0].get("url")

            elif formats:
                # Fallback to best available direct URL
                valid_formats = [
                    f for f in formats
                    if f.get("url")
                ]

                if valid_formats:
                    valid_formats.sort(
                        key=lambda f: (
                            f.get("height") or 0,
                            f.get("tbr") or 0
                        ),
                        reverse=True
                    )

                    download_url = valid_formats[0].get("url")

        if not download_url:
            return jsonify({
                "success": False,
                "error": "No direct downloadable video URL was found. This video may require login, DRM, or may not be supported."
            }), 422

        return jsonify({
            "success": True,
            "title": title,
            "thumbnail": thumbnail,
            "download_url": download_url
        })

    except subprocess.TimeoutExpired:

        return jsonify({
            "success": False,
            "error": "Video fetch timed out. Please try another URL."
        }), 504

    except json.JSONDecodeError:

        return jsonify({
            "success": False,
            "error": "Invalid response received from yt-dlp."
        }), 500

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
                )
