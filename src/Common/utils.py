from typing import List
from src.Core.Types import Type
import struct


def convert_to_hex(_bytes: bytes) -> List[int]:
    result = []
    for byte in _bytes:
        temp = hex(byte)[2:].upper()
        if len(temp) == 1:
            temp = "0" + temp
        result.append(temp)
    return result


import string


def decode_from_cp(_bytes: bytes) -> str:
    decoded = _bytes.decode("cp1251", "ignore")
    result = []
    for letter in decoded:
        if (
            letter in string.digits
            or letter in string.ascii_letters
            or letter in string.punctuation
        ):
            result.append(letter)
        else:
            result.append(".")

    return "".join(result)


def to_number(_bytes: bytes) -> int:
    return sum(_bytes)


def to_empty(_bytes: bytes) -> str:
    return "hex ->"


def get_to_number(size: int, _type: Type, endian="<", base=hex):
    def _to_number(_bytes: bytes):
        if endian == "<":
            dec = struct.unpack(
                endian + _type.to_c_string() * (size // int(_type)), _bytes
            )[0]
            return f"LE [{str(base(dec)).upper()}]"
        elif endian == ">":
            dec = struct.unpack(
                endian + _type.to_c_string() * (size // int(_type)), _bytes
            )[0]
            return f"BE [{str(base(dec)).upper()}]"
        else:
            raise AttributeError

    return _to_number


def get_int_le(_bytes: bytes, _type: Type= Type.WORD) -> int:
    size = len(_bytes)
    return struct.unpack("<" + _type.to_c_string() * (size // int(_type)), _bytes)[0]

def align_down(index:int, align:int)-> int:
    return index & (~(align-1))


def align_up(index:int, align:int) -> int:
    return align_down(index, align) + align if (index & (align-1)) else index

import time


def to_date(_bytes: bytes) -> str:
    return time.ctime(*struct.unpack("i", _bytes))
