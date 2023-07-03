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

    __slots__ = '_mac_address'

    def __init__(self, value: MacAddressType) -> None:
        self._mac_address: str
        if isinstance(value, bytes):
            self._mac_address = validate_mac_address(value)
        elif isinstance(value, str):
            self._mac_address = validate_mac_address(value.encode())
        else:
            raise PydanticCustomError(
                'mac_address_error',
                'value is not a valid Mac Address: value must be a string or bytes',
            )

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.general_after_validator_function(
            cls._validate,
            core_schema.str_schema(),
        )

    @classmethod
    def _validate(cls, __input_value: Any, _: Any) -> MacAddress:
        return cls(__input_value)


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
            'Length for a {mac_address} mac address must be {required_length}',
            {'mac_address': value.decode(), 'required_length': 14},
        )

    if value[2] in [ord(':'), ord('-')]:
        if (len(value) + 1) % 3 != 0:
            raise PydanticCustomError(
                'mac_address_format', 'Must have the format xx:xx:xx:xx:xx:xx or xx-xx-xx-xx-xx-xx'
            )
        n = (len(value) + 1) // 3
    elif value[4] == ord('.'):
        if (len(value) + 1) % 5 != 0:
            raise PydanticCustomError('mac_address_format', 'Must have the format xx.xx.xx.xx.xx.xx')
        n = 2 * (len(value) + 1) // 5
    else:
        raise PydanticCustomError('mac_address_format', 'Unrecognized format')

    if n not in (6, 8, 20):
        raise PydanticCustomError(
            'mac_address_len',
            'Length for a {mac_address}  mac address must be {required_length}',
            {'mac_address': value.decode(), 'required_length': (6, 8, 20)},
        )

    hw = bytearray(n)
    x = 0
    for i in range(0, n, 2):
        try:
            byte_value = int(value[x : x + 2], 16)
            hw[i] = byte_value
            if value[4] == ord('.'):
                byte_value = int(value[x + 2 : x + 4], 16)
                hw[i + 1] = byte_value
                x += 5
            else:
                x += 3
        except ValueError as e:
            raise PydanticCustomError('mac_address_format', 'Unrecognized format') from e

    return ':'.join(f'{b:02x}' for b in hw)
