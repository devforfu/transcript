import time
from pathlib import Path
from pytube import Playlist, YouTube


def download(output_dir: str = "data/videos"):
    download_playlist(get_playlist_url(), output_dir)


def download_playlist(url: str, output_dir: str, throttling: float = 0.1):
    playlist = Playlist(url)
    n_videos = len(playlist)
    for i, link in enumerate(playlist, 1):
        lecture = YouTube(link)
        stream = lecture.streams.filter(mime_type="audio/mp4").asc().first()
        print(f"[{i:02d}/{n_videos:02d}] Downloading: {stream.title}...")
        stream.download(output_path=output_dir, skip_existing=True, max_retries=3)
        time.sleep(throttling)


def get_playlist_url() -> str:
    return Path("data/fastai2022.txt").read_text().strip()


if __name__ == '__main__':
    download()

