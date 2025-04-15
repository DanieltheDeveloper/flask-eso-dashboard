from flask import Blueprint, jsonify
import requests
from bs4 import BeautifulSoup
from extensions import cache

api_v1_blueprint = Blueprint("api_v1", __name__)

ESO_SERVER_REGIONS = ["PC-EU", "PC-NA", "PC-PTS", "XBOX-EU", "XBOX-NA", "PS4-NA", "PS4-EU"]
STEAM_CHART_COUNTS = ["current", "24-peak", "all-time-peak"]

@cache.cached(timeout=120, key_prefix='eso_servers')
def get_servers():
    url = "https://esoserverstatus.net/"
    response = requests.get(url)
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
def servers():
    return jsonify(get_servers())

@cache.cached(timeout=600, key_prefix='eso_current_players')
@api_v1_blueprint.route("/eso_current_players")
def eso_current_players():
    url = "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid=306130"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("response") and "player_count" in data["response"]:
            player_count = data["response"]["player_count"]
        else:
            player_count = "Error: Unexpected API response"
    except Exception as e:
        player_count = f"Error: {str(e)}"

    return jsonify(player_count)

@cache.cached(timeout=600, key_prefix='steam_charts_current_players')
def get_steam_charts_player_count():
    url = "https://steamcharts.com/app/306130"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    eso_current_players = {}

    heading = soup.select_one("#app-heading")
    if heading:
        nums = heading.find_all("span", class_="num")
        if nums:
            for idx, stat in enumerate(nums):
                eso_current_players[STEAM_CHART_COUNTS[idx]] = stat.get_text(strip=True)

    return eso_current_players

@api_v1_blueprint.route("/steam_charts_player_count")
def steam_charts_player_count():
    return jsonify(get_steam_charts_player_count())