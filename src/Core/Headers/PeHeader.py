from src.Core.Header import Header
from src.Core.Types import Type


class PeHeader(Header):
    def __init__(self, offset):
        super().__init__("PE Header", "", offset=offset)

    def init_fields(self):
        self.set_field(
            "Signature", 4, size_type=Type.DWORD, description="File Format."
        )
