"""
HackBlitz/ingress API
"""
import socket
import struct

from hackblitz.clients.ingress.validators import validate_ip_address, validate_port


def encode(ip_address: str, port: int):
    """Encodes `ip_address` & `port` into a string that can be
    used as a subdomain in ingress service.

    When the encoded string is used in place of a subdomain, the
    ingress decodes the string and forwards the request to service
    running on ip_address:port.
    """

    validate_ip_address(ip_address)
    validate_port(port)

    packed_ip = socket.inet_aton(ip_address)
    decimal = struct.unpack("!L", packed_ip)[0]
    i_hash = ""

    for i in str(decimal):
        if i == "0":
            i_hash += i
        else:
            i_hash += chr(int(i) + 96)

    return f"{i_hash}-{port}"
