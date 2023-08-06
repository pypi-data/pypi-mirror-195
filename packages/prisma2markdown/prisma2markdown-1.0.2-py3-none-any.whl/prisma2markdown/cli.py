"""Command line interface for prisma2markdown."""
import os

import click

from .workflow import update_markdown, create_markdown


@click.group()
def prisma2mermaid():
    """Main entry group"""


@click.command()
@click.option("--prisma-target", help="Path to the prisma schema.")
@click.option(
    "--markdown-target",
    help="Path to markdown to be updated."
    " If not set, the target will have the same name as the prisma target",
)
@click.option(
    "--force", is_flag=True, help="Set the if you wish to forced overwrite of markdown target."
)
def generate(prisma_target: os.PathLike, markdown_target: os.PathLike, force: bool):
    """Generate a mermaid schema from a prisma schema."""
    create_markdown(prisma_target, markdown_target, force)


@click.command()
@click.option("--markdown-target", help="Path to markdown to be updated.")
@click.option(
    "--mock",
    is_flag=True,
    help="Set this option if you wish to check output if another file first.",
)
def update(markdown_target: os.PathLike, mock):
    """Given a markdown target, update to mermaid schema with relation to its prisma schema."""
    update_markdown(markdown_target, mock)


prisma2mermaid.add_command(generate)
prisma2mermaid.add_command(update)
