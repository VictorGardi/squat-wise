import time
from uuid import uuid4

import requests
import youtube_transcript_api


def main():
    channel_id = "UCyPYQTT20IgzVw92LDvtClw"  # Squat University YouTube channel ID
    api_key = "AIzaSyASCLOtiLbW_qP5z5ziIGaSjFZ8cipYQes"  # Replace with your actual YouTube API key
    yt = YoutubeTranscriber(api_key)
    yt.transcribe_videos_in_channel(channel_id)


class YoutubeTranscriber:
    def __init__(self, api_key: str) -> None:
        self._api_key = api_key
        self._base_url = "https://www.googleapis.com/youtube/v3/search"

    def get_video_ids(self, channel_id: str, limit: int = 100000) -> list[str]:
        ids: list[str] = []
        next_page_token = None

        while True:
            params = {
                'key': self._api_key,
                'channelId': channel_id,
                'part': 'id',
                'order': 'date',
                'maxResults': 50,
                'type': 'video'
            }
            if next_page_token:
                params['pageToken'] = next_page_token

            response = requests.get(self._base_url, params=params)
            data = response.json()
            breakpoint()

            ids.extend([i["id"]["videoId"] for i in data.get("items", [])])

            next_page_token = data.get('nextPageToken')
            if not next_page_token or len(ids) > limit:
                break

            time.sleep(0.5)  # To avoid hitting API rate limits

        return ids 

    @staticmethod
    def transcribe(video_id: str) -> str:
        try:
            transcript = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(video_id)
            return ' '.join([entry['text'] for entry in transcript])
        except Exception:
            #print(f"Error getting transcript for video {video_id}: {str(e)}")
            return ""

    def transcribe_videos_in_channel(self, channel_id: str, limit: int = 100000) -> list[str]:
        transcripts = []
        video_ids = self.get_video_ids(channel_id, limit)
        for video in video_ids:
            data = {
                "id": uuid4(),
                "title": "test",

            }
            transcripts.append(self.transcribe(video))
            time.sleep(0.5)
        return transcripts
        




if __name__ == "__main__":
    main()
