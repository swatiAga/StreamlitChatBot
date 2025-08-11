# Import Regular expression
import re
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
# Load from .env file into environment variables
load_dotenv()
# YouTube API Key (Replace with your own API key)
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")

# Function to validate YouTube channel URL
# def is_valid_youtube_channel(url):
#     pattern = r"(https?:\/\/)?(www\.)?(youtube\.com\/(c\/|channel\/|user\/|@)[a-zA-Z0-9_-]+)"
#     return re.match(pattern, url)

def is_valid_youtube_channel(url):
    pattern = r"^(https?:\/\/)?(www\.)?youtube\.com\/(c\/|channel\/|user\/|@)[a-zA-Z0-9_-]+(\?.*)?$"
    return re.match(pattern, url)

# Function to extract video links from a YouTube channel
def get_video_links(channel_url):
    video_links = []
    
    # Extract channel ID from URL
    # channel_id_match = re.search(r"youtube\.com/(channel|c|user|@)(/[^/?]+)", channel_url)
    # Clean URL: Remove query parameters and trailing slashes
    cleaned_url = channel_url.split("?")[0].rstrip("/")
    channel_id_match = re.search(r"youtube\.com/(channel/|c/|user/|@)([^/?]+)", cleaned_url)
    if not channel_id_match:
        return None  # Invalid URL format
    
    # Extract channel identifier
    channel_identifier = channel_id_match.group(2).strip("/")
    
    # Initialize YouTube API
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    # Get channel details
    request = youtube.search().list(
        part="snippet",
        q=channel_identifier,
        type="channel",
        maxResults=1
    )
    response = request.execute()

    if "items" in response and response["items"]:
        channel_id = response["items"][0]["id"]["channelId"]
    else:
        return None  # Channel not found

    # Get video uploads
    request = youtube.search().list(
        part="id",
        channelId=channel_id,
        maxResults = os.environ["YOU_TUBE_LINKS_TO_PULL"],  # Adjust as needed
        order="date"
    )
    response = request.execute()

    # Extract video links
    for item in response["items"]:
        if "videoId" in item["id"]:
            video_links.append(f"https://www.youtube.com/watch?v={item['id']['videoId']}")

    return video_links