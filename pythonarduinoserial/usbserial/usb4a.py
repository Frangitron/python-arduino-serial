from usb4a import usb
from usbserial4a import serial4a

from pythonarduinoserial.usbserial.abstract import AbstractUsbSerial
from pythonarduinoserial.usbserial.exception import UsbSerialException


class Usb4AUsbSerial(AbstractUsbSerial):

    def __init__(self):
        self._serial_port = None

    def close(self):
        self._serial_port.close()

    def is_buffer_empty(self) -> bool:
        return self._serial_port.in_waiting == 0

    def list_names(self) -> list[str]:
        return [device.getDeviceName() for device in usb.get_usb_device_list()]

    def open(self, name: str):
        self._serial_port = serial4a.get_serial_port(
            device_name=name,
            baudrate=115200,
            dsrdtr=True,
        )

    def read(self) -> bytearray:
        return self._serial_port.read(self._serial_port.in_waiting)

    def write(self, data: bytearray):
        try:
            self._serial_port.write(data)
        except Exception as e:
            raise UsbSerialException(e)
