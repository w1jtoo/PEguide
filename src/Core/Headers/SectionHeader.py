from src.Core.Header import Struct
from src.Core.Types import Type
from src.Common.utils import to_empty, to_number, get_to_number


class SectionHeader(Struct):
    def __init__(self, offset):
        super().__init__("", "", offset=offset)

    def init_fields(self):
        # fix descrition
        self.set_field("Name", 8, size_type=Type.BYTE)
        self.set_field(
            "VirtualSize",
            4,
            size_type=Type.DWORD,
            bytes_convertor=get_to_number(4, Type.DWORD),
        )
        self.set_field(
            "VirtualAddress", 4, size_type=Type.DWORD, bytes_convertor=to_empty
        )

        self.set_field(
            "SizeOfRawData", 4, size_type=Type.DWORD, bytes_convertor=to_empty
        )
        self.set_field(
            "PointerToRawData",
            4,
            size_type=Type.DWORD,
            bytes_convertor=to_empty,
        )
        self.set_field(
            "PointerToRelocations",
            4,
            size_type=Type.DWORD,
            bytes_convertor=to_empty,
        )
        self.set_field(
            "PointerToLinenumbers",
            4,
            size_type=Type.DWORD,
            bytes_convertor=to_empty,
        )
        self.set_field("NumberOfRelocations", 2, bytes_convertor=to_number)
        self.set_field("NumberOfLinenumbers", 2, bytes_convertor=to_number)
        self.set_field("Characteristics", 4, bytes_convertor=to_number)

class SectionHeaders:
    def __init__(self, offset, section_count):
        self.offset = offset
        self.section_count = section_count
        self.sections = []

    def init_sections(self, stream):
        file_pointer = self.offset
        for _ in range(self.section_count):
            section = SectionHeader(file_pointer)
            section.init_fields()
            file_pointer = section.fill_in_fields(stream)
            self.sections.append(section)
        return file_pointer

    def __str__(self):
        result = []
        for section in self.sections:
            result.append(section.decode())
            temp = str(sections).split("\n")[2:]
            result += map(lambda x: "      " + x, temp)
        return "\n".join(result)
