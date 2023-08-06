"""Main Generest CLI module."""
__all__ = ('main',)

import click


@click.group(invoke_without_command=True, chain=False)
def main(*a, **b):
    """Generest CLI."""
    pass


@main.command()
def make(*a, **b):
    """Make a REST API module from a config file."""
    pass
