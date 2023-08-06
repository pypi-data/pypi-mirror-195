"""
Package contains clients that can be used to interact with
the open source services available in HackBlitz.

Usage:
    >>> import hackblitz
    >>> ingress = hackblitz.client("ingress")

In the above example, if the client provided does not exists it
will raise `ClientNotFoundError`.
"""

from importlib import import_module


class ClientNotFoundError(Exception):
    """Raised when invalid client is passed to .client()."""


def client(name: str):
    """Gets the given service client if available in hackblitz."""

    try:
        return import_module(f"hackblitz.clients.{name}")
    except ModuleNotFoundError:
        raise ClientNotFoundError(f"no such client {name!r}") from None
