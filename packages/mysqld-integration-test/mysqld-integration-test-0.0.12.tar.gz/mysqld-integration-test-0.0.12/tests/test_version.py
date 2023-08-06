import pytest
from mysqld_integration_test.version import __version__

def test_version_isnotnone():
    assert __version__ is not None

def test_version_semver():
    assert len(__version__.split('.')) == 3
