from src.Core.IPEGuidEntity import IPEEntity
from src.Common.utils import convert_to_hex, get_int_le, decode_from_cp


class Section:
    def __init__(self, name: str, offset: int, size_of_raw_date: int):
        self.name = name
        self.__bytes: bytes = bytes()
        self.offset = offset
        self.size_of_raw_date = size_of_raw_date

    def fill_in_raw(self, stream):
        stream.seek(self.offset, 0)
        self.__bytes = stream.read(self.size_of_raw_date)

    def __str__(self):
        result = []
        position = self.offset
        for number in range(0, len(self.__bytes) - 1, 16):
            string_position = "".join(hex(position))
            raw = " ".join(convert_to_hex(self.__bytes[number: number + 16]))
            decoded = decode_from_cp(self.__bytes[number : number + 16])
            result.append(f"{string_position:>20}:  {raw} {decoded}")
            position += 16 * 16
        return "\n".join(result)

    def get_point(self, byte_position: int) -> int:
        return self.__bytes[byte_position]
