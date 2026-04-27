import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import os
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

def fetch_spotify_data():
    print("Connecting to Spotify...")

    auth_manager = SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # Top artists to pull data from
    artists = [
        "Taylor Swift", "The Weeknd", "Drake", "Billie Eilish",
        "Bad Bunny", "Ed Sheeran", "Ariana Grande", "Post Malone",
        "Dua Lipa", "Harry Styles"
    ]

    records = []

    for artist_name in artists:
        print(f"Fetching top tracks for: {artist_name}...")

        # Search for artist
        result = sp.search(q=artist_name, type="artist", limit=1)
        items = result["artists"]["items"]
        if not items:
            continue

        artist = items[0]
        artist_id = artist["id"]

        # Get their top tracks
        top_tracks = sp.artist_top_tracks(artist_id, country="US")

        for idx, track in enumerate(top_tracks["tracks"]):
            records.append({
                "platform":      "Spotify",
                "track_id":      track["id"],
                "title":         track["name"],
                "artist":        artist_name,
                "album":         track["album"]["name"],
                "popularity":    track["popularity"],
                "duration_ms":   track["duration_ms"],
                "explicit":      track["explicit"],
                "release_date":  track["album"]["release_date"],
                "chart_position": idx + 1
            })

    df = pd.DataFrame(records)

    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/spotify_charts.csv", index=False)
    print(f"Saved {len(df)} records to data/raw/spotify_charts.csv")

    return df

if __name__ == "__main__":
    df = fetch_spotify_data()
    if df is not None:
        print(df.head())