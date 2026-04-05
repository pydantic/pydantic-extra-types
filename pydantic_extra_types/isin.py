"""The `pydantic_extra_types.isin` module provides functionality to receive and validate ISIN.

ISIN (International Securities Identification Number) is a 12-character alphanumeric code
that uniquely identifies a security. This module provides an ISIN type for Pydantic models.
"""

from __future__ import annotations

from typing import Any

from pydantic import GetCoreSchemaHandler
from pydantic_core import PydanticCustomError, core_schema


def _isin_to_digits(isin: str) -> str:
    """Convert ISIN characters to a numeric representation.

    Letters are converted as A=10, ..., Z=35.

    Args:
        isin: The ISIN value to convert.

    Returns:
        A string containing only digits.
    """
    digits = []
    for character in isin:
        if character.isdigit():
            digits.append(character)
        else:
            digits.append(str(ord(character) - ord('A') + 10))
    return ''.join(digits)


def _validate_isin_check_digit(isin: str) -> bool:
    """Validate ISIN check digit using the Luhn algorithm.

    Args:
        isin: The full ISIN value in uppercase.

    Returns:
        Whether the ISIN check digit is valid.
    """
    digits = _isin_to_digits(isin)

    total = 0
    for idx, digit in enumerate(reversed(digits)):
        number = int(digit)
        if idx % 2 == 1:
            number *= 2
            if number > 9:
                number -= 9
        total += number

    return total % 10 == 0


class ISIN(str):
    """Represents an ISIN and provides methods for validation and serialization.

    ```py
    from pydantic import BaseModel

    from pydantic_extra_types.isin import ISIN


    class Security(BaseModel):
        isin: ISIN


    security = Security(isin='US0378331005')
    print(security)
    # > isin='US0378331005'
    ```
    """

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source: type[Any],
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        """Return a Pydantic CoreSchema with the ISIN validation.

        Args:
            source: The source type to be converted.
            handler: The handler to get the CoreSchema.

        Returns:
            A Pydantic CoreSchema with the ISIN validation.
        """
        return core_schema.with_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(strip_whitespace=True),
        )

    @classmethod
    def _validate(cls, __input_value: str, _: Any) -> ISIN:
        """Validate an ISIN from the provided str value.

        Args:
            __input_value: The str value to be validated.
            _: The source type to be converted.

        Returns:
            The validated ISIN.

        Raises:
            PydanticCustomError: If the ISIN is not valid.
        """
        value = __input_value.upper()
        cls.validate_isin_format(value)
        return cls(value)

    @staticmethod
    def validate_isin_format(value: str) -> None:
        """Validate ISIN format from the provided str value.

        Args:
            value: The str value representing the ISIN.

        Raises:
            PydanticCustomError: If the ISIN is not valid.
        """
        isin_length = len(value)

        if isin_length != 12:
            raise PydanticCustomError('isin_length', f'Length for ISIN must be 12 characters, not {isin_length}')

        if not value.isalnum():
            raise PydanticCustomError('isin_invalid_characters', 'All characters of ISIN must be letters or digits')

        if not value[:2].isalpha():
            raise PydanticCustomError('isin_invalid_country_code', 'The first 2 characters of ISIN must be letters')

        if not value[-1].isdigit():
            raise PydanticCustomError('isin_invalid_check_digit', 'The last character of ISIN must be an integer')

        if not _validate_isin_check_digit(value):
            raise PydanticCustomError('isin_invalid_check_digit', 'Provided digit is invalid for given ISIN')
