from pathlib import Path

CACHE_DIR = Path("~/.cache/whisper").expanduser()


def model_path(name: str) -> Path:
    return CACHE_DIR.joinpath(f"{name}.pt")


def model_exists(name: str) -> bool:
    return model_path(name).exists()
