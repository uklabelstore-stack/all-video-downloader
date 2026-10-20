from main import app

# Vercel serverless entrypoint for the Flask app.
# The root app instance is defined in main.py and is reused here to ensure
# that all routes (including /robots.txt and /sitemap.xml) run through Flask.
