"""Setup API routes and cache for ESO server status and player counts."""

from flask import Blueprint, jsonify
import requests
from bs4 import BeautifulSoup
from extensions import cache

api_v1_blueprint = Blueprint("api_v1", __name__)

ESO_SERVER_REGIONS = ["PC-EU", "PC-NA", "PC-PTS", "XBOX-EU", "XBOX-NA", "PS4-NA", "PS4-EU"]
STEAM_CHART_COUNTS = ["current", "24-peak", "all-time-peak"]

@cache.cached(timeout=120, key_prefix='eso_servers')
def get_servers():
    """Function fetching ESO server status."""
    url = "https://esoserverstatus.net/"
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')
    servers = {}

    for region in ESO_SERVER_REGIONS:
        item = soup.select_one("#" + region)
        if not item:
            continue
        status = item.find('b').get_text(strip=True) if item else "Unknown"
        servers[region] = status

    return servers

@api_v1_blueprint.route("/eso_servers")
def eso_servers():
    """ESO server status route."""
    return jsonify(get_servers())

@cache.cached(timeout=600, key_prefix='eso_current_players')
@api_v1_blueprint.route("/eso_current_players")
def eso_current_players():
    """Function fetching player count from Steam API."""
    url = "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid=306130"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data.get("response") and "player_count" in data["response"]:
            player_count = data["response"]["player_count"]
        else:
            player_count = "Error: Unexpected API response"
    except requests.exceptions.RequestException as e:
        player_count = f"Error: {str(e)}"

    return jsonify(player_count)

@cache.cached(timeout=600, key_prefix='steam_charts_current_players')
def get_steam_charts_player_count():
    """Function fetching player count from Steam Charts."""
    url = "https://steamcharts.com/app/306130"
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')
    steam_charts_players = {}

    heading = soup.select_one("#app-heading")
    if heading:
        nums = heading.find_all("span", class_="num")
        if nums:
            for idx, stat in enumerate(nums):
                steam_charts_players[STEAM_CHART_COUNTS[idx]] = stat.get_text(strip=True)

    return steam_charts_players

@api_v1_blueprint.route("/steam_charts_player_count")
def steam_charts_player_count():
    """Steam charts player count route."""
    return jsonify(get_steam_charts_player_count())
