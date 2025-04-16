"""Flask application entry point."""

from flask import Flask, render_template
from extensions import cache  # Import the cache object
from api_routes import api_v1_blueprint  # Import the blueprint

app = Flask(__name__, static_folder='static')

cache.init_app(app, config={'CACHE_TYPE': 'SimpleCache'})

# Register the blueprint for API routes
app.register_blueprint(api_v1_blueprint, url_prefix="/api/v1")

@app.route("/")
def home():
    """Home page route."""
    return render_template("dashboard.html")
