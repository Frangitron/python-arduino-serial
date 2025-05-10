from pythonarduinoserial.usbserial.abstract import AbstractUsbSerial

try:
    from pythonarduinoserial.usbserial.usb4a import Usb4AUsbSerial as Implementation
except ModuleNotFoundError:
    from pythonarduinoserial.usbserial.pyserial import PySerialUsbSerial as Implementation


def get_usb_serial() -> AbstractUsbSerial:
    return Implementation()
