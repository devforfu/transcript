import click
from transcript.download import download_channel


# create click commands with sub-commands
@click.group()
def cli():
    pass

