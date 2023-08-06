import pytest
from mysqld_integration_test.log import logger
from mysqld_integration_test.exceptions import InvalidLogLevel


@pytest.mark.log_test
def test_log_levelset_noexception():
    logger.setlevel('INFO')
    assert True


@pytest.mark.log_test
def test_log_levelset_fail():
    with pytest.raises(InvalidLogLevel):
        logger.setlevel('FAKE')
    assert True


@pytest.mark.log_test
def test_log_debug_noexception():
    logger.debug("test")
    assert True


@pytest.mark.log_test
def test_log_info_noexception():
    logger.info("test")
    assert True


@pytest.mark.log_test
def test_log_error_noexception():
    logger.error("test")
    assert True


@pytest.mark.log_test
def test_log_success_noexception():
    logger.success("test")
    assert True
