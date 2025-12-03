import dramatiq
import pytest
from azure.storage.queue import QueueMessage

from dramatiq_azure import asq


def test_type_guard_accepts_asq_message():
    dramatiq_message = dramatiq.Message(
        queue_name="test", actor_name="test", args=(), kwargs={}, options={}
    )
    queue_message = QueueMessage(content=dramatiq_message.encode())
    asq_message = asq._ASQMessage(queue_message, dramatiq_message)

    assert asq._is_asq_message(asq_message) is True


def test_type_guard_rejects_base_message_proxy():
    dramatiq_message = dramatiq.Message(
        queue_name="test", actor_name="test", args=(), kwargs={}, options={}
    )
    message_proxy = dramatiq.MessageProxy(dramatiq_message)

    assert asq._is_asq_message(message_proxy) is False


def test_consumer_ack_requires_asq_message(broker, queue_name):
    consumer = asq.ASQConsumer(
        broker,
        asq.ConsumerOptions(queue_name=queue_name, prefetch=1, timeout=1000),
    )

    dramatiq_message = dramatiq.Message(
        queue_name=queue_name, actor_name="test", args=(), kwargs={}, options={}
    )
    invalid_message = dramatiq.MessageProxy(dramatiq_message)

    with pytest.raises(
        AssertionError, match="ASQConsumer requires _ASQMessage"
    ):
        consumer.ack(invalid_message)


def test_consumer_nack_requires_asq_message(broker, queue_name):
    consumer = asq.ASQConsumer(
        broker,
        asq.ConsumerOptions(
            queue_name=queue_name, prefetch=1, timeout=1000, dead_letter=True
        ),
    )

    dramatiq_message = dramatiq.Message(
        queue_name=queue_name, actor_name="test", args=(), kwargs={}, options={}
    )
    invalid_message = dramatiq.MessageProxy(dramatiq_message)

    with pytest.raises(
        AssertionError, match="ASQConsumer requires _ASQMessage"
    ):
        consumer.nack(invalid_message)


def test_consumer_requeue_requires_asq_message(broker, queue_name):
    consumer = asq.ASQConsumer(
        broker,
        asq.ConsumerOptions(queue_name=queue_name, prefetch=1, timeout=1000),
    )

    dramatiq_message = dramatiq.Message(
        queue_name=queue_name, actor_name="test", args=(), kwargs={}, options={}
    )
    invalid_message = dramatiq.MessageProxy(dramatiq_message)

    with pytest.raises(
        AssertionError, match="ASQConsumer requires _ASQMessage"
    ):
        consumer.requeue([invalid_message])
