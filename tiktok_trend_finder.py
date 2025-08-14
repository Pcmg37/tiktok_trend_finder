"""
TikTok Trend Finder for Roblox + Dance Content
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
TREND_LIMIT = 50  # Number of trending videos to fetch
FILTER_KEYWORDS = []  # Keywords to filter trends, e.g. ["roblox", "dance", "gaming"]
while True:
    keyword = str(input("Enter a keyword, x to stop: "))
    if keyword.lower() == 'x':
        break
    else:
        FILTER_KEYWORDS.append(keyword)
OUTPUT_FOLDER = "./"  # Where to save the CSV report
# ====================================

def contains_keywords(text, keywords):
    """
    Checks if any keyword appears in the given text (case-insensitive).
    Returns True if at least one match is found.
    """
    text_lower = text.lower()
    return any(keyword.lower() in text_lower for keyword in keywords)

def fetch_trends():
    """
    Connects to TikTokApi and fetches trending videos.
    Extracts author, stats, hashtags, sound info.
    Returns a list of dictionaries for each video.
    """
    api = TikTokApi.get_instance()

    # Fetch trending videos
    trending_videos = api.trending(count=TREND_LIMIT)

    data = []
    for video in trending_videos:
        hashtags = [tag['title'] for tag in video['challenges']] if 'challenges' in video else []
        sound_name = video['music']['title'] if 'music' in video else "Unknown"
        sound_url = video['music']['playUrl'] if 'music' in video else None
        stats = video['stats'] if 'stats' in video else {}

        # Combine hashtags into one string for easy filtering
        all_text = " ".join(hashtags) + " " + sound_name

        data.append({
            "Author": video['author']['uniqueId'] if 'author' in video else "Unknown",
            "Views": stats.get('playCount', 0),
            "Likes": stats.get('diggCount', 0),
            "Shares": stats.get('shareCount', 0),
            "Hashtags": hashtags,
            "Sound": sound_name,
            "Sound URL": sound_url,
            "AllText": all_text
        })

    return data

def filter_trends(data):
    """
    Filters trend data for Roblox / dance related trends.
    Returns a filtered list of dictionaries.
    """
    return [item for item in data if contains_keywords(item["AllText"], FILTER_KEYWORDS)]

def save_to_csv(data):
    """
    Saves trend data to a CSV file.
    """
    df = pd.DataFrame(data)
    filename = f"{OUTPUT_FOLDER}tiktok_trends_{datetime.now().strftime('%Y-%m-%d')}.csv"
    df.to_csv(filename, index=False)
    print(f"[✔] Saved trend report to {filename}")

def print_top_summary(data, limit=5):
    """
    Prints the top N trends by views in the console.
    """
    sorted_data = sorted(data, key=lambda x: x["Views"], reverse=True)
    print("\n===== Top Trending Roblox/Dance TikToks =====")
    for idx, trend in enumerate(sorted_data[:limit], start=1):
        print(f"{idx}. {trend['Sound']} | Views: {trend['Views']:,} | Hashtags: {', '.join(trend['Hashtags'])}")
        if trend['Sound URL']:
            print(f"   🔗 {trend['Sound URL']}")

def main():
    print("[🔍] Fetching trending TikToks...")
    trends = fetch_trends()

    print(f"[📊] {len(trends)} total trends fetched.")
    filtered_trends = filter_trends(trends)
    print(f"[🎯] {len(filtered_trends)} trends match Roblox/dance keywords.")

    save_to_csv(filtered_trends)
    print_top_summary(filtered_trends)

if __name__ == "__main__":
    main()
