# -*- coding: utf-8 -*-
import click

from sncopy import VERSION
from sncopy.convert import slack2notion


@click.command()
@click.option('-m', '--mode', type=str, required=False, help='paste mode; None or `bullet` or `number`', default=None)
@click.version_option(VERSION)
def main(mode):
    """Copy-Paste Tool from Slack to Notion"""
    slack2notion(mode)



if __name__ == "__main__":
    main()