import click
from fastcore.basics import defaults

from transcript.download import download_channel


@click.pass_context
@click.option("--channel-url", required=True, type=str)
@click.option("--output-dir", default="data/streams", type=str)
@click.option("--mime-type", default="audio/mp4", type=str)
def download(ctx, channel_url: str, output_dir: str, mime_type: str) -> None:
    click.echo(f"Downloading channel: {channel_url}")
    n_workers = 0 if ctx.obj["DEBUG"] else defaults.cpus
    download_channel(channel_url, output_dir, mime_type, n_workers)
    click.echo(f"Output directory: {output_dir}")
