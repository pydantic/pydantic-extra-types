from __future__ import annotations

from typing import Any

from pydantic import GetCoreSchemaHandler
from pydantic_core import PydanticCustomError, core_schema

try:
    import schwifty  # type: ignore[import]
except ModuleNotFoundError:  # pragma: no cover
    raise RuntimeError(
        'The `iban` module requires "schwifty" to be installed. You can install it with "pip install schwifty".'
    )


class Iban(str):
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
        if not isinstance(iban, str):
            raise PydanticCustomError('iban_digits', 'IBAN is invalid')  # pragma: no cover
        return schwifty.IBAN(iban)

    @property
    def bank(self) -> Any:
        return self.iban.bank

    @property
    def compact(self) -> str:
        return self.iban.compact

    @property
    def formatted(self) -> str:
        return self.iban.formatted

    @property
    def account_code(self) -> str:
        return self.iban.account_code

    @property
    def bank_code(self) -> str:
        return self.iban.bank_code

    @property
    def numeric(self) -> int:
        return self.iban.numeric

    @property
    def spec(self) -> Any:
        return self.iban.spec

    @property
    def bic(self) -> None | schwifty.bic.BIC:
        return self.iban.bic

    @property
    def country(self) -> Any:
        return self.iban.country

    @property
    def bank_name(self) -> None | str:
        return self.iban.bank_name

    @property
    def bank_short_name(self) -> None | str:
        return self.iban.bank_short_name

    @property
    def branch_code(self) -> str:
        return self.iban.branch_code

    @property
    def bban(self) -> str:
        return self.iban.bban

    @property
    def checksum_digits(self) -> str:
        return self.iban.checksum_digits
