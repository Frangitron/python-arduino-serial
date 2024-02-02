"""
This demonstrates usage of `pythonarduinoserial.types` to construct bytes-serializable dataclasses
"""
from unittest import TestCase

from tests.values import *

from pythonarduinoserial.byte_serializer import ByteSerializer


class TestSerializeToBytes(TestCase):

    def setUp(self):
        self.serializer = ByteSerializer()

    def test_serialize_all_types(self):
        output = self.serializer.to_bytes(all_types)

        self.assertEqual(
            all_types_as_bytes,
            output
        )

    def test_serialize_nested(self):
        output = self.serializer.to_bytes(nested)

        self.assertEqual(
            nested_as_bytes,
            output
        )
