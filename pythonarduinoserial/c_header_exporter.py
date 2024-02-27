import os.path
from typing import get_type_hints, Annotated, get_origin, get_args

from jinja2 import Template

from pythonarduinoserial.types import SerializationAnnotation


class CHeaderExporter:
    _default_template = os.path.dirname(__file__) + '/resources/c_header.h.j2'

    def __init__(self, struct_types: list, namespace, include_guard_name, template_filepath=None):
        self._namespace = namespace
        self._include_guard_name = include_guard_name
        self._struct_types = struct_types
        self._template_filepath = self._default_template if template_filepath is None else template_filepath

        self._structs_definitions = list()
        self._structs_names = [struct_type.__name__ for struct_type in self._struct_types]
        self._indent_level = 0

    def _append_to_structs_definitions(self, text):
        self._structs_definitions.append(("    " * self._indent_level) + text)

    def export(self) -> str:
        self._structs_definitions = list()
        self._indent_level = 2

        for struct_type in self._struct_types:
            default_struct = struct_type()
            self._render_object(default_struct)
            self._append_to_structs_definitions("")

        self._structs_definitions.pop(-1)
        structs = "\n".join(self._structs_definitions)

        with open(self._template_filepath, "r") as template_file:
            template = Template(template_file.read())

        # Fixme: really has impact ?
        template.environment.trim_blocks = True
        template.environment.lstrip_blocks = True

        return template.render({
            "namespace": self._namespace,
            "include_guard_name": self._include_guard_name,
            "structs_names": self._structs_names,
            "structs": structs
        })

    def _render_object(self, object_):
        self._append_to_structs_definitions(f"struct {type(object_).__name__} {{")
        self._indent_level += 1

        items = get_type_hints(object_, include_extras=True).items()
        for name, type_hint in items:
            self._render_attribute(name, getattr(object_, name), type_hint)

        self._indent_level -= 1
        self._append_to_structs_definitions("};")

    def _render_attribute(self, name, value, type_hint):
        if get_origin(type_hint) == Annotated:
            type_, annotation = get_args(type_hint)
            if get_origin(type_) == list:
                self._render_list(name, value, type_)
            else:
                self._render_basic_type(name, value, type_, annotation)
        else:
            self._render_object(type_hint)

    def _render_basic_type(self, name, value, type_, annotation):
        assert isinstance(annotation, SerializationAnnotation)

        c_name = self._render_attribute_name(name)
        c_type = annotation.c_name
        c_value = self._render_basic_value(value, type_, annotation)

        if type_ == bytes:
            c_name += f"[{annotation.length}]"

        elif type_ == str:
            c_name += f"[{annotation.length}]"  # null terminating character is last character

        self._append_to_structs_definitions(f"{c_type} {c_name} = {c_value};")

    def _render_list(self, name, value, type_):
        # FIXME: check Annotation length
        sub_hint = get_args(type_)[0]
        type_, annotation = get_args(sub_hint)
        if type_ in [bool, int, float]:
            c_name = self._render_attribute_name(name)
            c_name += f"[{len(value)}]"
            c_type = annotation.c_name
            c_value = f"{{{', '.join([self._render_basic_value(item, type_, annotation) for item in value])}}}"
            self._append_to_structs_definitions(f"{c_type} {c_name} = {c_value};")
        else:
            pass

    @staticmethod
    def _render_attribute_name(name):
        return "".join([word.capitalize() if i > 0 else word for i, word in enumerate(name.split("_"))])

    @staticmethod
    def _render_basic_value(value, type_, annotation):  # FIXME find a better name
        if type_ == bytes:
            return f"{{0x{', 0x'.join(value.hex(sep=' ').split(' '))}}}"

        elif type_ == bool:
            return str(value).lower()

        elif type_ == str:
            if len(value) < annotation.length:
                return f'"{ value + " " * (annotation.length - len(value) - 1) }"'
            else:
                return f'"{ value[:annotation.length - 1] }"'

        elif type_ in [float, int]:
            return str(value)
