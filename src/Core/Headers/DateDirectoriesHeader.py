from src.Core.Header import Header
from src.Core.Types import Type
from src.Common.utils import to_number, to_empty, to_date


class DateDirectoriesHeader(Header):
    def __init__(self, offset):
        super().__init__("Optional Header Data Directories", "", offset=offset)

    def init_fields(self) -> None:
        self.set_field(
            "Export Table", 8, bytes_convertor=to_empty, size_type=Type.DWORD
        )
        self.set_field(
            "Import Table", 8, bytes_convertor=to_empty, size_type=Type.DWORD
        )
        self.set_field(
            "Resource Table", 8, bytes_convertor=to_empty, size_type=Type.DWORD
        )
        self.set_field(
            "Exception Table",
            8,
            bytes_convertor=to_empty,
            size_type=Type.DWORD,
        )
        self.set_field(
            "Certificate Table",
            8,
            bytes_convertor=to_empty,
            size_type=Type.DWORD,
        )
        self.set_field(
            "Base Relocation Table",
            8,
            bytes_convertor=to_empty,
            size_type=Type.DWORD,
        )
        self.set_field(
            "Debug", 8, bytes_convertor=to_empty, size_type=Type.DWORD
        )
        self.set_field(
            "Export Table", 8, bytes_convertor=to_empty, size_type=Type.DWORD
        )
        self.set_field(
            "Architecture", 8, bytes_convertor=to_empty, size_type=Type.DWORD
        )
        self.set_field(
            "Global Ptr", 8, bytes_convertor=to_empty, size_type=Type.DWORD
        )
        self.set_field(
            "TLS Table", 8, bytes_convertor=to_empty, size_type=Type.DWORD
        )
        self.set_field(
            "Load Config Table",
            8,
            bytes_convertor=to_empty,
            size_type=Type.DWORD,
        )
        self.set_field(
            "Bound Import", 8, bytes_convertor=to_empty, size_type=Type.DWORD
        )
        self.set_field(
            "IAT", 8, bytes_convertor=to_empty, size_type=Type.DWORD
        )
        self.set_field(
            "Delay Import Descriptor",
            8,
            bytes_convertor=to_empty,
            size_type=Type.DWORD,
        )
        self.set_field(
            "CLR Runtime Header",
            8,
            bytes_convertor=to_empty,
            size_type=Type.DWORD,
        )
        self.set_field(
            "Reserved",
            8,
            bytes_convertor=to_empty,
            size_type=Type.DWORD,
            description="must be zero",
        )
