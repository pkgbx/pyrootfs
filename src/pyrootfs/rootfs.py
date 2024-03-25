"""
rootfs utility module.
"""
import os
import hashlib
import pathlib
import shutil
import subprocess
from typing import Any, Dict
from dataclasses import dataclass, field

import canonicaljson
import dictdiffer

from pyrootfs import errors


base_paths = [
    'bin',
    'boot',
    'dev',
    'etc',
    'home',
    'lib',
    'lib64',
    'media',
    'mnt',
    'opt',
    'proc',
    'root',
    'run',
    'sbin',
    'srv',
    'sys',
    'tmp',
    'usr',
    'var',
]


@dataclass
class RootFS:
    """
    RootFS dataclass.
    """
    path: pathlib.Path
    data: Dict[str, Any]
    digest: str = field(init=False)

    def __post_init__(self) -> None:
        """
        Post initialization dataclass method.

        Sets the value of the digest property.
        """
        self.digest = digest(self)

    def __eq__(self, other: 'RootFS') -> bool:
        """
        Compares two rootfs objects using the digest property of each.
        """
        return self.digest == other.digest
    
    def __ne__(self, other: 'RootFS') -> bool:
        """
        Compares two rootfs objects using the digest property of each.
        """
        return self.digest != other.digest


def initialize(path: pathlib.Path) -> RootFS:
    """
    Intializes a new rootfs in "path".
    """
    try:
        os.makedirs(str(path), exist_ok=True)
    except OSError as e:
        raise errors.PyRootFSError(e.strerror, code=e.errno)

    for p in base_paths:
        os.makedirs(f'{path}/{p}', exist_ok=True)

    return RootFS(pathlib.Path(path), read(path))


def read(path: pathlib.Path) -> Dict[str, Any]:
    """
    Read a rootfs dir and return a dictionary with the mapped
    data.

    Directotires are stored as dicts and files as a `pathlib.Path` object.
    """
    data = {}

    for root, dirs, files in os.walk(str(path)):
        current_directory = data

        for directory in os.path.relpath(root, path).split(os.path.sep):
            if directory == '.':
                continue
            full_path = f'{path}/{directory}'
            current_directory = current_directory.setdefault(directory, {}) 

        for filename in files:
            file_path = os.path.join(root, filename)
            current_directory[filename] = pathlib.Path(file_path)
            
    return data


def to_json(rootfs: RootFS, pretty: bool = False) -> str:
    """
    Return the canonical json representation of a rootfs dict structure.
    """
    def cb(p: pathlib.Path) -> str:
        return str(p)
    canonicaljson.register_preserialisation_callback(pathlib.Path, cb)

    if pretty:
        return canonicaljson.encode_pretty_printed_json(rootfs.data).decode()
    
    return canonicaljson.encode_canonical_json(rootfs.data).decode()


def digest(rootfs: RootFS) -> str:
    """
    Return the sha256 digest representation of the rootfs' json data,
    file content is not considered.
    """
    json_data = to_json(rootfs)

    return hashlib.sha256(json_data.encode()).hexdigest()


def archive(rootfs: RootFS, dest: pathlib.Path) -> None:
    """
    Archives rootfs in a tarball to the dest folder.
    """
    cmd = [
        'tar',
        '--sort=name',
        '--mtime=\'@0\'',
        '--xattrs',
        '--pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime',
        '-cvf',
        dest.resolve(), 
        '.'
    ]
    opts = {
        'stdout': subprocess.PIPE,
        'stderr': subprocess.PIPE,
        'universal_newlines': True,
        'cwd': str(rootfs.path)
    }
    
    code = None
    with subprocess.Popen(cmd, **opts) as p:
        out, err = p.communicate()
        yield (out, err)

        code = p.returncode

    return code


def diff(rootfs1: RootFS, rootfs2: RootFS) -> Dict[str, Any]:
    """
    Diffs two rootfs objects and return a dict containig the difference.
    """
    output = {}
    
    for ctx, field, values in dictdiffer.diff(rootfs1.data, rootfs2.data):
        item = output.setdefault(ctx, [])
        
        for value in values:
            k, v = value
            item.append(_diff_parse(f'{field}/{k}', v))
    
    return output


def _diff_parse(field, values, p=''):
    if not p:
        p = f'{field}'
        if not p.startswith('/'):
            p = f'/{p}'

    if type(values) is not dict or len(values) == 0:
        return p
        
    for k, v in values.items():
        if isinstance(v, dict):
            return _diff_add(v, p + f'/{k}')
        else:
            return f'{p}/{k}' 
