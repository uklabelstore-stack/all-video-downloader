from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json(silent=True) or {}
    url = data.get('url', '').strip()

    if not url:
        return jsonify({"success": False, "error": "No URL provided"}), 400

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'best',
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 '
                           '(KHTML, like Gecko) Chrome/126.0 Mobile Safari/537.36'
        },
        'extractor_args': {
            'tiktok': {'api_hostname': 'api22-normal-c-useast2a.tiktokv.com'}
        },
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
        # Extraction failed (blocked, invalid URL, private video, etc.)
        return jsonify({"success": False, "error": str(e)}), 200

    except Exception as e:
        # Catch-all so the server NEVER crashes with a raw 500 again
        return jsonify({"success": False, "error": "Server error: " + str(e)}), 200        meta = json.loads(result.stdout)

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
