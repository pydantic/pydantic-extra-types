"""
The `pydantic_extra_types.iban` module provides functionality to recieve and validate [IBAN (International Bank Account Number)](https://en.wikipedia.org/wiki/International_Bank_Account_Number).
"""


from __future__ import annotations

from typing import Any

from pydantic import GetCoreSchemaHandler
from pydantic_core import PydanticCustomError, core_schema

try:
    import schwifty
except ModuleNotFoundError:  # pragma: no cover
    raise RuntimeError(
        'The `iban` module requires "schwifty" to be installed. You can install it with "pip install schwifty".'
    )


class Iban(str):
    """Represents a IBAN and provides methods for conversion, validation, and serialization.


    ```py
    from pydantic import BaseModel, constr
    from pydantic_extra_types.iban import Iban
    class IbanExample(BaseModel):
        name: constr(strip_whitespace=True, min_length=1)
        number: Iban
    iban = IbanExample(
        name='Georg Wilhelm Friedrich Hegel',
        number='DE89 3704 0044 0532 0130 00',
    )
    assert iban.number.account_code == '0532013000'
    assert iban.number.bank_code == '37040044'
    assert iban.number.numeric == 370400440532013000131489
    assert iban.number.bic == 'COBADEFFXXX'
    assert iban.number.bank_name == 'Commerzbank'
    assert iban.number.bban == '370400440532013000'
    ```
    """

    def __init__(self, iban: str):
        self.iban = self.validate_iban_digits(iban)

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.with_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(),
        )

    @classmethod
    def _validate(cls, __input_value: str, _: core_schema.ValidationInfo) -> str:
        return cls(__input_value)

    @classmethod
    def validate_iban_digits(cls, iban: str) -> schwifty.iban.IBAN:
        """Validate that the IBAN is all digits."""
        if not isinstance(iban, str):
            raise PydanticCustomError('iban_digits', 'IBAN is invalid')  # pragma: no cover
        return schwifty.IBAN(iban)

    @property
    def bank(self) -> Any:
        """The bank of the IBAN."""
        return self.iban.bank

    @property
    def compact(self) -> str:
        """The compact IBAN."""
        return self.iban.compact

    @property
    def formatted(self) -> str:
        """The formatted IBAN."""
        return self.iban.formatted

    @property
    def account_code(self) -> str:
        """The account code of the IBAN."""
        return self.iban.account_code

    @property
    def bank_code(self) -> str:
        """The bank code of the IBAN."""
        return self.iban.bank_code

    @property
    def numeric(self) -> int:
        """The numeric IBAN."""
        return self.iban.numeric

    @property
    def spec(self) -> Any:
        """The IBAN spec."""
        return self.iban.spec

    @property
    def bic(self) -> None | schwifty.bic.BIC:
        """The BIC of the IBAN."""
        return self.iban.bic

    @property
    def country(self) -> Any:
        """The country of the IBAN."""
        return self.iban.country

    @property
    def bank_name(self) -> None | str:
        """The bank name of the IBAN."""
        return self.iban.bank_name

    @property
    def bank_short_name(self) -> None | str:
        """The bank short name of the IBAN."""
        return self.iban.bank_short_name

    @property
    def branch_code(self) -> str:
        """The branch code of the IBAN."""
        return self.iban.branch_code

    @property
    def bban(self) -> str:
        """The BBAN of the IBAN."""
        return self.iban.bban

    @property
    def checksum_digits(self) -> str:
        """The checksum digits of the IBAN."""
        return self.iban.checksum_digits
