import pytest
import functools
from mysqld_integration_test import Mysqld


@pytest.fixture
def mysqld_connect():
    return Mysqld()

def rgetattr(obj, attr, *args):
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split('.'))


def rsetattr(obj, attr, val):
    pre, _, post = attr.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)

# Make sure config options exists and check some defaults
@pytest.mark.config_exists
def test_config_exists(mysqld_connect):
    assert rgetattr(mysqld_connect, 'config') is not None

@pytest.mark.config_exists
def test_basedir_exists(mysqld_connect):
    assert rgetattr(mysqld_connect, 'config.dirs.base_dir') is not None



# Make sure config options are not None
@pytest.mark.config_notnone
def test_basedir_notnone(mysqld_connect):
    assert mysqld_connect.config.dirs.base_dir is not None


