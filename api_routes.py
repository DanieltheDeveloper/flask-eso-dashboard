"""Setup API routes and cache for ESO server status and player counts."""

from typing import Dict
import requests
from fastapi import APIRouter, HTTPException
from bs4 import BeautifulSoup
from cachetools import cached  # Import cached from cachetools
from extensions import cache, cacheLong  # Import cache from extensions

# Create API router instead of Blueprint
router = APIRouter()

ESO_SERVER_REGIONS = ["PC-EU", "PC-NA", "PC-PTS", "XBOX-EU", "XBOX-NA", "PS4-NA", "PS4-EU"]
STEAM_CHART_COUNTS = ["current", "24-peak", "all-time-peak"]

# ESO server status route
def get_servers() -> Dict[str, str]:
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

# Cache for ESO server status
# ESO server status route
@cached(cacheLong)
@router.get("/eso_servers")
async def eso_servers() -> Dict[str, str]:
    """ESO server status route."""
    return get_servers()

# Cache for ESO current players
# ESO current players route
@cached(cache)
@router.get("/eso_current_players")
async def eso_current_players() -> Dict[str, int]:
    """Function fetching player count from Steam API."""
    url = "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid=306130"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data.get("response") and "player_count" in data["response"]:
            return {"player_count": data["response"]["player_count"]}
        return {"error": "Unexpected API response"}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

# Steam Charts player count route
def get_steam_charts_player_count() -> Dict[str, str]:
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

# Cache for Steam Charts player count
# Steam Charts player count route
@cached(cache)
@router.get("/steam_charts_player_count")
async def steam_charts_player_count() -> Dict[str, str]:
    """Steam charts player count route."""
    return get_steam_charts_player_count()
