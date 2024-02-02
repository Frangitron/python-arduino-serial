# https://stackoverflow.com/questions/59881123/c-sizeof-char-in-struct
from binascii import hexlify
import logging
import struct
from typing import get_type_hints, Annotated, get_origin, get_args

from pythonarduinoserial.types import SerializationAnnotation


_logger = logging.getLogger(__name__)


class ByteSerializer:

    def __init__(self):
        self._output = bytes()
        self._values = list()
        self._format = "@"

    def to_bytes(self, object_) -> bytes:
        items = get_type_hints(object_, include_extras=True).items()
        for name, type_hint in items:
            self._serialize(getattr(object_, name), type_hint)

        result = struct.pack(self._format, *self._values)
        _logger.debug(f"serialized {len(result)} bytes: {hexlify(result, sep=' ')}")
        return result

    def _serialize(self, value, type_hint):
        if get_origin(type_hint) == Annotated:
            type_, annotation = get_args(type_hint)
            if get_origin(type_) == list:
                self._serialize_list(value, type_)
            else:
                self._serialize_value(value, type_, annotation)
        else:
            self.to_bytes(value)

    def _serialize_value(self, value, type_, annotation):
        assert isinstance(value, type_)
        assert isinstance(annotation, SerializationAnnotation)

        if type_ == bytes:
            self._values.append(value)
            self._format += annotation.struct_format

        elif type_ == bool:
            self._values.append(bytes([value]))
            self._format += annotation.struct_format

        elif type_ == str:
            if len(value) < annotation.length:
                self._values.append(bytes(value + " " * (annotation.length - len(value) - 1), "ascii") + bytes(1))
            else:
                self._values.append(bytes(value[:annotation.length - 1], "ascii") + bytes(1))
            self._format += annotation.struct_format

        elif type_ in [float, int]:
            self._values.append(value)
            self._format += annotation.struct_format

    def _serialize_list(self, value, type_):
        sub_hint = get_args(type_)[0]
        for item in value:
            self._serialize(item, sub_hint)
