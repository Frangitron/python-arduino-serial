

class UsbSerialException(IOError):
    """Base class for USB-to-Serial exceptions."""
    pass


class UsbSerialPortNotOpenedError(UsbSerialException):
    """Raised when a port is not opened."""
    pass


class UsbSerialNoDataReceivedError(UsbSerialException):
    """Raised when no data is received from the port."""
    pass


class UsbSerialInvalidDataError(UsbSerialException):
    """Raised when invalid data is received from the port."""
    pass


class UsbSerialStructNotRegisteredError(UsbSerialException):
    """Raised when a C struct is not registered in the communicator."""
    pass
