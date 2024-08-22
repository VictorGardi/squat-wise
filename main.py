import json
import os

from article_scraper import scrape
from youtube_transcriber import YoutubeTranscriber

SQUAT_UNI_CHANNEL_ID = "UCyPYQTT20IgzVw92LDvtClw"
YT_API_KEY = os.environ.get("YT_API_KEY", "")
ARTICLE_LIMIT = 10000
VIDEO_LIMIT = 10

def generate_dataset():
    yt = YoutubeTranscriber(YT_API_KEY)
    # list with strings. One video -> one item in list
    #transcripts = yt.transcribe_videos_in_channel(channel_id=SQUAT_UNI_CHANNEL_ID, limit=VIDEO_LIMIT)
    # list with strings. One sentence/section of a sentence -> one item in list
    articles = scrape(limit=ARTICLE_LIMIT)
    with open('squat_university_data.json', 'w') as f:
        json.dump(articles, f, indent=2)
    
if __name__ == "__main__":
    generate_dataset()


