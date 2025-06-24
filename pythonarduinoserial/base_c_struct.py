

class BaseCStruct:
    """
    Represents a base structure for handling custom binary data layouts.

    This class provides a blueprint for converting between its custom binary
    data representation and a base format. Users are expected to extend this
    class and implement the methods for convertion from/to actual domain's
    dataclasses.
    """

    @staticmethod
    def from_base(base):
        raise NotImplemented

    def to_base(self):
        raise NotImplemented
