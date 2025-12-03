from unittest.mock import (
    ANY,
    MagicMock,
    patch,
)

import pytest
from azure.storage.queue import QueueClient

from dramatiq_azure import asq


def test_get_client_uses_connection_string_when_available():
    """Test that _get_client uses connection string auth when CONN_STR is set."""
    conn_str = (
        "DefaultEndpointsProtocol=https;AccountName=testaccount;"
        "AccountKey=testkey;QueueEndpoint=https://testaccount.queue.core.windows.net;"
    )

    with patch.object(asq, "CONN_STR", conn_str), patch(
        "dramatiq_azure.asq.QueueClient.from_connection_string"
    ) as mock_from_conn_str:

        mock_client = MagicMock(spec=QueueClient)
        mock_from_conn_str.return_value = mock_client

        client = asq._get_client("test-queue")

        mock_from_conn_str.assert_called_once_with(
            conn_str=conn_str,
            queue_name="test-queue",
            message_encode_policy=ANY,
            message_decode_policy=ANY,
        )
        assert client is mock_client


def test_get_client_uses_default_azure_credential_without_connection_string():
    """Test that _get_client uses DefaultAzureCredential when CONN_STR is not set."""
    pytest.importorskip("azure.identity")
    account_url = "https://testaccount.queue.core.windows.net"

    with patch.object(asq, "CONN_STR", ""), patch.object(
        asq, "ACCOUNT_URL", account_url
    ), patch("dramatiq_azure.asq.QueueClient") as mock_queue_client, patch(
        "azure.identity.DefaultAzureCredential"
    ) as mock_credential_class:

        mock_credential = MagicMock()
        mock_credential_class.return_value = mock_credential
        mock_client = MagicMock(spec=QueueClient)
        mock_queue_client.return_value = mock_client

        client = asq._get_client("test-queue")

        mock_credential_class.assert_called_once_with()
        mock_queue_client.assert_called_once_with(
            account_url=account_url,
            queue_name="test-queue",
            credential=mock_credential,
            message_encode_policy=ANY,
            message_decode_policy=ANY,
        )
        assert client is mock_client


def test_get_client_respects_custom_account_url():
    """Test that _get_client uses custom AZURE_QUEUE_ACCOUNT_URL when provided."""
    pytest.importorskip("azure.identity")
    custom_url = "https://custom.queue.example.com"

    with patch.object(asq, "CONN_STR", ""), patch.object(
        asq, "ACCOUNT_URL", custom_url
    ), patch("dramatiq_azure.asq.QueueClient") as mock_queue_client, patch(
        "azure.identity.DefaultAzureCredential"
    ) as mock_credential_class:

        mock_credential = MagicMock()
        mock_credential_class.return_value = mock_credential
        mock_client = MagicMock(spec=QueueClient)
        mock_queue_client.return_value = mock_client

        asq._get_client("test-queue")

        mock_queue_client.assert_called_once_with(
            account_url=custom_url,
            queue_name="test-queue",
            credential=mock_credential,
            message_encode_policy=ANY,
            message_decode_policy=ANY,
        )


def test_get_client_uses_http_when_ssl_disabled():
    """Test that _get_client uses http protocol when AZURE_SSL is false."""
    pytest.importorskip("azure.identity")
    http_url = "http://testaccount.queue.core.windows.net"

    with patch.object(asq, "CONN_STR", ""), patch.object(
        asq, "ACCOUNT_URL", http_url
    ), patch("dramatiq_azure.asq.QueueClient") as mock_queue_client, patch(
        "azure.identity.DefaultAzureCredential"
    ) as mock_credential_class:

        mock_credential = MagicMock()
        mock_credential_class.return_value = mock_credential
        mock_client = MagicMock(spec=QueueClient)
        mock_queue_client.return_value = mock_client

        asq._get_client("test-queue")

        mock_queue_client.assert_called_once_with(
            account_url=http_url,
            queue_name="test-queue",
            credential=mock_credential,
            message_encode_policy=ANY,
            message_decode_policy=ANY,
        )
