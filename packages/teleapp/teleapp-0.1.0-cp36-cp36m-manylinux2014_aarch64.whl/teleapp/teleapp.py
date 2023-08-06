import click

from teleapp.const.click_setting import CONTEXT_SETTINGS
from teleapp.cmd.cmd import start_cmd


@click.group()
def cli():
    pass


@cli.command('start', short_help='teleapp start', context_settings=CONTEXT_SETTINGS)
def start():
    start_cmd()
