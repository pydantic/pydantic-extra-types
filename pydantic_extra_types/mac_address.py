"""The MAC address module provides functionality to parse and validate MAC addresses in different
formats, such as IEEE 802 MAC-48, EUI-48, EUI-64, or a 20-octet format.
"""

from __future__ import annotations

from typing import Any

from pydantic import GetCoreSchemaHandler
from pydantic_core import PydanticCustomError, core_schema


class MacAddress(str):
    """Represents a MAC address and provides methods for conversion, validation, and serialization.

    ```py
    from pydantic import BaseModel

    from pydantic_extra_types.mac_address import MacAddress


    class Network(BaseModel):
        mac_address: MacAddress


    network = Network(mac_address='00:00:5e:00:53:01')
    print(network)
    # > mac_address='00:00:5e:00:53:01'
    ```
    """

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        """Return a Pydantic CoreSchema with the MAC address validation.

        Args:
            source: The source type to be converted.
            handler: The handler to get the CoreSchema.

        Returns:
            A Pydantic CoreSchema with the MAC address validation.

        """
        return core_schema.with_info_before_validator_function(
            cls._validate,
            core_schema.str_schema(),
        )

    @classmethod
    def _validate(cls, __input_value: str, _: Any) -> str:
        """Validate a MAC Address from the provided str value.

        Args:
            __input_value: The str value to be validated.
            _: The source type to be converted.

        Returns:
            str: The parsed MAC address.

        """
        return cls.validate_mac_address(__input_value.encode())

    @staticmethod
    def validate_mac_address(value: bytes) -> str:
        """Validate a MAC Address from the provided byte value."""
        string = value.decode()
        if len(string) < 14:
            raise PydanticCustomError(
                'mac_address_len',
                'Length for a {mac_address} MAC address must be {required_length}',
                {'mac_address': string, 'required_length': 14},
            )
        for sep, partbytes in ((':', 2), ('-', 2), ('.', 4)):
            if sep in string:
                parts = string.split(sep)
                if any(len(part) != partbytes for part in parts):
                    raise PydanticCustomError(
                        'mac_address_format',
                        f'Must have the format xx{sep}xx{sep}xx{sep}xx{sep}xx{sep}xx',
                    )
                if len(parts) * partbytes // 2 not in (6, 8, 20):
                    raise PydanticCustomError(
                        'mac_address_format',
                        'Length for a {mac_address} MAC address must be {required_length}',
                        {'mac_address': string, 'required_length': (6, 8, 20)},
                    )
                mac_address = []
                for part in parts:
                    for idx in range(0, partbytes, 2):
                        try:
                            byte_value = int(part[idx : idx + 2], 16)
                        except ValueError as exc:
                            raise PydanticCustomError('mac_address_format', 'Unrecognized format') from exc
                        else:
                            mac_address.append(byte_value)
                return ':'.join(f'{b:02x}' for b in mac_address)
        else:
            raise PydanticCustomError('mac_address_format', 'Unrecognized format')
