"""
The `pydantic_extra_types.payment` module provides the
[`PaymentCardNumber`][pydantic_extra_types.payment.PaymentCardNumber] data type.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, ClassVar

from pydantic import GetCoreSchemaHandler
from pydantic_core import PydanticCustomError, core_schema


class PaymentCardBrand(str, Enum):
    """Payment card brands supported by the [`PaymentCardNumber`][pydantic_extra_types.payment.PaymentCardNumber]."""

    amex = 'American Express'
    mastercard = 'Mastercard'
    visa = 'Visa'
    mir = 'Mir'
    other = 'other'

    def __str__(self) -> str:
        return self.value


class PaymentCardNumber(str):
    """A [payment card number](https://en.wikipedia.org/wiki/Payment_card_number)."""

    strip_whitespace: ClassVar[bool] = True
    """Whether to strip whitespace from the input value."""
    min_length: ClassVar[int] = 12
    """The minimum length of the card number."""
    max_length: ClassVar[int] = 19
    """The maximum length of the card number."""
    bin: str
    """The first 6 digits of the card number."""
    last4: str
    """The last 4 digits of the card number."""
    brand: PaymentCardBrand
    """The brand of the card."""

    def __init__(self, card_number: str):
        self.validate_digits(card_number)

        card_number = self.validate_luhn_check_digit(card_number)

        self.bin = card_number[:6]
        self.last4 = card_number[-4:]
        self.brand = self.validate_brand(card_number)

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.with_info_after_validator_function(
            cls.validate,
            core_schema.str_schema(
                min_length=cls.min_length, max_length=cls.max_length, strip_whitespace=cls.strip_whitespace
            ),
        )

    @classmethod
    def validate(cls, __input_value: str, _: core_schema.ValidationInfo) -> PaymentCardNumber:
        """Validate the `PaymentCardNumber` instance.

        Args:
            __input_value: The input value to validate.
            _: The validation info.

        Returns:
            The validated `PaymentCardNumber` instance.
        """
        return cls(__input_value)

    @property
    def masked(self) -> str:
        """The masked card number."""
        num_masked = len(self) - 10  # len(bin) + len(last4) == 10
        return f'{self.bin}{"*" * num_masked}{self.last4}'

    @classmethod
    def validate_digits(cls, card_number: str) -> None:
        """Validate that the card number is all digits.

        Args:
            card_number: The card number to validate.

        Raises:
            PydanticCustomError: If the card number is not all digits.
        """
        if not card_number.isdigit():
            raise PydanticCustomError('payment_card_number_digits', 'Card number is not all digits')

    @classmethod
    def validate_luhn_check_digit(cls, card_number: str) -> str:
        """Validate the payment card number.
        Based on the [Luhn algorithm](https://en.wikipedia.org/wiki/Luhn_algorithm).

        Args:
            card_number: The card number to validate.

        Returns:
            The validated card number.

        Raises:
            PydanticCustomError: If the card number is not valid.
        """
        sum_ = int(card_number[-1])
        length = len(card_number)
        parity = length % 2
        for i in range(length - 1):
            digit = int(card_number[i])
            if i % 2 == parity:
                digit *= 2
            if digit > 9:
                digit -= 9
            sum_ += digit
        valid = sum_ % 10 == 0
        if not valid:
            raise PydanticCustomError('payment_card_number_luhn', 'Card number is not luhn valid')
        return card_number

    @staticmethod
    def validate_brand(card_number: str) -> PaymentCardBrand:
        """Validate length based on
        [BIN](https://en.wikipedia.org/wiki/Payment_card_number#Issuer_identification_number_(IIN))
        for major brands.

        Args:
            card_number: The card number to validate.

        Returns:
            The validated card brand.

        Raises:
            PydanticCustomError: If the card number is not valid.
        """
        if card_number[0] == '4':
            brand = PaymentCardBrand.visa
        elif 51 <= int(card_number[:2]) <= 55:
            brand = PaymentCardBrand.mastercard
        elif card_number[:2] in {'34', '37'}:
            brand = PaymentCardBrand.amex
        elif 2200 <= int(card_number[:4]) <= 2204:
            brand = PaymentCardBrand.mir
        else:
            brand = PaymentCardBrand.other

        required_length: None | int | str = None
        if brand in PaymentCardBrand.mastercard:
            required_length = 16
            valid = len(card_number) == required_length
        elif brand == PaymentCardBrand.visa:
            required_length = '13, 16 or 19'
            valid = len(card_number) in {13, 16, 19}
        elif brand == PaymentCardBrand.amex:
            required_length = 15
            valid = len(card_number) == required_length
        elif brand == PaymentCardBrand.mir:
            required_length = 'in range from 16 to 19'
            valid = len(card_number) in range(16, 20)
        else:
            valid = True

        if not valid:
            raise PydanticCustomError(
                'payment_card_number_brand',
                'Length for a {brand} card must be {required_length}',
                {'brand': brand, 'required_length': required_length},
            )
        return brand
