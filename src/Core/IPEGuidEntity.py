# from typing import *
import abc


class IPEEntity:
    def __init__(self, offset: int, name: str, description: str):
        self.name = name
        self.description = description
        self.offset = offset
        self._initialized = False

    @abc.abstractmethod
    def is_initalized(self) -> bool:
        return self._initialized
