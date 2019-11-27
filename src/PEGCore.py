from src.Core.Header import Header
from src.Core.Headers.DosHeader import DosHeader
from src.Core.Headers.PeHeader import PeHeader
from src.Core.Headers.FileHeader import FileHeader
from src.Core.Headers.OptionalHeader import OptionalHeader
from src.Core.Headers.DateDirectoriesHeader import DateDirectoriesHeader
from src.Core.Headers.SectionHeader import SectionHeaders
from src.Core.Types import Type


class Core:
    def __init__(self, file_name: str):
        self.file_name = file_name

    def read_headers(self):
        dos_header = pe_header = file_header = None
        file_pointer = 0

        with open(self.file_name, mode="rb") as f:
            dos_header = DosHeader(file_pointer)
            dos_header.fill_in_fields(f)

            pe_header = PeHeader(file_pointer + sum(dos_header.e_lfanew))
            pe_header.fill_in_fields(f)

            file_header = FileHeader(sum(dos_header.e_lfanew) + 4)
            file_pointer = file_header.fill_in_fields(f)

            optional_header = OptionalHeader(file_pointer)
            file_pointer = optional_header.fill_in_fields(f)
            optional_header.offset = file_pointer
            optional_header.afterward_init()
            file_pointer = optional_header.fill_in_fields(f)

            date_dir_header = DateDirectoriesHeader(file_pointer)
            file_pointer = date_dir_header.fill_in_fields(f)

            sections = SectionHeaders(
                file_pointer, sum(file_header.NumberOfSections)
            )
            file_pointer = sections.init_sections(f)

        self.dos_header = str(dos_header)
        self.pe_header = str(pe_header)
        self.file_header = str(file_header)
        self.optional_header = str(optional_header)
        self.date_dir_header = str(date_dir_header)
        self.sections = str(sections)

    def write_headers(self):
        print(self.dos_header)
        print(self.pe_header)
        print(self.file_header)
        print(self.optional_header)
        print(self.date_dir_header)
        print(self.sections)
