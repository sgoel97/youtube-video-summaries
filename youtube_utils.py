from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from datetime import datetime, timedelta

def get_top_videos(search_term, num_weeks, max_results, developer_key):
    # Create a YouTube service object
    youtube = build("youtube", "v3", developerKey=developer_key)

    # Calculate the date `num_weeks` days ago
    num_weeks_ago = datetime.now() - timedelta(weeks=num_weeks)
    # Format it appropriately for the API request
    published_after = num_weeks_ago.isoformat("T") + "Z"

    # Make an API request to search for videos matching the `search_term` published in the last `num_weeks`
    search_response = youtube.search().list(
        q=search_term,
        type="video",
        order="viewCount",
        publishedAfter=published_after,
        maxResults=max_results,
        part="id,snippet"
    ).execute()
    
    videos = []
    for search_result in search_response.get("items", []):
        videos.append({
            'Title': search_result['snippet']['title'],
            'URL': f'https://www.youtube.com/watch?v={search_result["id"]["videoId"]}',
            'Id': search_result["id"]["videoId"]
        })
            
    return videos

def get_transcript_from_video_id(video_id):
    try:
        # Fetch the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        entries = []
        for entry in transcript:
            entries.append(entry['text'])
        text = ' '.join(entries)
        
        return text

    except Exception as e:
        return None