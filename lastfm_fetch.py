import requests
import pandas as pd
import os
from config import LASTFM_API_KEY

BASE_URL = "http://ws.audioscrobbler.com/2.0/"

def fetch_top_tracks(country="united states", limit=50):
    print(f"Fetching Last.fm top tracks for: {country}...")
    
    params = {
        "method": "geo.gettoptracks",
        "country": country,
        "api_key": LASTFM_API_KEY,
        "format": "json",
        "limit": limit
    }
    
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    if "error" in data:
        print(f"Last.fm API Error: {data['message']}")
        return None
    
    records = []
    tracks = data.get("tracks", {}).get("track", [])
    
    for idx, track in enumerate(tracks):
        records.append({
            "platform": "Last.fm",
            "title": track.get("name"),
            "artist": track.get("artist", {}).get("name"),
            "listeners": int(track.get("listeners", 0)),
            "playcount": int(track.get("playcount", 0)),
            "country": country,
            "chart_position": idx + 1
        })
    
    df = pd.DataFrame(records)
    
    os.makedirs("data/raw", exist_ok=True)
    filename = f"data/raw/lastfm_{country.replace(' ', '_')}.csv"
    df.to_csv(filename, index=False)
    print(f"Saved {len(df)} records to {filename}")
    
    return df

if __name__ == "__main__":
    df = fetch_top_tracks(country="united states", limit=50)
    if df is not None:
        print(df.head())