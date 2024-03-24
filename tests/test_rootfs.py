import os
import json
import shutil
import pathlib

from pyrootfs import rootfs


def test_initialize_empty_ok(testdir, uid):
    path = f'{testdir}/{uid}'
    r = rootfs.initialize(path)

    assert os.path.isdir(path)
    assert r.path == pathlib.Path(path)
    assert r.data['usr'] == {}
    assert r.digest == '5bf67f0f33f44ae801871e79bd489d26819b2dfbef06ba46cc2edde1630c27b3'

    shutil.rmtree(path)


def test_initialize_existing_ok(testdir, uid):
    path = f'{testdir}/{uid}'
    os.makedirs(path, exist_ok=True)

    r = rootfs.initialize(path)

    assert os.path.isdir(path)
    assert r.path == pathlib.Path(path)
    assert r.data['usr'] == {}
    assert r.digest == '5bf67f0f33f44ae801871e79bd489d26819b2dfbef06ba46cc2edde1630c27b3'

    shutil.rmtree(path)


def test_read_ok(fixturedir):
    path = pathlib.Path(f'{fixturedir}/rootfs')
    data = rootfs.read(path)
    
    assert data['etc']['containers']['storage.conf'] == pathlib.Path(f'{path}/etc/containers/storage.conf')
    assert data['etc']['containers']['systemd']['a.kube'] == pathlib.Path(f'{path}/etc/containers/systemd/a.kube')
    assert data['usr'] == {}


def test_to_json_ok(fixturedir):
    path = pathlib.Path(f'{fixturedir}/rootfs')
    r = rootfs.RootFS(path, rootfs.read(path))

    json_data = json.loads(rootfs.to_json(r))

    assert json_data['etc']['containers']['storage.conf'] == str(r.data['etc']['containers']['storage.conf'])


def test_digest(fixturedir):
    path = pathlib.Path(f'{fixturedir}/rootfs')
    r = rootfs.RootFS(path, rootfs.read(path))

    assert rootfs.digest(r) == '2653f035f098deb915d592fc4275c2424486b21a71afe6b7685b800380ab8769'
