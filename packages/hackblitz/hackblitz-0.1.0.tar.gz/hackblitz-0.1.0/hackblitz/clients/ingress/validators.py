"""Validators used in ingress client."""

from .utils import is_valid_ipv4_address, is_valid_ipv6_address


def validate_ip_address(ip_address: str):
    """Validates the given ip address."""

    if not isinstance(ip_address, str):
        raise TypeError(f"ip address must be str, not {type(ip_address)!r}")

    if not is_valid_ipv4_address(ip_address) or not is_valid_ipv6_address(ip_address):
        raise TypeError(f"str {ip_address!r} is not an ip address")


def validate_port(port: int):
    """Validates the given port"""

    if not isinstance(port, int):
        raise TypeError("port must be int")
