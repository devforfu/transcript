import click
import whisper

from transcript import CACHE_DIR


def download_all_models():
    click.echo("Downloading Whisper models")
    for model_name in whisper.available_models():
        model_path = CACHE_DIR.joinpath(f"{model_name}.pt")
        if model_path.exists():
            click.echo(f"Model {model_name} already exists")
        else:
            click.echo(f"Downloading model {model_name}...")
            whisper.load_model(model_name, download_root=str(CACHE_DIR))
    click.echo("Done!")
