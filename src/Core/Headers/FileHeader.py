from src.Core.Header import Struct
from src.Core.Types import Type
from src.Common.utils import to_number, to_empty, to_date, get_to_number


class FileHeader(Struct):
    def __init__(self, offset):
        super().__init__("File Header", "", offset=offset)

    def init_fields(self):
        self.set_field("Machine", 2, bytes_convertor=to_empty)
        self.set_field("NumberOfSections", 2, bytes_convertor=to_number)
        self.set_field(
            "TimeDateStamp", 4, size_type=Type.DWORD, bytes_convertor=to_date
        )
        self.set_field(
            "PointerToSymbolTable",
            4,
            size_type=Type.DWORD,
            bytes_convertor=get_to_number(4, Type.DWORD),
        )
        self.set_field(
            "NumberOfSymbols",
            4,
            size_type=Type.DWORD,
            bytes_convertor=to_number,
        )
        self.set_field("SizeOfOptionalHeader", 2, bytes_convertor=to_number)
        self.set_field("Characteristics", 2, bytes_convertor=to_empty)
