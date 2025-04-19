"""Flask application entry point."""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from extensions import cache, cached  # Import the cache and cached decorator

from api_routes import router  # Import the router

# Create a Jinja2 template instance
templates = Jinja2Templates(directory="templates")

# Create application instance
app = FastAPI(title="ESO Dashboard",
              summary="Simple ESO dashboard with caching support for local deployment",
              version="1.0"
              )

# Mount the static folder to the app
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include the router with prefix
app.include_router(router, prefix="/api/v1")

# Define the cache for the root route
@cached(cache)
# Root route for the dashboard
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Home page route."""
    return templates.TemplateResponse(
          name="dashboard.html", context={}, request=request
      )
