"""The `pydantic_extra_types.routing_number` module provides the
[`ABARoutingNumber`][pydantic_extra_types.routing_number.ABARoutingNumber] data type.
"""

from typing import Any, ClassVar

from pydantic import GetCoreSchemaHandler
from pydantic_core import PydanticCustomError, core_schema


class ABARoutingNumber(str):
    """The `ABARoutingNumber` data type is a string of 9 digits representing an ABA routing transit number.

    The algorithm used to validate the routing number is described in the
    [ABA routing transit number](https://en.wikipedia.org/wiki/ABA_routing_transit_number#Check_digit)
    Wikipedia article.

    ```py
    from pydantic import BaseModel

    from pydantic_extra_types.routing_number import ABARoutingNumber


    class BankAccount(BaseModel):
        routing_number: ABARoutingNumber


    account = BankAccount(routing_number='122105155')
    print(account)
    # > routing_number='122105155'
    ```
    """

    strip_whitespace: ClassVar[bool] = True
    min_length: ClassVar[int] = 9
    max_length: ClassVar[int] = 9

    def __init__(self, routing_number: str):
        self._validate_digits(routing_number)
        self._routing_number = self._validate_routing_number(routing_number)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.AfterValidatorFunctionSchema:
        return core_schema.with_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(
                min_length=cls.min_length,
                max_length=cls.max_length,
                strip_whitespace=cls.strip_whitespace,
                strict=False,
            ),
        )

    @classmethod
    def _validate(cls, __input_value: str, _: core_schema.ValidationInfo) -> 'ABARoutingNumber':
        return cls(__input_value)

    @classmethod
    def _validate_digits(cls, routing_number: str) -> None:
        """Check that the routing number is all digits.

        Args:
            routing_number: The routing number to validate.

        Raises:
            PydanticCustomError: If the routing number is not all digits.
        """
        if not routing_number.isdigit():
            raise PydanticCustomError('aba_routing_number', 'routing number is not all digits')

    @classmethod
    def _validate_routing_number(cls, routing_number: str) -> str:
        """Check [digit algorithm](https://en.wikipedia.org/wiki/ABA_routing_transit_number#Check_digit) for
        [ABA routing transit number](https://www.routingnumber.com/).

        Args:
            routing_number: The routing number to validate.

        Raises:
            PydanticCustomError: If the routing number is incorrect.
        """
        checksum = (
            3 * (sum(map(int, [routing_number[0], routing_number[3], routing_number[6]])))
            + 7 * (sum(map(int, [routing_number[1], routing_number[4], routing_number[7]])))
            + sum(map(int, [routing_number[2], routing_number[5], routing_number[8]]))
        )
        if checksum % 10 != 0:
            raise PydanticCustomError('aba_routing_number', 'Incorrect ABA routing transit number')
        return routing_number
