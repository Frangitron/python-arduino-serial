from abc import ABC, abstractmethod


class AbstractUsbSerial(ABC):
    """
    Base class representing an abstract USB-to-Serial communication interface.

    This class defines the required interface for a USB-to-Serial driver,
    providing functionality for managing the connection, reading, writing, and
    listing available ports. Implementations of this class must define the
    behavior of the declared abstract methods.

    All derived classes are expected to implement the methods for opening a
    connection, closing it, writing data, reading data, checking if the buffer
    is empty, and querying available device names.
    """

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
