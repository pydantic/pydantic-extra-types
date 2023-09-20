"""
MAC address Parsing and Validation

This code provides functionality to parse and validate MAC addresses in different formats, such as IEEE 802 MAC-48,
EUI-48, EUI-64, or a 20-octet format. It includes a `MacAddress` class that represents a Mac Address and provides
methods for conversion, validation, and serialization. The code also includes a `validate_mac_address` function
that takes a byte value representing a Mac Address and returns the parsed Mac Address as a string.
"""

from __future__ import annotations

from typing import Any, Union

from pydantic import GetCoreSchemaHandler
from pydantic_core import PydanticCustomError, core_schema

MacAddressType = Union[str, bytes]


class MacAddress(str):
    """
    Represents a mac address - IEEE 802 MAC-48, EUI-48, EUI-64, or a 20-octet
    """

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.general_before_validator_function(
            cls._validate,
            core_schema.str_schema(),
        )

    @classmethod
    def _validate(cls, __input_value: str, _: Any) -> str:
        return cls.validate_mac_address(__input_value.encode())

    @staticmethod
    def validate_mac_address(value: bytes) -> str:
        """
        Validate a Mac Address from the provided byte value.

        Args:
            value (bytes): The byte value representing the Mac Address.

        Returns:
            str: The parsed Mac Address as a string.

        Raises:
            PydanticCustomError: If the value is not a valid Mac Address.
        """
        if len(value) < 14:
            raise PydanticCustomError(
                'mac_address_len',
                'Length for a {mac_address} MAC address must be {required_length}',
                {'mac_address': value.decode(), 'required_length': 14},
            )

        if value[2] in [ord(':'), ord('-')]:
            if (len(value) + 1) % 3 != 0:
                raise PydanticCustomError(
                    'mac_address_format', 'Must have the format xx:xx:xx:xx:xx:xx or xx-xx-xx-xx-xx-xx'
                )
            n = (len(value) + 1) // 3
            if n not in (6, 8, 20):
                raise PydanticCustomError(
                    'mac_address_format',
                    'Length for a {mac_address} MAC address must be {required_length}',
                    {'mac_address': value.decode(), 'required_length': (6, 8, 20)},
                )
            mac_address = bytearray(n)
            x = 0
            for i in range(n):
                try:
                    byte_value = int(value[x : x + 2], 16)
                    mac_address[i] = byte_value
                    x += 3
                except ValueError as e:
                    raise PydanticCustomError('mac_address_format', 'Unrecognized format') from e

        elif value[4] == ord('.'):
            if (len(value) + 1) % 5 != 0:
                raise PydanticCustomError('mac_address_format', 'Must have the format xx.xx.xx.xx.xx.xx')
            n = 2 * (len(value) + 1) // 5
            if n not in (6, 8, 20):
                raise PydanticCustomError(
                    'mac_address_format',
                    'Length for a {mac_address} MAC address must be {required_length}',
                    {'mac_address': value.decode(), 'required_length': (6, 8, 20)},
                )
            mac_address = bytearray(n)
            x = 0
            for i in range(0, n, 2):
                try:
                    byte_value = int(value[x : x + 2], 16)
                    mac_address[i] = byte_value
                    byte_value = int(value[x + 2 : x + 4], 16)
                    mac_address[i + 1] = byte_value
                    x += 5
                except ValueError as e:
                    raise PydanticCustomError('mac_address_format', 'Unrecognized format') from e

        else:
            raise PydanticCustomError('mac_address_format', 'Unrecognized format')

        return ':'.join(f'{b:02x}' for b in mac_address)
