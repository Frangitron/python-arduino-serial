# Python Arduino Serial

**/!\ BETA VERSION**

Bidirectionnal serial communication (C Structs and Python Dataclasses) between Python and Arduino

- declare type hinted Dataclasses in Python
- generate C Header files
- send and receive data from both Python and Arduino through serial communication

Meant to be used with [Arduino Python Serial](https://github.com/MrFrangipane/arduino-python-serial)

## Usage

- Data serialization examples can be found in [the tests](tests/test_bytes_serialization.py)
- Header generation example can be found in [the tests](tests/test_c_header_exporter.py)

## Protocol

Message topology (bytes)

|    0    |     1     |     2     |  n   |  n + 3  |
|:-------:|:---------:|:---------:|:----:|:-------:|
|  begin  | direction | data type | data |   end   |
| ------- |  header   |  header   | data | ------- |

**note** data is omitted when sending a reception request (only data type is sent)

## TODO

- [ ] Deal with byte alignment and place 'x's in struct format
- [ ] Nested structure support for CHeaderExporter
