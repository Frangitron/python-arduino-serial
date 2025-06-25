from binascii import hexlify
from typing import Type
import logging
import time

from pythonarduinoserial.base_c_struct import BaseCStruct
from pythonarduinoserial.byte_deserializer import ByteDeserializer
from pythonarduinoserial.byte_serializer import ByteSerializer
from pythonarduinoserial.usbserial.api import get_usb_serial
from pythonarduinoserial.usbserial.exception import (
    UsbSerialException,
    UsbSerialInvalidDataError,
    UsbSerialNoDataReceivedError,
    UsbSerialPortNotOpenedError,
    UsbSerialStructNotRegisteredError,
)

_logger = logging.getLogger(__name__)


class SerialCommunicator:
    _wait_before_receive = 0.03

    header_size = 2

    class Flag:
        Begin = 0x3c  # "<"
        End = 0x3e  # ">"

    class Direction:
        Send = 0
        Receive = 1

    # FIXME: create a SerialProtocol class ?
    def __init__(self, structs: list):
        self.serial_port_name: str = None

        self._structs = structs
        self._serial_port = get_usb_serial()
        self._is_serial_port_open = False

    @staticmethod
    def get_port_names():
        return get_usb_serial().list_names()

    def set_port_name(self, port_name):
        self._disconnect()
        self.serial_port_name = port_name

    def __del__(self):
        self._disconnect()

    def send(self, struct_: BaseCStruct):
        data = ByteSerializer().to_bytes(struct_)
        try:
            type_code = self._structs.index(type(struct_))
        except ValueError:
            # FIXME: create a SerialProtocol class ?
            raise UsbSerialStructNotRegisteredError(
                f"Struct {type(struct_)} is missing from structs list. Have you passed it to the constructor?"
            )

        message = bytearray([self.Flag.Begin, self.Direction.Send, type_code])
        message += data
        message += bytearray([self.Flag.End])

        self._connect()
        self._serial_port.write(message)

        _logger.debug(f"Sent {hexlify(message, sep=' ')}")

    def receive(self, struct_type: Type[BaseCStruct]) -> BaseCStruct | None:
        self._connect()
        if not self._is_serial_port_open:
            raise UsbSerialPortNotOpenedError(f"Serial port {self.serial_port_name} is not open")

        type_code = self._structs.index(struct_type)
        message = bytearray([self.Flag.Begin, self.Direction.Receive, type_code, self.Flag.End])
        self._serial_port.write(message)
        time.sleep(self._wait_before_receive)

        response = bytearray()
        while not self._serial_port.is_buffer_empty():
            response += self._serial_port.read()

        if len(response) == 0:
            raise UsbSerialNoDataReceivedError(
                f"Nothing received while requesting {struct_type.__name__}. "
                f"Is device a LEDBoard or Serial Protocol mismatch ? "
                f"({self.serial_port_name}) "
            )

        _logger.debug(f"Received {hexlify(response, sep=' ')}")
        _logger.debug(
            f"Parsing {hexlify(response[self.header_size + 1:-1], sep=' ')}, "
            f"len={len(response[self.header_size + 1:-1])}"
        )

        deserialized = ByteDeserializer(response[self.header_size + 1:-1]).to_object(struct_type)
        if deserialized is None:
            raise UsbSerialInvalidDataError(
                f"Failed to deserialize {struct_type.__name__} ({self.serial_port_name}). "
                f"Maybe timings are too short ?"
            )

        return deserialized

    def _connect(self):
        if self.serial_port_name is None:
            raise UsbSerialException("Serial port name is not set")

        if not self._is_serial_port_open:
            self._serial_port.open(self.serial_port_name)
            self._is_serial_port_open = True

    def _disconnect(self):
        if self._is_serial_port_open:
            self._serial_port.close()
            self._is_serial_port_open = False
