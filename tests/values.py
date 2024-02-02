from dataclasses import dataclass

from pythonarduinoserial.types import *


#
# Define dataclasses and default values
@dataclass
class AllTypes:
    string: StringType(10) = StringDefault(10)
    float: FloatType() = 0.0
    boolean: BooleanType() = False
    integer: IntegerType() = 0
    integers: ListType(IntegerType(), 3) = ListDefault(IntegerType(), 3)
    bytes: BytesType(5) = BytesDefault(5)


@dataclass
class Nested:
    string: StringType(5) = StringDefault(5)
    nested: AllTypes = AllTypes()
    nesteds: ListType(AllTypes, 2) = ListDefault(AllTypes, 2)


#
# Modify each value to ensure actual data is serialized (not default values)
all_types = AllTypes()
all_types.string = "ABCDEFGHI\x00"  # null terminator included or last character will be replaced
all_types.float = 0.5
all_types.boolean = True
all_types.integer = 5
all_types.integers = [1, 2, 3]
all_types.bytes = b'\x01\x02\x03\x04\x05'


nested = Nested()
nested.nested = all_types
nested.nesteds = [all_types, all_types]

#
# Bytes representations
all_types_as_bytes = (
    b'\x41\x42\x43\x44\x45\x46\x47\x48\x49\x00'  # string with null terminator as last char
    b'\x00\x00'  # padding
    b'\x00\x00\x00\x3f'  # float
    b'\x01'  # bool
    b'\x00\x00\x00'  # padding
    b'\x05\x00\x00\x00'  # int
    b'\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00'  # [int, int, int]
    b'\x01\x02\x03\x04\x05'  # [byte, byte, byte, byte, byte]
)


nested_as_bytes = (
        b'\x20\x20\x20\x20\x00' +  # string with null terminator as last char
        all_types_as_bytes * 3
)
