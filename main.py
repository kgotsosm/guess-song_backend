from fastapi import FastAPI, HTTPException
import os
from dotenv import load_dotenv
import requests
import base64

app = FastAPI()
load_dotenv()

# Load Spotify credentials from environment variables
spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

# Spotify API endpoints
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com/v1"

# Function to get an access token from Spotify
def get_spotify_token():
    auth_header = base64.b64encode(f"{spotify_client_id}:{spotify_client_secret}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_header}"
    }
    data = {
        "grant_type": "client_credentials"
    }
    response = requests.post(SPOTIFY_TOKEN_URL, headers=headers, data=data)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to authenticate with Spotify")
    return response.json().get("access_token")


@app.get("/kendrick-lamar-tracks")
async def get_kendrick_lamar_tracks():
    access_token = get_spotify_token()
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # Search for Kendrick Lamar tracks
    search_url = f"{SPOTIFY_API_BASE_URL}/search"
    params = {
        "q": "artist:Kendrick Lamar",
        "type": "track",
        "limit": 50,  # Maximum number of tracks to retrieve
        "market": "US"  # US market
    }
    response = requests.get(search_url, headers=headers, params=params)

    # Handle rate limits
    if response.status_code == 429:
        retry_after = int(response.headers.get("Retry-After", 1))
        raise HTTPException(status_code=429, detail=f"Rate limit exceeded. Retry after {retry_after} seconds.")
    elif response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch tracks from Spotify")

    tracks = response.json().get("tracks", {}).get("items", [])

    # Include all tracks and remove "available_markets" for relevant results object
    formatted_tracks = [
        {
            "name": track["name"],
            "preview_url": track.get("preview_url"),
            "track_id": track["id"],
            "album": track["album"]["name"],
            "release_date": track["album"]["release_date"],
            "popularity": track["popularity"],
        }
        for track in tracks
    ]

    return {"tracks": formatted_tracks}

# Get Beyonce tracks

@app.get("/beyonce-tracks")
async def get_beyonce_tracks():
    access_token = get_spotify_token()
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # Search for Beyonce tracks
    search_url = f"{SPOTIFY_API_BASE_URL}/search"
    params = {
        "q": "artist:Beyonce",
        "type": "track",
        "limit": 50,  # Maximum number of tracks to retrieve
        "market": "US"  # US market
    }
    response = requests.get(search_url, headers=headers, params=params)

    # Handle rate limits
    if response.status_code == 429:
        retry_after = int(response.headers.get("Retry-After", 1))
        raise HTTPException(status_code=429, detail=f"Rate limit exceeded. Retry after {retry_after} seconds.")
    elif response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch tracks from Spotify")

    tracks = response.json().get("tracks", {}).get("items", [])

    # Include all tracks and remove "available_markets" for relevant results object
    formatted_tracks = [
        {
            "name": track["name"],
            "preview_url": track.get("preview_url"),
            "track_id": track["id"],
            "album": track["album"]["name"],
            "release_date": track["album"]["release_date"],
            "popularity": track["popularity"],
        }
        for track in tracks
    ]

    return {"tracks": formatted_tracks}
