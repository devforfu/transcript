import json
import math
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path

from fastcore.basics import chunked, defaults
from fastcore.parallel import parallel

import whisper
from transcript import model_exists
from whisper import DecodingOptions, Whisper


def transcribe_all(
    audio_dir: str,
    output_dir: str,
    model_name: str = "base",
    extension: str = "mp4",
    device: str = "cuda",
    n_workers: int = defaults.cpus,
    decoding_options: DecodingOptions = DecodingOptions(),
) -> None:
    audio_files = list(Path(audio_dir).glob(f"*.{extension}"))
    os.makedirs(output_dir, exist_ok=True)
    worker = TranscribeJob(model_name, output_dir, decoding_options, device)
    parallel(worker, chunks(audio_files, n_workers),
             progress=True, method="spawn", n_workers=n_workers)


def chunks(paths: list[Path], n_workers: int) -> list[tuple[Path, ...]]:
    n_total = len(paths)
    chunk_size = math.ceil(n_total / n_workers) if n_workers > 0 else n_total
    return list(chunked(paths, chunk_sz=chunk_size))


@dataclass
class TranscribeJob:
    model_name: str
    output_dir: str
    decoding_options: DecodingOptions
    device: str
    model_instance: Whisper = field(init=False)

    def __post_init__(self):
        assert model_exists(self.model_name), f"download model {self.model_name} before using parallel execution"

    def __call__(self, paths: tuple[Path, ...]) -> None:
        model = whisper.load_model(name=self.model_name, device=self.device)
        options = asdict(self.decoding_options)
        for path in paths:
            self._transcribe_one(model, path, **options)

    def _transcribe_one(self, model: Whisper, path: Path, **options) -> None:
        result = model.transcribe(str(path), **options)
        output_path = f"{self.output_dir}/{path.stem}.json"
        Path(output_path).write_text(json.dumps(result["segments"]))
