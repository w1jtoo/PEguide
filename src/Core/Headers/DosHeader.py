from src.Core.Header import Header
from src.Core.Types import Type
from src.Common.utils import to_empty, to_number


class DosHeader(Header):
    def __init__(self, offset):
        super().__init__("Dos Header", "", offset=offset)

    def init_fields(self) -> None:
        self.set_field(
            "e_magic", 2, description="Mark Zbikowski is watching you."
        )
        self.set_field("e_cblp", 2, bytes_convertor=to_empty)
        self.set_field("e_cp", 2, bytes_convertor=to_empty)
        self.set_field("e_crlc", 2, bytes_convertor=to_empty)
        self.set_field("e_cparhdr", 2, bytes_convertor=to_empty)
        self.set_field("e_minalloc", 2, bytes_convertor=to_empty)
        self.set_field("e_maxalloc", 2, bytes_convertor=to_empty)
        self.set_field("e_ss", 2, bytes_convertor=to_empty)
        self.set_field("e_sp", 2, bytes_convertor=to_empty)
        self.set_field("e_csum", 2, bytes_convertor=to_empty)
        self.set_field("e_ip", 2, bytes_convertor=to_empty)
        self.set_field("e_cs", 2, bytes_convertor=to_empty)
        self.set_field("e_lfarlc", 2, bytes_convertor=to_empty)
        self.set_field("e_ovno", 2, bytes_convertor=to_empty)
        self.set_field("e_res[4]", 8, bytes_convertor=to_empty)
        self.set_field("e_oemid", 2, bytes_convertor=to_empty)
        self.set_field("e_oeminfo", 2, bytes_convertor=to_empty)
        self.set_field("e_e_res2[10]", 20, bytes_convertor=to_empty)
        self.set_field(
            "e_lfanew",
            4,
            Type.DWORD,
            description="PE signature raw.",
            bytes_convertor=to_number,
        )
