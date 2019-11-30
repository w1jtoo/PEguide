from enum import IntEnum


class Type(IntEnum):
    DWORD = 4
    WORD = 2
    BYTE = 1

    def __str__(self):
        return super().__str__()[5:]

    def to_c_string(self) -> str:
        if int(self) == 4:
            return "I"
        elif int(self) == 2:
            return "H"
        elif int(self) == 1:
            return "c"
        else: 
            raise Exception("Wrong type of structure. ")
