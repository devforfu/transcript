import click
from transcript.cli.download import download


@click.group()
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def cli(ctx, debug: bool) -> None:
    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = debug
    if debug: click.echo("Debug mode is on")


cli.command(download)
