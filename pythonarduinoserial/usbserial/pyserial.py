import serial
from serial.tools import list_ports

from pythonarduinoserial.usbserial.abstract import AbstractUsbSerial
from pythonarduinoserial.usbserial.exception import UsbSerialException


# TODO use UsbSerialException everywhere
class PySerialUsbSerial(AbstractUsbSerial):
    """
    Manages USB serial communication using the PySerial library

    This class provides methods to interact with USB serial ports, including
    opening and closing connections, reading from and writing to the port, and
    listing available ports. It allows for efficient management of serial
    communication for devices connected via USB.
    """

    def __init__(self):
        self._serial_port: serial.Serial | None = None

    def close(self):
        try:
            self._serial_port.close()
        except serial.SerialException as e:
            raise UsbSerialException(e)

    def is_buffer_empty(self) -> bool:
        return self._serial_port.in_waiting == 0

    def list_names(self) -> list[str]:
        return [port.name for port in list_ports.comports()]

    def open(self, name: str):
        try:
            self._serial_port = serial.Serial()
            self._serial_port.baudrate = 115200
            self._serial_port.dtr = True
            self._serial_port.port = name
            self._serial_port.timeout = 2
            self._serial_port.write_timeout = 2
            self._serial_port.open()
        except serial.SerialException as e:
            raise UsbSerialException(e)

    def read(self) -> bytearray:
        return self._serial_port.read(self._serial_port.in_waiting)

    def write(self, data: bytearray):
        try:
            self._serial_port.write(data)
            self._serial_port.flush()
        except serial.SerialException as e:
            raise UsbSerialException(e)
