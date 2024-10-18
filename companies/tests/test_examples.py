import pytest
import logging


@pytest.mark.xfail
def test_should_be_ok_if_fails() -> None:
    assert 1 == 2


@pytest.mark.skip
def test_should_be_skipped() -> None:
    assert 1 == 2


def raise_covid19_exception() -> None:
    raise ValueError('Coronavirus Exception')


def test_raise_covid19_exception_should_pass() -> None:
    with pytest.raises(ValueError) as ex:
        raise_covid19_exception()

    assert str(ex.value) == 'Coronavirus Exception'


logger = logging.getLogger('CORONA_LOGS')


def function_that_logs_something() -> None:
    try:
        raise ValueError('Coronavirus Exception')
    except ValueError as e:
        logger.warning(f'I am logging: {str(e)}')


def test_logged_warning_level(caplog) -> None:
    function_that_logs_something()
    assert 'I am logging: Coronavirus Exception' in caplog.text


def test_logged_info_level(caplog) -> None:
    with caplog.at_level(logging.INFO):
        logger.info('I am logging info level')
        assert 'I am logging info level' in caplog.text
