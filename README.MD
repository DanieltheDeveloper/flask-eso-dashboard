# Flask ESO Dashboard

Simple Flask ESO dashboard with caching support for local deployment

You can find a demo here: https://flask-eso-dashboard.onrender.com/

![Project Overview](readme.png)

## Features

- ESO player count, server status and RSS feed from ESO hub.
- Versioned API.
- Easy to extend and customize.

## Requirements

- Python 3.7 or higher
- Flask

## Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd flask-eso-dashboard
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the Flask application:
    ```bash
    flask run
    ```

2. Open your browser and navigate to `http://127.0.0.1:5000`.

## Project Structure

Here is an overview of the project structure:

```
flask-eso-dashboard/
├── app.py                 # Main Flask application
├── api_routes.py          # API v1 routes
├── extensions.py          # Add extensions like cache to app
├── .github/workflows/     # GitHub workflows
│   └── pylint.yml         # Pylint
├── templates/             # HTML templates for the app
│   └── dashboard.html     # Main dashboard page
├── static/                # Static assets (CSS, JS, images, videos)
│   └── background-video.mp4
├── .vscode/               # VS Code configuration files
│   └── launch.json        # Debugging configuration
├── .gitattributes         # Git LFS file
├── .gitignore             # Git ignore file
├── requirements.txt       # Python dependencies
├── LICENSE                # MIT license
├── README.md              # Project documentation
└── readme.png             # Project overview
```

This structure ensures clarity and ease of navigation for developers.

## License

This project is licensed under the MIT License.

## Legal

Elder Scrolls Online, SteamCharts, Steam, and all associated logos and designs are trademarks or registered trademarks of their respective owners.  
This project is not affiliated with ZeniMax Online Studios, Bethesda Softworks, Steam, or any of their family of sites.
