import pytest
from mysqld_integration_test import Mysqld
from mysqld_integration_test.helpers import Utils


@pytest.fixture
def mysqld_connect(autouse=True):
    return Mysqld()


@pytest.fixture
def version_mariadb():
    return "mysqld  Ver 10.5.16-MariaDB for Linux on x86_64 (MariaDB Server)"


@pytest.fixture
def version_mysql():
    return "/usr/sbin/mysqld  Ver 8.0.32-0ubuntu0.20.04.2 for Linux on x86_64 ((Ubuntu))"


@pytest.mark.helper_test
def test_find_program():
    mysqld_location = Utils.find_program("mysqld")
    assert mysqld_location is not None


@pytest.mark.helper_test
def test_unused_port_isnum():
    port = Utils.get_unused_port()
    assert isinstance(port, int)


@pytest.mark.helper_test
def test_unused_port_isinrange():
    port = Utils.get_unused_port()
    assert ((port > 1024) and (port < 65535))


# Test for MariaDB variant
@pytest.mark.helper_test
def test_parse_version_mariadb_variant(version_mariadb):
    (variant, version_major, version_minor) = Utils.parse_version(version_mariadb)
    assert variant == "mariadb"


# Test for MariaD Bversion major number, also verifies it is an integer
@pytest.mark.helper_test
def test_parse_version_mariadb_major(version_mariadb):
    (variant, version_major, version_minor) = Utils.parse_version(version_mariadb)
    assert version_major == 10


# Test for MariaDB minor version
@pytest.mark.helper_test
def test_parse_version_mariadb_minor(version_mariadb):
    (variant, version_major, version_minor) = Utils.parse_version(version_mariadb)
    assert version_minor == '5.16'


# Test for MySQL variant
@pytest.mark.helper_test
def test_parse_version_mysql_variant(version_mysql):
    (variant, version_major, version_minor) = Utils.parse_version(version_mysql)
    assert variant == "mysql"


# Test for MySQL version major number, also verifies it is an integer
@pytest.mark.helper_test
def test_parse_version_mysql_major(version_mysql):
    (variant, version_major, version_minor) = Utils.parse_version(version_mysql)
    assert version_major == 8


# Test for MySQL minor version
@pytest.mark.helper_test
def test_parse_version_mysql_minor(version_mysql):
    (variant, version_major, version_minor) = Utils.parse_version(version_mysql)
    assert version_minor == '0.32'
