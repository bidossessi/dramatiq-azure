import dramatiq
from azure.core.exceptions import HttpResponseError
from azure.storage.queue import StorageErrorCode

from dramatiq_azure import errors


def _http_error(error_code):
    error = HttpResponseError("boom")
    error.error_code = error_code
    return error


def test_errors_are_broker_errors():
    assert issubclass(errors.ASQError, dramatiq.errors.BrokerError)
    assert issubclass(errors.MessageTooLarge, errors.ASQError)
    assert issubclass(errors.DelayTooLong, errors.ASQError)


def test_translate_maps_oversized_message():
    error = _http_error(StorageErrorCode.REQUEST_BODY_TOO_LARGE)

    assert isinstance(errors.translate(error), errors.MessageTooLarge)


def test_translate_maps_out_of_range_delay():
    error = _http_error(StorageErrorCode.OUT_OF_RANGE_QUERY_PARAMETER_VALUE)

    assert isinstance(errors.translate(error), errors.DelayTooLong)


def test_translate_falls_back_on_unknown_code():
    error = _http_error(StorageErrorCode.AUTHENTICATION_FAILED)

    assert type(errors.translate(error)) is errors.ASQError


def test_translate_falls_back_without_code():
    assert type(errors.translate(HttpResponseError("boom"))) is errors.ASQError
