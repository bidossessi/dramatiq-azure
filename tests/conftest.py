import random
import string

import dramatiq
import pytest
from dramatiq.middleware import (
    AgeLimit,
    Callbacks,
    Pipelines,
    Retries,
    TimeLimit,
)

from dramatiq_azure import asq


@pytest.fixture
def broker():
    broker = asq.ASQBroker(
        dead_letter=True,
        middleware=[
            AgeLimit(),
            TimeLimit(),
            Callbacks(),
            Pipelines(),
            Retries(min_backoff=1000, max_backoff=900000, max_retries=2),
        ],
    )
    dramatiq.set_broker(broker)
    yield broker
    for queue_name in broker.queues:
        client = asq._get_client(queue_name)
        client.delete_queue()
        if broker.dead_letter:
            dlq_client = asq._get_dlq_client(queue_name)
            dlq_client.delete_queue()


@pytest.fixture
def queue_name():
    letters = string.ascii_lowercase
    result_str = "".join(random.choice(letters) for i in range(10))
    return f"queue{result_str}"


@pytest.fixture
def worker(broker):
    worker = dramatiq.Worker(broker)
    worker.start()
    yield worker
    worker.stop()
