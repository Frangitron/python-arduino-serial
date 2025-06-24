from binascii import hexlify


def without_terminator(s: str):
    return s.rstrip('\x00')


def bytes_to_string(b: bytes):
    return str(hexlify(b, sep=' '), 'utf-8')


def string_to_bytes(s: str):
    raise NotImplementedError
