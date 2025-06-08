import os
import re
import requests
import feedparser
from tqdm import tqdm
from urllib.parse import urlparse

def sanitize_filename(name):
    return re.sub(r'[^a-zA-Z0-9\-_ ]', '', name).strip().replace(' ', '_')

def download_file(url, output_path):
    response = requests.get(url, stream=True)
    total = int(response.headers.get('content-length', 0))

    with open(output_path, 'wb') as file, tqdm(
        desc=os.path.basename(output_path),
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)

def download_podcast(rss_url, download_dir='downloads'):
    feed = feedparser.parse(rss_url)
    podcast_title = sanitize_filename(feed.feed.get('title', 'podcast'))
    folder_path = os.path.join(download_dir, podcast_title)
    os.makedirs(folder_path, exist_ok=True)

    for entry in feed.entries:
        episode_title = sanitize_filename(entry.get('title', 'episode'))
        media_url = entry.enclosures[0].href if entry.enclosures else None
        if not media_url:
            continue

        ext = os.path.splitext(urlparse(media_url).path)[-1] or '.mp3'
        filename = f"{episode_title}{ext}"
        filepath = os.path.join(folder_path, filename)

        if not os.path.exists(filepath):
            print(f"Downloading: {episode_title}")
            try:
                download_file(media_url, filepath)
            except Exception as e:
                print(f"Failed to download {episode_title}: {e}")
        else:
            print(f"Already downloaded: {episode_title}")

if __name__ == '__main__':
    rss_url = input("Enter podcast RSS feed URL: ").strip()
    download_podcast(rss_url)
