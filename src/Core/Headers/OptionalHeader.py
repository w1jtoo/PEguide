from src.Core.Header import Header
from src.Core.Types import Type
from src.Common.utils import (
    to_number,
    to_empty,
    to_date,
    get_to_number,
    to_int_le,
)


class OptionalHeader(Header):
    def __init__(self, offset):
        super().__init__("Optional Header", "", offset=offset)

    def init_fields(self) -> None:
        self.set_field(
            "Magic",
            2,
            bytes_convertor=lambda x: "PE32+" if x == b"\x0b\x02" else "PE32",
        )
        self.set_field(
            "MajorLinkerVersion",
            1,
            bytes_convertor=get_to_number(1, Type.BYTE, base=to_int_le),
            size_type=Type.BYTE,
        )
        self.set_field(
            "MinorLinkerVersion",
            1,
            bytes_convertor=get_to_number(1, Type.BYTE, base=to_int_le),
            size_type=Type.BYTE,
        )
        self.set_field(
            "SizeOfCode",
            4,
            bytes_convertor=get_to_number(4, Type.DWORD, base=to_int_le),
            size_type=Type.DWORD,
        )
        self.set_field(
            "SizeOfInitializedData",
            4,
            bytes_convertor=get_to_number(4, Type.DWORD, base=to_int_le),
            size_type=Type.DWORD,
        )
        self.set_field(
            "SizeOfUninitializedData",
            4,
            bytes_convertor=get_to_number(4, Type.DWORD, base=to_int_le),
            size_type=Type.DWORD,
        )
        self.set_field(
            "AddressOfEntryPoint",
            4,
            bytes_convertor=get_to_number(4, Type.DWORD),
            size_type=Type.DWORD,
        )
        self.set_field(
            "BaseOfCode",
            4,
            bytes_convertor=get_to_number(4, Type.DWORD),
            size_type=Type.DWORD,
        )

    def afterward_init(self):
        if self.Magic != b"\x0b\x02":
            self.set_field(
                "BaseOfData",
                4,
                bytes_convertor=get_to_number(4, Type.DWORD),
                size_type=Type.DWORD,
            )

        if self.Magic != b"\x0b\x02":
            self.set_field(
                "ImageBase",
                4,
                bytes_convertor=get_to_number(4, Type.DWORD),
                size_type=Type.DWORD,
            )
        elif self.Magic == b"\x0b\x02":
            self.set_field(
                "ImageBase",
                8,
                bytes_convertor=get_to_number(8, Type.DWORD),
                size_type=Type.DWORD,
            )

        self.set_field(
            "SectionAlignment",
            4,
            bytes_convertor=get_to_number(4, Type.DWORD),
            size_type=Type.DWORD,
        )
        self.set_field(
            "FileAlignment",
            4,
            bytes_convertor=get_to_number(4, Type.DWORD),
            size_type=Type.DWORD,
        )
        self.set_field(
            "MajorOperatingSystemVersion",
            2,
            bytes_convertor=get_to_number(2, Type.WORD, base=to_int_le),
            size_type=Type.WORD,
        )
        self.set_field(
            "MinorOperatingSystemVersion",
            2,
            bytes_convertor=get_to_number(2, Type.WORD, base=to_int_le),
            size_type=Type.WORD,
        )
        self.set_field(
            "MajorImageVersion",
            2,
            bytes_convertor=get_to_number(2, Type.WORD, base=to_int_le),
            size_type=Type.WORD,
        )
        self.set_field(
            "MinorImageVersion",
            2,
            bytes_convertor=get_to_number(2, Type.WORD, base=to_int_le),
            size_type=Type.WORD,
        )
        self.set_field(
            "MajorSubsystemVersion",
            2,
            bytes_convertor=get_to_number(2, Type.WORD, base=to_int_le),
            size_type=Type.WORD,
        )
        self.set_field(
            "MinorSubsystemVersion",
            2,
            bytes_convertor=get_to_number(2, Type.WORD, base=to_int_le),
            size_type=Type.WORD,
        )

        self.set_field(
            "Win32VersionValue",
            4,
            bytes_convertor=get_to_number(4, Type.DWORD, base=to_int_le),
            size_type=Type.DWORD,
        )
        self.set_field(
            "SizeOfImage",
            4,
            bytes_convertor=get_to_number(4, Type.DWORD),
            size_type=Type.DWORD,
        )
        self.set_field(
            "SizeOfHeaders",
            4,
            bytes_convertor=get_to_number(4, Type.DWORD),
            size_type=Type.DWORD,
        )
        self.set_field(
            "CheckSum", 4, bytes_convertor=to_empty, size_type=Type.DWORD
        )

        self.set_field(
            "Subsystem",
            2,
            bytes_convertor=get_to_number(2, Type.WORD, base=hex),
            size_type=Type.WORD,
            description="Search 'Windows Subsystem' to know more information.",
        )
        self.set_field(
            "DllCharacteristics",
            2,
            bytes_convertor=get_to_number(2, Type.WORD, base=hex),
            description="Search 'DLL Characteristics' to know more information.",
        )

        optional_size = 8 if self.Magic == b"\x0b\x02" else 4

        self.set_field(
            "SizeOfStackReserve",
            optional_size,
            size_type=Type.DWORD,
            bytes_convertor=get_to_number(optional_size, Type.DWORD),
        )
        self.set_field(
            "SizeOfStackCommit",
            optional_size,
            size_type=Type.DWORD,
            bytes_convertor=get_to_number(optional_size, Type.DWORD),
        )
        self.set_field(
            "SizeOfHeapReserve",
            optional_size,
            size_type=Type.DWORD,
            bytes_convertor=get_to_number(optional_size, Type.DWORD),
        )
        self.set_field(
            "SizeOfHeapCommit",
            optional_size,
            size_type=Type.DWORD,
            bytes_convertor=get_to_number(optional_size, Type.DWORD),
        )

        self.set_field(
            "LoaderFlags", 4, size_type=Type.DWORD, bytes_convertor=to_number
        )
        self.set_field(
            "NumberOfRvaAndSizes",
            4,
            size_type=Type.DWORD,
            bytes_convertor=to_number,
        )
