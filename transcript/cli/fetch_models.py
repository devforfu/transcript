import click
import whisper

def fetch_models():
    click.echo("Getting all Whisper models")
    for model in whisper.available_models():
        click.echo(f"Fetching model: {model}")
    click.echo("Done")