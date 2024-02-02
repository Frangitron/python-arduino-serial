"""
This demonstrates usage of `pythonarduinoserial.types` to construct bytes-serializable dataclasses
"""
from unittest import TestCase

from tests.values import *

from pythonarduinoserial.byte_deserializer import ByteDeserializer


class TestDeserializeFromBytes(TestCase):

    def test_deserialize_all_types(self):
        deserializer = ByteDeserializer(all_types_as_bytes)
        output = deserializer.to_object(AllTypes)

        self.assertEqual(
            all_types,
            output
        )

    def test_deserialize_nested(self):
        deserializer = ByteDeserializer(nested_as_bytes)
        output = deserializer.to_object(Nested)

        self.assertEqual(
            nested,
            output
        )
