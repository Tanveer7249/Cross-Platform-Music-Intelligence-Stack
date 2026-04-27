import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def run_analytics():
    print("Loading master dataset...")
    df = pd.read_csv("data/processed/master_music_data.csv")
    os.makedirs("data/processed/charts", exist_ok=True)

    print(f"Total records: {len(df)}")
    print(f"Platforms    : {df['platform'].unique()}")

    # ── 1. Records per platform ────────────────────────────────
    platform_counts = df.groupby("platform").size().reset_index(name="track_count")
    print("\n── Records per platform ──")
    print(platform_counts)

    # ── 2. Top 10 artists by popularity ───────────────────────
    top_artists = (
        df.groupby("artist")["popularity"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    top_artists.columns = ["artist", "avg_popularity"]
    print("\n── Top 10 artists by avg popularity ──")
    print(top_artists)

    # ── 3. Platform avg popularity comparison ─────────────────
    platform_popularity = (
        df.groupby("platform")["popularity"]
        .mean()
        .reset_index()
    )
    platform_popularity.columns = ["platform", "avg_popularity"]
    print("\n── Avg popularity per platform ──")
    print(platform_popularity)

    # ── 4. Explicit content breakdown ─────────────────────────
    explicit_df = df[df["explicit"].notna()].copy()
    explicit_df["explicit"] = explicit_df["explicit"].astype(str)
    explicit_counts = explicit_df.groupby("explicit").size().reset_index(name="count")
    print("\n── Explicit content breakdown ──")
    print(explicit_counts)

    # ── 5. Cross-platform artist overlap ──────────────────────
    platform_artists = df.groupby("platform")["artist"].apply(set)
    platforms = list(platform_artists.index)
    print("\n── Cross-platform artist overlap ──")
    for i in range(len(platforms)):
        for j in range(i+1, len(platforms)):
            overlap = platform_artists[platforms[i]] & platform_artists[platforms[j]]
            print(f"{platforms[i]} ∩ {platforms[j]}: {len(overlap)} artists → {list(overlap)[:5]}")

    # ── 6. Engagement rate (engagement / popularity) ──────────
    df["engagement_rate"] = df["engagement"] / (df["popularity"] + 1)
    top_engagement = (
        df[df["platform"] == "YouTube"]
        .nlargest(10, "engagement_rate")[["title", "artist", "engagement_rate"]]
    )
    print("\n── Top 10 YouTube tracks by engagement rate ──")
    print(top_engagement)

    # ── Save analytics summary ─────────────────────────────────
    summary = {
        "total_records"         : len(df),
        "platforms"             : df["platform"].nunique(),
        "unique_artists"        : df["artist"].nunique(),
        "avg_popularity_youtube": round(float(df[df["platform"]=="YouTube"]["popularity"].mean()), 2),
        "avg_popularity_spotify": round(float(df[df["platform"]=="Spotify"]["popularity"].mean()), 2),
        "avg_popularity_lastfm" : round(float(df[df["platform"]=="Last.fm"]["popularity"].mean()), 2),
    }
    summary_df = pd.DataFrame([summary])
    summary_df.to_csv("data/processed/analytics_summary.csv", index=False)
    print("\n── Analytics summary saved ──")
    print(summary_df)

    # ── 7. Charts ──────────────────────────────────────────────
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Cross-Platform Music Intelligence Dashboard", fontsize=16, fontweight="bold")

    # Chart 1: Records per platform
    axes[0,0].bar(platform_counts["platform"], platform_counts["track_count"],
                  color=["#FF6B6B","#4ECDC4","#45B7D1"])
    axes[0,0].set_title("Track Count by Platform")
    axes[0,0].set_ylabel("Number of Tracks")

    # Chart 2: Top 10 artists
    axes[0,1].barh(top_artists["artist"][::-1], top_artists["avg_popularity"][::-1],
                   color="#FF6B6B")
    axes[0,1].set_title("Top 10 Artists by Avg Popularity")
    axes[0,1].set_xlabel("Avg Popularity Score")

    # Chart 3: Avg popularity per platform
    axes[1,0].bar(platform_popularity["platform"], platform_popularity["avg_popularity"],
                  color=["#FF6B6B","#4ECDC4","#45B7D1"])
    axes[1,0].set_title("Avg Popularity Score by Platform")
    axes[1,0].set_ylabel("Avg Popularity")

    # Chart 4: Explicit vs clean
    if not explicit_counts.empty:
        axes[1,1].pie(explicit_counts["count"], labels=explicit_counts["explicit"],
                      autopct="%1.1f%%", colors=["#FF6B6B","#4ECDC4"])
        axes[1,1].set_title("Explicit vs Clean Tracks (Spotify)")

    plt.tight_layout()
    chart_path = "data/processed/charts/music_dashboard.png"
    plt.savefig(chart_path, dpi=150, bbox_inches="tight")
    print(f"\nChart saved → {chart_path}")
    plt.show()

    return df

if __name__ == "__main__":
    df = run_analytics()