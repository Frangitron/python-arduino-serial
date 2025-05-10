from abc import ABC, abstractmethod


class AbstractUsbSerial(ABC):

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def is_buffer_empty(self) -> bool:
        pass

    @abstractmethod
    def list_names(self) -> list[str]:
        pass

    @abstractmethod
    def open(self, name: str):
        pass

    @abstractmethod
    def read(self) -> bytearray:
        pass

    @abstractmethod
    def write(self, data: bytearray):
        pass
