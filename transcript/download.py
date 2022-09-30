from __future__ import annotations

import io
import json
import time
from dataclasses import dataclass
from xml.etree import ElementTree

from fastcore.basics import defaults
from fastcore.parallel import parallel
from pytube import Caption, Channel, YouTube


def download_channel(
    channel_url: str,
    output_dir: str = "data/streams",
    mime_type: str = "audio/mp4",
    n_workers: int = defaults.cpus,
) -> None:
    channel = Channel(channel_url)
    worker = DownloadJob(output_dir, mime_type)
    parallel(worker, list(channel), progress=True, threadpool=True, n_workers=n_workers)


@dataclass
class DownloadJob:
    output_dir: str
    mime_type: str
    max_retries: int = 10
    skip_existing: bool = True

    def __call__(self, link: str) -> None:
        if video := self._download_video(link):
            self._download_caption(video)

    def _download_video(self, link) -> YouTube | None:
        n_attempts, wait = 10, 0.05
        while n_attempts > 0:
            try:
                video = YouTube(link)
                audio = video.streams.filter(mime_type=self.mime_type).desc().first()
                audio.download(
                    output_path=self.output_dir,
                    max_retries=self.max_retries,
                    skip_existing=self.skip_existing
                )
            except ConnectionResetError:
                time.sleep(wait)
                wait *= 2
                n_attempts -= 1
            else:
                return video
        return None

    def _download_caption(self, video: YouTube, language: str = "en") -> None:
        if caption := video.captions.get(language):
            parsed = parse_caption(caption)
            with open(f"{self.output_dir}/{video.title}.json", "w") as fp:
                json.dump(parsed, fp)


def parse_caption(caption: Caption) -> list[dict]:
    tree = ElementTree.parse(io.StringIO(caption.xml_captions)).getroot()
    return [{"text": el.text, **el.attrib} for el in tree.findall("body/p")]