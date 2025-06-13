import feedparser
import requests
import os

class PodcastDownloader:
    def __init__(self, rss_url, download_dir="downloads"):
        self.rss_url = rss_url
        self.download_dir = download_dir
        os.makedirs(self.download_dir, exist_ok=True)
        self.feed = None

    def fetch_feed(self):
        self.feed = feedparser.parse(self.rss_url)
        if self.feed.bozo:
            raise ValueError("Invalid RSS feed")
        return self.feed

    def list_episodes(self):
        if not self.feed:
            self.fetch_feed()
        return [
            {
                "title": entry.title,
                "url": entry.enclosures[0].href if entry.enclosures else None,
                "published": entry.published
            }
            for entry in self.feed.entries
        ]

    def download_episode(self, episode):
        url = episode["url"]
        if not url:
            print(f"No audio URL found for episode: {episode['title']}")
            return
        
        filename = os.path.basename(url)
        local_path = os.path.join(self.download_dir, filename)
        
        if os.path.exists(local_path):
            print(f"Already downloaded: {filename}")
            return
        
        print(f"Downloading {episode['title']}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        
        print(f"Downloaded: {filename}")

    def download_all(self):
        episodes = self.list_episodes()
        for ep in episodes:
            self.download_episode(ep)

