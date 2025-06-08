import os
import re
import requests
import feedparser
from tqdm import tqdm
from urllib.parse import urlparse
from bs4 import BeautifulSoup

class RSSFeedHandler:
    def __init__(self, user_input, download_dir='downloads'):
        self.user_input = user_input.strip()
        self.download_dir = download_dir
        self.rss_url = self.identify_rss_feed(self.user_input) if not self.user_input.endswith('.xml') else self.user_input

    def sanitize_filename(self, name):
        return re.sub(r'[^a-zA-Z0-9\-_ ]', '', name).strip().replace(' ', '_')

    def download_file(self, url, output_path):
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

    def identify_rss_feed(self, page_url):
        try:
            response = requests.get(page_url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            for link in soup.find_all('link', type='application/rss+xml'):
                href = link.get('href')
                if href:
                    return href
        except Exception as e:
            print(f"Error identifying RSS feed: {e}")
        return None

    def process_feed(self, feed, folder_path):
        for entry in feed.entries:
            episode_title = self.sanitize_filename(entry.get('title', 'episode'))
            media_url = entry.enclosures[0].href if entry.enclosures else None
            if not media_url:
                continue

            ext = os.path.splitext(urlparse(media_url).path)[-1] or '.mp3'
            filename = f"{episode_title}{ext}"
            filepath = os.path.join(folder_path, filename)

            if not os.path.exists(filepath):
                print(f"Downloading: {episode_title}")
                try:
                    self.download_file(media_url, filepath)
                except Exception as e:
                    print(f"Failed to download {episode_title}: {e}")
            else:
                print(f"Already downloaded: {episode_title}")

    def find_next_link(self, feed):
        if 'links' in feed.feed:
            for link in feed.feed.links:
                if link.rel == 'next':
                    return link.href
        return None

    def download_all(self):
        if not self.rss_url:
            print("Could not identify RSS feed.")
            return

        print(f"Using RSS feed: {self.rss_url}")
        next_url = self.rss_url
        first_feed = feedparser.parse(next_url)
        podcast_title = self.sanitize_filename(first_feed.feed.get('title', 'podcast'))
        folder_path = os.path.join(self.download_dir, podcast_title)
        os.makedirs(folder_path, exist_ok=True)

        while next_url:
            feed = feedparser.parse(next_url)
            self.process_feed(feed, folder_path)
            next_url = self.find_next_link(feed)

if __name__ == '__main__':
    user_input = input("Enter podcast RSS feed URL or podcast page URL: ")
    handler = RSSFeedHandler(user_input)
    handler.download_all()