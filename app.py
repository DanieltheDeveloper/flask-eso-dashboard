from flask import Flask, render_template
from flask_caching import Cache
from api_routes import api_v1_blueprint  # Import the blueprint

app = Flask(__name__, static_folder='static')

# Register the blueprint for API routes
app.register_blueprint(api_v1_blueprint, url_prefix="/api/v1")

@app.route("/")
def home():
    return render_template("dashboard.html")