import pandas as pd
import os

def load_and_merge():
    print("Loading all raw data...")

    # ── Load each CSV ──────────────────────────────────────────
    youtube = pd.read_csv("data/raw/youtube_US.csv")
    spotify = pd.read_csv("data/raw/spotify_charts.csv")
    lastfm  = pd.read_csv("data/raw/lastfm_united_states.csv")

    print(f"YouTube records  : {len(youtube)}")
    print(f"Spotify records  : {len(spotify)}")
    print(f"Last.fm records  : {len(lastfm)}")

    # ── Normalize column names to a common schema ──────────────
    youtube_clean = pd.DataFrame({
        "platform"       : youtube["platform"],
        "title"          : youtube["title"].str.strip(),
        "artist"         : youtube["channel"].str.strip(),
        "popularity"     : youtube["views"],
        "engagement"     : youtube["likes"],
        "explicit"       : None,
        "release_date"   : youtube["published_at"],
        "chart_position" : range(1, len(youtube) + 1),
        "region"         : youtube["region"]
    })

    spotify_clean = pd.DataFrame({
        "platform"       : spotify["platform"],
        "title"          : spotify["title"].str.strip(),
        "artist"         : spotify["artist"].str.strip(),
        "popularity"     : spotify["popularity"],
        "engagement"     : spotify["duration_ms"],
        "explicit"       : spotify["explicit"],
        "release_date"   : spotify["release_date"],
        "chart_position" : spotify["chart_position"],
        "region"         : "US"
    })

    lastfm_clean = pd.DataFrame({
        "platform"       : lastfm["platform"],
        "title"          : lastfm["title"].str.strip(),
        "artist"         : lastfm["artist"].str.strip(),
        "popularity"     : lastfm["listeners"],
        "engagement"     : lastfm["playcount"],
        "explicit"       : None,
        "release_date"   : None,
        "chart_position" : lastfm["chart_position"],
        "region"         : lastfm["country"]
    })

    # ── Merge all three ────────────────────────────────────────
    master = pd.concat([youtube_clean, spotify_clean, lastfm_clean], ignore_index=True)

    # ── Clean up ───────────────────────────────────────────────
    master["title"]  = master["title"].str.title()
    master["artist"] = master["artist"].str.title()
    master["release_date"] = pd.to_datetime(master["release_date"], errors="coerce")

    # Drop duplicates based on title + artist + platform
    before = len(master)
    master.drop_duplicates(subset=["title", "artist", "platform"], inplace=True)
    after = len(master)
    print(f"\nDuplicates removed: {before - after}")

    # ── Save ───────────────────────────────────────────────────
    os.makedirs("data/processed", exist_ok=True)
    master.to_csv("data/processed/master_music_data.csv", index=False)
    print(f"Master dataset saved: {after} records → data/processed/master_music_data.csv")

    print("\nSample:")
    print(master.head(10).to_string())

    return master

if __name__ == "__main__":
    df = load_and_merge()