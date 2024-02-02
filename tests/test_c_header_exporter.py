"""
This demonstrates usage of `pythonarduinoserial.types` to export C header files
"""
import os.path
from dataclasses import dataclass
from unittest import TestCase

from pythonarduinoserial.c_header_exporter import CHeaderExporter
from pythonarduinoserial.types import *


# FIXME factorize with serializer tests
@dataclass
class AllTypes:
    field_string: StringType(10) = StringDefault(10)
    field_float: FloatType() = 0.0
    field_boolean: BooleanType() = False
    field_integer: IntegerType() = 0
    field_integers: ListType(IntegerType(), 3) = ListDefault(IntegerType(), 3)
    field_bytes: BytesType(5) = BytesDefault(5)


@dataclass
class Nested:
    string: StringType(5) = StringDefault(5)
    nested: AllTypes = AllTypes()
    nesteds: ListType(AllTypes, 2) = ListDefault(AllTypes, 2)


class TestCHeaderExporter(TestCase):

    def setUp(self):
        self.exporter = CHeaderExporter(
            struct_types=[AllTypes],
            namespace="Tests",
            include_guard_name="TESTS_ALL_TYPES_H"
        )

        #
        # Modify each value to ensure default values are used anyways
        self.all_types = AllTypes()
        self.all_types.field_string = "ABCDEFGHIJ"
        self.all_types.field_float = 0.5
        self.all_types.field_boolean = True
        self.all_types.field_integer = 5
        self.all_types.field_integers = [1, 2, 3]
        self.all_types.field_bytes = b'\x01\x02\x03\x04\x05'

        self.nested = Nested()
        self.nested.nested = self.all_types
        self.nested.nesteds = [self.all_types, self.all_types]

        with open(os.path.dirname(__file__) + '/test_all_types.h', 'r') as c_header_file:
            self._all_types_as_c_header = c_header_file.read()

    def test_export_all_types(self):
        output = self.exporter.export().strip()

        self.assertEqual(
            self._all_types_as_c_header,
            output
        )
