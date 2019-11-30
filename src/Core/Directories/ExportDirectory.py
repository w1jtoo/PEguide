from src.Core.Header import Struct 
from src.Core.Types import Type
from src.Common.utils import (
    to_number,
    to_empty,
    to_date,
    get_to_number,
    get_int_le,
)

class ExportDirectory(Struct):
    def __init__(self, offset:int):
        super().__init__("Export Direcory", "", offset=offset)
    
    def init_fields(self)->None:
        self.set_field(
            "Characteristics",
            4,
            bytes_convertor=get_to_number(4, Type.DWORD, base=lambda x: x),
            size_type=Type.DWORD,
        )
        self.set_field(
            "TimeDateStamp",
            4,
            bytes_convertor=to_date,
            size_type=Type.DWORD,
        )
        self.set_field(
            "MajorVersion",
            2,
            bytes_convertor=get_to_number(2, Type.WORD, base=lambda x: x),
        )
        self.set_field(
            "MinorVersion",
            2,
            bytes_convertor=get_to_number(2, Type.WORD, base=lambda x: x),
            size_type=Type.DWORD,
        )
        self.set_field(
            "Name",
            4,
            size_type=Type.DWORD,
        )
        self.set_field(
            "Base",
            4,
            bytes_convertor=get_to_number(4, Type.DWORD, base=lambda x: x),
            size_type=Type.DWORD,
        )
        self.set_field(
            "NumberOfFunctions",
            4,
            bytes_convertor=get_to_number(4, Type.DWORD, base=lambda x: x),
            size_type=Type.DWORD,
        )
        self.set_field(
            "NumberOfNames",
            4,
            bytes_convertor=get_to_number(4, Type.DWORD, base=lambda x: x),
            size_type=Type.DWORD,
        )
        self.set_field(
            "AddressOfFunctions",
            4,
            bytes_convertor=get_to_number(4, Type.DWORD),
            size_type=Type.DWORD,
        )
        self.set_field(
            "AddressOfNames",
            4,
            bytes_convertor=get_to_number(4, Type.DWORD),
            size_type=Type.DWORD,
        )
        self.set_field(
            "AddressOfNameOrdinals",
            4,
            bytes_convertor=get_to_number(4, Type.DWORD),
            size_type=Type.DWORD,
        )
