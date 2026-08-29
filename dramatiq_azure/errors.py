from azure.core.exceptions import HttpResponseError
from azure.storage.queue import StorageErrorCode
from dramatiq.errors import BrokerError


class ASQError(BrokerError):
    """Base class for Azure Storage Queue broker errors."""


class MessageTooLarge(ASQError):
    """Raised when a message is larger than the queue allows."""


class DelayTooLong(ASQError):
    """Raised when a message delay is longer than the queue allows."""


_ERROR_CLASSES: dict[str, type[ASQError]] = {
    StorageErrorCode.REQUEST_BODY_TOO_LARGE: MessageTooLarge,
    StorageErrorCode.OUT_OF_RANGE_QUERY_PARAMETER_VALUE: DelayTooLong,
}


def translate(error: HttpResponseError) -> ASQError:
    """Build the ASQError matching an Azure storage error response.

    Responses carrying an unknown error code, or none at all, yield a
    plain ASQError.
    """
    error_code: str = getattr(error, "error_code", "") or ""
    return _ERROR_CLASSES.get(error_code, ASQError)(str(error))
