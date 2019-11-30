from src.Core.Header import Struct
from src.Core.Headers.DosHeader import DosHeader
from src.Core.Headers.PeHeader import PeHeader
from src.Core.Headers.FileHeader import FileHeader
from src.Core.Headers.OptionalHeader import OptionalHeader
from src.Core.Headers.DateDirectoriesHeader import DateDirectoriesHeader
from src.Core.Headers.SectionHeader import SectionHeaders
from src.Core.Types import Type
from src.Core.Section import Section
from typing import Dict, List, Optional
from src.Common.utils import convert_to_hex, get_int_le, align_down, align_up
from src.Core.Directories.ExportDirectory import ExportDirectory


class Core:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.file_pointer = 0

    def read_headers(self):
        dos_header = pe_header = file_header = None
        self.file_pointer = 0

        with open(self.file_name, mode="rb") as f:
            dos_header = DosHeader(self.file_pointer)
            dos_header.fill_in_fields(f)

            pe_header = PeHeader(self.file_pointer + sum(dos_header.e_lfanew))
            pe_header.fill_in_fields(f)

            file_header = FileHeader(sum(dos_header.e_lfanew) + 4)
            self.file_pointer = file_header.fill_in_fields(f)

            optional_header = OptionalHeader(self.file_pointer)
            self.file_pointer = optional_header.fill_in_fields(f)
            optional_header.offset = self.file_pointer
            optional_header.afterward_init()
            self.file_pointer = optional_header.fill_in_fields(f)

            date_dir_header = DateDirectoriesHeader(self.file_pointer)
            self.file_pointer = date_dir_header.fill_in_fields(f)

            sections = SectionHeaders(
                self.file_pointer, sum(file_header.NumberOfSections)
            )
            self.file_pointer = sections.init_sections(f)

        self.dos_header = dos_header
        self.pe_header = pe_header
        self.file_header = file_header
        self.optional_header = optional_header
        self.date_dir_header = date_dir_header
        self.section_headers = sections

    def get_va(self, rva: int) -> int:
        return get_int_le(self.optional_header.get("ImageBase"), _type=Type.DWORD) + rva

    def get_rva(self, va: int) -> int:
        return va - get_int_le(self.optional_header.get("ImageBase"), _type=Type.DWORD)

    def define_section(self, rva: int) -> Optional[Struct]:
        for index, section in enumerate(self.section_headers.sections):
            start = self.get_rva(get_int_le(section.VirtualAddress, _type=Type.DWORD))
            end = start + align_up(
                get_int_le(section.VirtualSize, _type=Type.DWORD),
                get_int_le(
                    self.optional_header.get("SectionAlignment"), _type=Type.DWORD
                ),
            )
            if end <= rva <= start:
                return section
        return None

    def rva_to_raw(self, rva: int) -> int:
        found_section = self.define_section(rva)
        if found_section:
            return (
                rva
                - self.get_rva(get_int_le(found_section.VirtualAddress, Type.DWORD))
                + get_int_le(found_section.PointerToRawData, Type.DWORD)
            )
        return 0

    def read_sections(self) -> None:
        self.sections: List[Section] = []
        with open(self.file_name, mode="rb") as f:
            for section_header in self.section_headers.sections:
                section = Section(
                    section_header.Name.decode("cp1251"),
                    get_int_le(section_header.PointerToRawData, Type.DWORD),
                    get_int_le(section_header.SizeOfRawData, Type.DWORD),
                )
                section.fill_in_raw(f)
                self.sections.append(section)

    def write_headers(self):
        print(120 * "=")
        print("\n This file have next headers:")
        print(self.dos_header)
        print(self.pe_header)
        print(self.file_header)
        print(self.optional_header)
        print(self.date_dir_header)
        print(120 * "=")

    def write_tables(self):
        print(120 * "=")
        print(self.export_directory)
        print(120 * "=")

    def read_directories(self) -> None:
        with open(self.file_name, mode="rb") as f:
            raw_to_export = self.rva_to_raw(
                get_int_le(
                    self.date_dir_header.get("Export Table")[0:4], _type=Type.DWORD
                )
            )
            self.export_directory = ExportDirectory(raw_to_export)
            if raw_to_export:
                self.export_directory.fill_in_fields(f)
            else:
                self.export_directory.set_error("\n NO EXPORT TABLE WAS FOUND. \n")

    def write_sections(self):
        print(120 * "=")
        print("Next sections was found. ")
        result = []
        number = 1
        for section, header in zip(self.sections, self.section_headers.sections):
            result.append(
                f"""
Header Section #{number}
{str(header)[2:]}
Raw Date
{str(section)}"""
            )
            number += 1

        print("\n".join(result))
        print(120 * "=")
