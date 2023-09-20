from typing import Any, ClassVar, Type

from pydantic import GetCoreSchemaHandler
from pydantic_core import PydanticCustomError, core_schema


class ABARoutingNumber(str):
    strip_whitespace: ClassVar[bool] = True
    min_length: ClassVar[int] = 9
    max_length: ClassVar[int] = 9

    def __init__(self, routing_number: str):
        self.validate_digits(routing_number)
        self._routing_number = self.validate_routing_number(routing_number)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: Type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.AfterValidatorFunctionSchema:
        return core_schema.general_after_validator_function(
            cls.validate,
            core_schema.str_schema(
                min_length=cls.min_length,
                max_length=cls.max_length,
                strip_whitespace=cls.strip_whitespace,
                strict=False,
            ),
        )

    @classmethod
    def validate(cls, __input_value: str, _: core_schema.ValidationInfo) -> 'ABARoutingNumber':
        return cls(__input_value)

    @classmethod
    def validate_digits(cls, routing_number: str) -> None:
        if not routing_number.isdigit():
            raise PydanticCustomError('aba_routing_number', 'routing number is not all digits')

    @classmethod
    def validate_routing_number(cls, routing_number: str) -> str:
        """
        Check digit algorithm for ABA routing transit number.
        https://en.wikipedia.org/wiki/ABA_routing_transit_number#Check_digit
        https://www.routingnumber.com/
        """
        checksum = (
            3 * (sum(map(int, [routing_number[0], routing_number[3], routing_number[6]])))
            + 7 * (sum(map(int, [routing_number[1], routing_number[4], routing_number[7]])))
            + sum(map(int, [routing_number[2], routing_number[5], routing_number[8]]))
        )
        if checksum % 10 != 0:
            raise PydanticCustomError('aba_routing_number', 'Incorrect ABA routing transit number')
        return routing_number
