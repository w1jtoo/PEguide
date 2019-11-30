from src.Core.IPEGuidEntity import IPEEntity
from src.Common.utils import convert_to_hex
from collections import namedtuple
from src.Core.Types import Type


class Struct(IPEEntity):
    Container = namedtuple(
        "Container", "size type description bytes_convertor"
    )

    def __init__(self, name: str, description: str, offset=0):
        super().__init__(offset, name, description)
        self.__fields = {}
        self.__values = {}
        self.init_fields()
        self.__error:str = ""

    def init_fields(self) -> None:
        raise NotImplementedError()

    def set_field(
        self,
        name: str,
        size: int,
        size_type=Type.WORD,
        description="",
        bytes_convertor=None,
    ) -> None:
        """Initialize new field. Use to fill in field's information
		 and to get stuctured data in future.
			Rely on order of field adding.  
		   Use size, name, etc. """
        if not bytes_convertor:
            bytes_convertor = lambda x: x.decode("cp1251")
        self.__fields[name] = Struct.Container(
            size, size_type, description, bytes_convertor
        )

    def get_full_size(self) -> int:
        return sum(self.__fields.values())

    def fill_in_fields(self, stream) -> int:
        stream.seek(self.offset, 0)
        for field in self.__fields.keys():
            if self.__values.get(field):
                continue
            self.__values[field] = stream.read(self.__fields[field].size)
        return stream.tell()

    def __str__(self):
        if self.__error:
            return self.__error
        result = []
        result.append(f"{self.name} \n {self.description}")
        position = self.offset
        for field in self.__fields:
            hex_date = " ".join(convert_to_hex(self.__values[field]))
            try:
                _bytes = self.__fields[field].bytes_convertor(self.__values[field])
            except Exception:
                _bytes = "????????"
            _type = self.__fields[field].type

            if int(_type) < self.__fields[field].size:
                _type = (
                    str(_type) + f"[{self.__fields[field].size // int(_type)}]"
                )

            result.append(
                f"{hex(position):<10} {str(_type):>8}\
{field:>28}: {_bytes:<30} {hex_date:<16}: {self.__fields[field].description}"
            )
            position += self.__fields[field].size
        return "\n".join(result) + "\n"

    def __getattr__(self, value):
        if value in self.__values:
            return self.__values[value]
        raise AttributeError

    def get(self, key:str)-> "Struct":
        if key in self.__values:
            return self.__values[key]
        return None
    
    def set_error(self, description:str)-> None:
        self.__error = description
