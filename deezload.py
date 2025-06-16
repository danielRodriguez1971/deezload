import os
import requests
import feedparser
from urllib.parse import urlparse

class PodcastDownloader:
    def __init__(self, rss_url, download_dir="downloads"):
        self.rss_url = rss_url
        self.download_dir = download_dir
        os.makedirs(self.download_dir, exist_ok=True)

    def fetch_feed(self):
        self.feed = feedparser.parse(self.rss_url)
        if self.feed.bozo:
            raise ValueError("Invalid RSS feed or parsing error.")

    def list_episodes(self):
        return [(entry.title, entry.enclosures[0].href) for entry in self.feed.entries if entry.enclosures]

    def download_all(self):
        self.fetch_feed()
        for entry in self.feed.entries:
            if not entry.enclosures:
                continue  # skip if no media
            url = entry.enclosures[0].href
            filename = self._get_filename(url)
            self._download_file(url, filename)

    def _get_filename(self, url):
        path = urlparse(url).path
        filename = os.path.basename(path)
        return os.path.join(self.download_dir, filename)

    def _download_file(self, url, filename):
        print(f"Downloading: {filename}")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Finished: {filename}")

# Example usage (once initialized, no external URL argument needed anymore)
# downloader = PodcastDownloader("https://example.com/podcast/feed.xml")
# downloader.download_all()


if __main__ == __name__
    new = PodcastDownloader()
    https://dzr.page.link/gDJPSq5dFuRVytLy8