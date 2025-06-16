import os
import requests
import feedparser
from urllib.parse import urlparse

class PodcastDownloader:
    def __init__(self, rss_url: str = 'https://localhost/no-url-secure', download_dir="downloads"):
        self.rss_url = rss_url
        self.download_dir = download_dir
        self.filename = f'{self.download_dir}/liste.xml'
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
            filename = self._get_filename()
            self._download_file(self.filename)

    def _create_request(self):
        path = f'{self.download_dir}/request'
        reques_file = os.path.basename(path)
        return os.path.join(self.download_dir)

    def _download_file(self):
        print(f"Downloading: {self.filename}")
        response = requests.post(self.rss_url, stream=True)
        response.raise_for_status()
        with open(self._get_filenamefilename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Finished: {self.filename}")

# Example usage (once initialized, no external URL argument needed anymore)
# downloader = PodcastDownloader("https://example.com/podcast/feed.xml")
# downloader.download_all()


if __name__ == "__main__":
    new = PodcastDownloader()
    new.rss_url = "https://media.deezer.com/v1/get_url"
    new._get_filename()
    new._download_file()