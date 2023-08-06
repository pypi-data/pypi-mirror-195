from mysqld_integration_test import Mysqld
import os
import pytest


@pytest.mark.mysqld_test
def test_mysqld_init():
    mysqld = Mysqld()
    assert mysqld.base_dir is not None


@pytest.mark.mysqld_test
def test_mysqld_tmpdir_delete():
    mysqld = Mysqld()
    base_dir = mysqld.base_dir
    mysqld.close()
    assert not os.path.exists(base_dir)
