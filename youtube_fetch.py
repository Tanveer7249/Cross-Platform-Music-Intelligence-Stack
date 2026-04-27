import requests
import pandas as pd
import os
from config import YOUTUBE_API_KEY
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_trending_music(region_code="US", max_results=50):
    print(f"Fetching YouTube trending music for region: {region_code}...")
    
    url = "https://www.googleapis.com/youtube/v3/videos"
    
    params = {
        "part": "snippet,statistics,contentDetails",
        "chart": "mostPopular",
        "videoCategoryId": "10",  # 10 = Music category
        "regionCode": region_code,
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY
    }
    
    response = requests.get(url, params=params, verify=False)
    data = response.json()
    
    if "error" in data:
        print(f"YouTube API Error: {data['error']['message']}")
        return None
    
    records = []
    for item in data.get("items", []):
        snippet = item.get("snippet", {})
        stats = item.get("statistics", {})
        
        records.append({
            "platform": "YouTube",
            "video_id": item.get("id"),
            "title": snippet.get("title"),
            "channel": snippet.get("channelTitle"),
            "published_at": snippet.get("publishedAt"),
            "views": int(stats.get("viewCount", 0)),
            "likes": int(stats.get("likeCount", 0)),
            "comments": int(stats.get("commentCount", 0)),
            "region": region_code
        })
    
    df = pd.DataFrame(records)
    
    os.makedirs("data/raw", exist_ok=True)
    df.to_csv(f"data/raw/youtube_{region_code}.csv", index=False)
    print(f"Saved {len(df)} records to data/raw/youtube_{region_code}.csv")
    
    return df

if __name__ == "__main__":
    df = fetch_trending_music(region_code="US", max_results=50)
    if df is not None:
        print(df.head())