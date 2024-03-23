import pytest

from pyrootfs import errors


def test_baserror():
    e = errors.PyRootFSError('foobar', code=2)

    with pytest.raises(errors.PyRootFSError):
        raise e

    assert '[ERR] foobar' == str(e)
    assert 'PyRootFSError("foobar", code=2)' == repr(e)
