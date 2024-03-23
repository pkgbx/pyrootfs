from pyrootfs.cli import cli


def test_version(clirunner):
    res = clirunner.invoke(cli, ['version'])

    assert res.exit_code == 0
    assert res.output == 'v0.1.0\n'
