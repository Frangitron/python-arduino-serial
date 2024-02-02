# https://stackoverflow.com/questions/59881123/c-sizeof-char-in-struct
from typing import get_type_hints, Annotated, get_origin, get_args


class ByteFormatter:
    def __init__(self):
        self._format = "@"

    def make_format(self, struct_type):
        items = get_type_hints(struct_type, include_extras=True).items()
        for name, type_hint in items:
            self._format_attribute(type_hint)

        return self._format

    def _format_attribute(self, type_hint):
        if get_origin(type_hint) == Annotated:
            type_, annotation = get_args(type_hint)

            if get_origin(type_) == list:
                sub_hint = get_args(type_)[0]
                for _ in range(annotation.length):
                    self._format_attribute(sub_hint)

            else:
                self._format += annotation.struct_format
