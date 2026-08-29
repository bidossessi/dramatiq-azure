import dramatiq
import pytest
from azure.core.exceptions import HttpResponseError
from azure.storage.queue import (
    QueueMessage,
    StorageErrorCode,
)

from dramatiq_azure import (
    asq,
    errors,
)


def _http_error(error_code):
    error = HttpResponseError("boom")
    error.error_code = error_code
    return error


def _asq_message(queue_name):
    dramatiq_message = dramatiq.Message(
        queue_name=queue_name, actor_name="test", args=(), kwargs={}, options={}
    )
    queue_message = QueueMessage(content=dramatiq_message.encode())
    return asq._ASQMessage(queue_message, dramatiq_message)


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


def test_nack_translates_storage_errors(broker, queue_name, mocker):
    consumer = asq.ASQConsumer(
        broker,
        asq.ConsumerOptions(
            queue_name=queue_name, prefetch=1, timeout=1000, dead_letter=True
        ),
    )
    mocker.patch.object(
        consumer.dlq_client,
        "send_message",
        side_effect=_http_error(StorageErrorCode.REQUEST_BODY_TOO_LARGE),
    )

    with pytest.raises(errors.MessageTooLarge):
        consumer.nack(_asq_message(queue_name))


def test_requeue_translates_storage_errors(broker, queue_name, mocker):
    consumer = asq.ASQConsumer(
        broker,
        asq.ConsumerOptions(queue_name=queue_name, prefetch=1, timeout=1000),
    )
    mocker.patch.object(
        consumer.q_client,
        "send_message",
        side_effect=_http_error(
            StorageErrorCode.OUT_OF_RANGE_QUERY_PARAMETER_VALUE
        ),
    )

    with pytest.raises(errors.DelayTooLong):
        consumer.requeue([_asq_message(queue_name)])
