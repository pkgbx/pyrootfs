import os
import uuid

import pytest
from click.testing import CliRunner


@pytest.fixture
def basedir():
    return os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def fixturedir(basedir):
    return f'{basedir}/fixtures'


@pytest.fixture
def testdir(basedir):
    return f'{basedir}/testdir'


@pytest.fixture
def clirunner():
    return CliRunner()


@pytest.fixture
def uid():
    return str(uuid.uuid4())
