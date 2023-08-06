# coding=utf8
from mercury_base.mercury_v2 import commands
from struct import pack, unpack

ADDRESS_FORMAT = '!B'  # 1 byte in network order
cache = {
    b'\x30\x00\x15\xB0': b'\x30\x00\x15\xB0',
    b'\x30\x01\x01\x01\x02\x03\x04\x05\x06\x35\x3B': b'\x30\x00\x15\xB0',
    b'\x30\x08\x05\xB6\x0C': b'\x30\x00\x30\x71\xDB',
    b'\x30\x08\x00\x76\x0F': b'\x30\x28\x44\x00\x30\x16\x01\x14\x0B\x02',
    b'\x30\x08\x03\x36\x0E': b'\x30\x08\x00\x00\x8E\xE6',
    b'\x30\x08\x12\xF6\x02': b'\x30\xB4\xE3\xC2\x95\x57\x40\xE7\x35',
    b'\x30\x08\x26\xF7\xD5': b'\x30\x4E\x51\x85\x93',
    b'\x30\x08\x02\xF7\xCE': b'\x30\x00\x01\x00\x01\xF4\x04',
}


def prepare_address(address: int) -> int:
    address %= 1000
    if address > 239:
        address %= 100
        if address == 0:
            address = 1
    return address


def format_address(address: int) -> bytes:
    return pack(ADDRESS_FORMAT, address)


def extract_address(message: bytes) -> int:
    address = unpack(ADDRESS_FORMAT, message[:1])[0]
    return address


def extract_command(message: bytes) -> None:
    return None


def extract_data(message: bytes) -> list[bytes]:
    data = list(message[1:-2])
    return data
