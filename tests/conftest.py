import pytest
from click.testing import CliRunner


@pytest.fixture
def clirunner():
    return CliRunner()
