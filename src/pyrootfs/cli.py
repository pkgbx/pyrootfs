import click


@click.group
def cli() -> None:
    pass


@cli.command
def version():
    """
    Shows pyrootfs' version.
    """
    click.echo('v0.1.0')


@cli.command
@click.argument('path', type=click.Path())
def init(path: str):
    """
    Initializes a new (minimal) rootfs directory.

    It won't do anything in case the structure to be created
    already exists in "path".
    """
    click.echo(f'Initializing a new rootfs at "{path}"...')


@cli.command
@click.argument('path', type=click.Path(exists=True))
def inspect(path: str) -> None:
    """
    Inspect an existing rootfs in "path".
    """
    click.echo(f'Inspecting "{path}"...')


@cli.command
@click.argument('path1', type=click.Path(exists=True))
@click.argument('path2', type=click.Path(exists=True))
def diff(path1: str, path2: str) -> None:
    """
    Prints the difference between two rootfs
    directories "path1" and "path2".
    """
    click.echo(f'Comparing "{path1}" and "{path2}"...')


@cli.command
@click.argument('path', type=click.Path(exists=True))
@click.argument('dest', type=click.Path(exists=True))
def snapshot(path: str, dest: str) -> None:
    """
    Snapshots rootfs from "path" into a directory "dest"
    which must already exist.

    The snapshot is written  as a tar.gz file and will increment
    its filename (rootfs.$n.tar.gz) accordingly.
    """
    click.echo(f'Snapshot "{path}" to "{dest}"')


def run():
    cli()
