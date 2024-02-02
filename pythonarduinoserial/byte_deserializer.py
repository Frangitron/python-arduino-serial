import struct
from typing import get_type_hints, Annotated, get_origin, get_args, Any

from pythonarduinoserial.types import SerializationAnnotation
from pythonarduinoserial.byte_formatter import ByteFormatter


class ByteDeserializer:

    def __init__(self, input_: bytes):
        self._input = input_
        self._index = 0
        self._values = list()

    def to_object(self, type_):
        output = type_()

        format_ = ByteFormatter().make_format(type_)
        self._values = struct.unpack(format_, self._input)

        items = get_type_hints(output, include_extras=True).items()
        for name, type_hint in items:
            setattr(output, name, self._deserialize(type_hint))

        return output

    def _deserialize(self, type_hint) -> Any:
        if get_origin(type_hint) == Annotated:
            type_, annotation = get_args(type_hint)
            if get_origin(type_) == list:
                return self._deserialize_list(type_, annotation)
            else:
                return self._deserialize_value(type_, annotation)
        else:
            return self.to_object(type_hint)

    def _deserialize_value(self, type_, annotation) -> Any:
        assert isinstance(annotation, SerializationAnnotation)
        value = None

        if type_ in [bytes, int, float, bool]:
            value = self._values[self._index]
            self._index += 1

        elif type_ == str:
            value = self._values[self._index].decode('ascii')
            self._index += 1

        return value

    def _deserialize_list(self, type_, annotation) -> list[Any]:
        sub_hint = get_args(type_)[0]
        return [self._deserialize(sub_hint) for _ in range(annotation.length)]
