"""
TikTok Trend Finder for hashtags
Author: Pablo & ChatGPT
Purpose:
    - Pull trending TikTok videos
    - Extract hashtags and sounds
    - Filter for Roblox / dance trends
    - Save to CSV for daily reference
    - Print quick summary of top 5 trends
"""

# Install TikTokApi before running:
# pip install TikTokApi pandas

from TikTokApi import TikTokApi
import pandas as pd
from datetime import datetime

# ========== CONFIGURATION ==========
TREND_LIMIT = 50  # Number of videos to fetch
OUTPUT_FOLDER = "./"  # Where to save the CSV report
# ====================================

def fetch_trends_by_hashtag(hashtag):
    """
    Fetches TikTok videos by hashtag.
    """
    api = TikTokApi()
    videos = api.by_hashtag(hashtag, count=TREND_LIMIT)

    data = []
    for video in videos:
        hashtags = [tag['title'] for tag in video.get('challenges', [])]
        sound_name = video.get('music', {}).get('title', "Unknown")
        sound_url = video.get('music', {}).get('playUrl')
        stats = video.get('stats', {})

        data.append({
            "Author": video.get('author', {}).get('uniqueId', "Unknown"),
            "Views": stats.get('playCount', 0),
            "Likes": stats.get('diggCount', 0),
            "Shares": stats.get('shareCount', 0),
            "Hashtags": hashtags,
            "Sound": sound_name,
            "Sound URL": sound_url,
        })

    return data

def save_to_csv(data, hashtag):
    """
    Saves trend data to a CSV file.
    """
    df = pd.DataFrame(data)
    filename = f"{OUTPUT_FOLDER}tiktok_trends_{hashtag}_{datetime.now().strftime('%Y-%m-%d')}.csv"
    df.to_csv(filename, index=False)
    print(f"[✔] Saved trend report to {filename}")

def print_top_summary(data, limit=5):
    """
    Prints the top N trends by views in the console.
    """
    sorted_data = sorted(data, key=lambda x: x["Views"], reverse=True)
    print("\n===== Top Trending TikToks =====")
    for idx, trend in enumerate(sorted_data[:limit], start=1):
        print(f"{idx}. {trend['Sound']} | Views: {trend['Views']:,} | Hashtags: {', '.join(trend['Hashtags'])}")
        if trend['Sound URL']:
            print(f"   🔗 {trend['Sound URL']}")

def main():
    hashtag = input("Enter a hashtag (without #): ").strip()
    print(f"[🔍] Fetching TikToks for #{hashtag} ...")
    trends = fetch_trends_by_hashtag(hashtag)

    print(f"[📊] {len(trends)} total videos fetched for #{hashtag}.")
    save_to_csv(trends, hashtag)
    print_top_summary(trends)

if __name__ == "__main__":
    main()
