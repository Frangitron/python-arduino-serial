from binascii import hexlify
import logging
import time
from typing import Type

from pythonarduinoserial.base_c_struct import BaseCStruct
from pythonarduinoserial.byte_deserializer import ByteDeserializer
from pythonarduinoserial.byte_serializer import ByteSerializer
from pythonarduinoserial.usbserial.api import get_usb_serial
from pythonarduinoserial.usbserial.exception import UsbSerialException

_logger = logging.getLogger(__name__)


class SerialCommunicator:
    _wait_before_receive = 0.2

    header_size = 2

    class Flag:
        Begin = 0x3c  # "<"
        End = 0x3e  # ">"

    class Direction:
        Send = 0
        Receive = 1

    def __init__(self, structs: list):
        self.serial_port_name: str = None

        self._structs = structs
        self._serial_port = get_usb_serial()
        self._is_serial_port_open = False

    def set_port_name(self, name):
        self.disconnect()
        self.serial_port_name = name
        self.connect()
        self.disconnect()

    def connect(self):
        if self.serial_port_name is None:
            return False

        if not self._is_serial_port_open:
            self._serial_port.open(self.serial_port_name)
            self._is_serial_port_open = True

        return True

    def disconnect(self):
        if self._is_serial_port_open:
            self._serial_port.close()
            self._is_serial_port_open = False

    def send(self, struct_: BaseCStruct):
        data = ByteSerializer().to_bytes(struct_)
        try:
            type_code = self._structs.index(type(struct_))
        except ValueError:
            raise UsbSerialException(f"Struct {type(struct_)} is missing from structs list. Have you passed it to the constructor?")

        message = bytearray([self.Flag.Begin, self.Direction.Send, type_code])
        message += data
        message += bytearray([self.Flag.End])

        self.connect()
        # TODO check if needed for Android ?
        try:
            self._serial_port.write(message)
        except UsbSerialException:
            self._is_serial_port_open = False
            self.connect()
            self._serial_port.write(message)

        _logger.debug(f"Sent {hexlify(message, sep=' ')}")

    def receive(self, struct_type: Type[BaseCStruct]) -> BaseCStruct | None:
        self.connect()
        if not self._is_serial_port_open:
            raise UsbSerialException("Serial port is not open")

        type_code = self._structs.index(struct_type)
        message = bytearray([self.Flag.Begin, self.Direction.Receive, type_code, self.Flag.End])

        try:
            self._serial_port.write(message)
        except UsbSerialException:
            self._is_serial_port_open = False
            self.connect()
            self._serial_port.write(message)

        time.sleep(self._wait_before_receive)

        response = bytearray()
        while not self._serial_port.is_buffer_empty():
            response += self._serial_port.read()

        if len(response) == 0:
            raise UsbSerialException(
                f"Nothing received while requesting {struct_type.__name__}, "
                f"probably not a LEDBoard on this port "
                f"({self.serial_port_name}) "
            )

        _logger.debug(f"Received {hexlify(response, sep=' ')}")
        _logger.debug(
            f"Parsing {hexlify(response[self.header_size + 1:-1], sep=' ')}, "
            f"len={len(response[self.header_size + 1:-1])}"
        )

        self.disconnect()

        deserialized = ByteDeserializer(response[self.header_size + 1:-1]).to_object(struct_type)
        if deserialized is None:
            raise UsbSerialException(f"Failed to deserialize {struct_type.__name__}")

        return deserialized
