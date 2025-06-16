import os
import re
from pytubefix import YouTube
from pytubefix.cli import on_progress
from pytubefix.oauth import get_token

# Ensure output path exists
OUTPUT_PATH = "audios"
os.makedirs(OUTPUT_PATH, exist_ok=True)

def sanitize_filename(title: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "", title)

def download_youtube_audio(video_url: str) -> str:
    """
    Downloads audio from a YouTube video using pytubefix with OAuth.
    Returns the path to the downloaded audio file.
    """

    # Use OAuth token (it will open browser the first time)
    token = get_token(client_secrets_file="client_secrets.json")
    
    yt = YouTube(video_url, on_progress_callback=on_progress, use_po_token=True, token=token)
    
    print(f"\n🎬 Video Title: {yt.title}")
    safe_title = sanitize_filename(yt.title)
    audio_file_name = f"{safe_title}.mp3"

    stream = yt.streams.get_audio_only()
    if not stream:
        raise Exception("No suitable audio stream found.")
    
    print("⬇️ Starting download...")
    audio_path = stream.download(output_path=OUTPUT_PATH, filename=audio_file_name)
    
    print(f"✅ Downloaded audio to: {audio_path}")
    return audio_path

def main():
    url = input("🔗 Enter YouTube URL: ")
    try:
        audio_path = download_youtube_audio(url)
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
