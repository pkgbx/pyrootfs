import os
import pathlib
import shutil

import click

from . import rootfs


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
@click.option('-p', '--pretty', is_flag=True, help='prints formatted json if used')
def inspect(path: pathlib.Path, pretty: bool) -> None:
    """
    Inspect an existing rootfs in "path".
    """

    o = rootfs.RootFS(path, rootfs.read(path))

    click.echo(rootfs.to_json(o, pretty=pretty))


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
@click.argument('path', type=click.Path(exists=True, path_type=pathlib.Path))
@click.argument('dest', type=click.Path(path_type=pathlib.Path))
def snapshot(path: pathlib.Path, dest: pathlib.Path) -> None:
    """
    Snapshots rootfs from "path" into a "dest" file.

    The "dest" directory tree will be created if it does not exist.

    The snapshot is written as a tar file, which is why
    it needs the "tar" cli to be available.
    """
    if not path.is_dir():
        return click.echo(f'{path} is not a directory', err=True)
    if not dest.parent.is_dir():
        os.makedirs(dest.parent.resolve(), exist_ok=True)
    if not shutil.which('tar'):
        return click.echo('Could not find "tar" in PATH', err=True)

    o = rootfs.RootFS(path, rootfs.read(path)) 
    proc = rootfs.archive(o, dest)
    for out, err in proc:
        if out is not None:
            click.echo(out, nl=False)
        if err is not None:
            click.echo(err, err=True, nl=False)


def run():
    cli()
