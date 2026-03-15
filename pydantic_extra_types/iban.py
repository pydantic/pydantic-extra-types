"""The `pydantic_extra_types.iban` module provides functionality to receive and validate IBAN.

IBAN (International Bank Account Number) is an internationally agreed system of identifying
bank accounts across national borders to facilitate the communication and processing of
cross border transactions. For more information, see the
`Wikipedia page <https://en.wikipedia.org/wiki/International_Bank_Account_Number>`_.
"""

from __future__ import annotations

from typing import Any

from pydantic import GetCoreSchemaHandler
from pydantic_core import PydanticCustomError, core_schema

# IBAN lengths per country code (ISO 3166-1 alpha-2)
# Source: https://www.swift.com/standards/data-standards/iban
IBAN_COUNTRY_CODE_LENGTH: dict[str, int] = {
    'AL': 28,
    'AD': 24,
    'AT': 20,
    'AZ': 28,
    'BH': 22,
    'BY': 28,
    'BE': 16,
    'BA': 20,
    'BR': 29,
    'BG': 22,
    'CR': 22,
    'HR': 21,
    'CY': 28,
    'CZ': 24,
    'DK': 18,
    'DO': 28,
    'TL': 23,
    'EG': 29,
    'SV': 28,
    'EE': 20,
    'FO': 18,
    'FI': 18,
    'FR': 27,
    'GE': 22,
    'DE': 22,
    'GI': 23,
    'GR': 27,
    'GL': 18,
    'GT': 28,
    'HU': 28,
    'IS': 26,
    'IQ': 23,
    'IE': 22,
    'IL': 23,
    'IT': 27,
    'JO': 30,
    'KZ': 20,
    'XK': 20,
    'KW': 30,
    'LV': 21,
    'LB': 28,
    'LI': 21,
    'LT': 20,
    'LU': 20,
    'MK': 19,
    'MT': 31,
    'MR': 27,
    'MU': 30,
    'MC': 27,
    'MD': 24,
    'ME': 22,
    'NL': 18,
    'NO': 15,
    'PK': 24,
    'PS': 29,
    'PL': 28,
    'PT': 25,
    'QA': 29,
    'RO': 24,
    'LC': 32,
    'SM': 27,
    'ST': 25,
    'SA': 24,
    'RS': 22,
    'SC': 31,
    'SK': 24,
    'SI': 19,
    'ES': 24,
    'SD': 18,
    'SE': 24,
    'CH': 21,
    'TN': 24,
    'TR': 26,
    'UA': 29,
    'AE': 23,
    'GB': 22,
    'VA': 22,
    'VG': 24,
}


def _validate_iban_check_digits(iban: str) -> bool:
    """Validate IBAN check digits using the MOD-97 algorithm (ISO 7064).

    The algorithm:
    1. Move the first four characters to the end
    2. Convert letters to numbers (A=10, B=11, ..., Z=35)
    3. Compute remainder of the resulting number divided by 97
    4. If remainder is 1, the IBAN is valid
    """
    rearranged = iban[4:] + iban[:4]
    numeric = ''
    for char in rearranged:
        if char.isdigit():
            numeric += char
        else:
            numeric += str(ord(char) - ord('A') + 10)
    return int(numeric) % 97 == 1


class IBAN(str):
    """Represents an International Bank Account Number (IBAN).

    ```python
    from pydantic import BaseModel

    from pydantic_extra_types.iban import IBAN


    class BankAccount(BaseModel):
        iban: IBAN


    account = BankAccount(iban='GB29NWBK60161331926819')
    print(account)
    # > iban='GB29NWBK60161331926819'
    ```
    """

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source: type[Any],
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        return core_schema.with_info_before_validator_function(
            cls._validate,
            core_schema.str_schema(),
        )

    @classmethod
    def _validate(cls, __input_value: str, _: Any) -> IBAN:
        # Remove spaces and convert to uppercase
        iban = __input_value.replace(' ', '').upper()

        # Check minimum length
        if len(iban) < 5:
            raise PydanticCustomError('iban_invalid_length', 'Invalid IBAN: too short')

        # Check that first two characters are letters (country code)
        country_code = iban[:2]
        if not country_code.isalpha():
            raise PydanticCustomError(
                'iban_invalid_country_code',
                'Invalid IBAN: country code must be two letters',
            )

        # Validate country code and length
        expected_length = IBAN_COUNTRY_CODE_LENGTH.get(country_code)
        if expected_length is None:
            raise PydanticCustomError(
                'iban_invalid_country_code',
                'Invalid IBAN: unknown country code {country_code}',
                {'country_code': country_code},
            )

        if len(iban) != expected_length:
            raise PydanticCustomError(
                'iban_invalid_length',
                'Invalid IBAN: expected {expected_length} characters for {country_code}, got {actual_length}',
                {
                    'expected_length': expected_length,
                    'country_code': country_code,
                    'actual_length': len(iban),
                },
            )

        # Check that remaining characters are alphanumeric
        if not iban[2:].isalnum():
            raise PydanticCustomError(
                'iban_invalid_characters',
                'Invalid IBAN: must contain only alphanumeric characters',
            )

        # Validate check digits (positions 3-4 must be digits)
        if not iban[2:4].isdigit():
            raise PydanticCustomError(
                'iban_invalid_check_digits',
                'Invalid IBAN: check digits must be numeric',
            )

        # Validate using MOD-97 algorithm
        if not _validate_iban_check_digits(iban):
            raise PydanticCustomError(
                'iban_invalid_checksum',
                'Invalid IBAN: checksum validation failed',
            )

        return cls(iban)
