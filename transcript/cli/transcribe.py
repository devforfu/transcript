from datetime import timedelta
from timeit import default_timer as timer

import click
from fastcore.basics import defaults

from transcript.transcribe import transcribe_all
from whisper import DecodingOptions


@click.pass_context
@click.option("--audio-dir", required=True, type=str)
@click.option("--output-dir", required=True, type=str)
@click.option("--model-name", default="base", type=str)
@click.option("--language", default="en", type=str)
@click.option("--extension", default="mp4", type=str)
@click.option("--device", default="cuda", type=str)
@click.option("--n-workers", default=defaults.cpus, type=int)
@click.option("--fp16/--no-fp16", default=True)
def transcribe(
    ctx,
    audio_dir: str,
    output_dir: str,
    model_name: str,
    language: str,
    extension: str,
    device: str,
    n_workers: int,
    fp16: bool,
) -> None:
    click.echo(f"Transcribing audio files from dir: {audio_dir}")
    started = timer()
    transcribe_all(
        audio_dir,
        output_dir,
        model_name,
        extension=extension,
        device=device,
        n_workers=0 if ctx.obj["DEBUG"] else n_workers,
        decoding_options=DecodingOptions(language=language, fp16=fp16),
    )
    elapsed = timedelta(seconds=timer() - started)
    click.echo(f"Processing time: {elapsed}")
