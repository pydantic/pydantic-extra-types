from typing import Any, Callable, Generator
from pydantic_core import PydanticCustomError, core_schema

GeneratorCallableStr = Generator[Callable[[str | int], str], None, None]


PhoneNumberError = PydanticCustomError("value_error", "value is not a valid phone number")


class PhoneNumber(str):
    """
    An international phone number
    """
    default_region_code: str | None = None
    min_length: int = 7
    max_length: int = 64


    @classmethod
    def __get_pydantic_core_schema__(cls, **_kwargs: Any) -> core_schema.AfterValidatorFunctionSchema:
        return core_schema.general_after_validator_function(
            cls.validate,
            core_schema.str_schema(
                min_length=cls.min_length, max_length=cls.max_length
            ),
        )

    @classmethod
    def __get_validators__(cls) -> GeneratorCallableStr:
        # yield str_validator
        yield cls.validate

    @classmethod
    def validate(cls, phone_number: str, _: core_schema.ValidationInfo) -> None:
        import phonenumbers

        try:
            parsed_number = phonenumbers.parse(phone_number, cls.default_region_code)
        except phonenumbers.phonenumberutil.NumberParseException as exc:
            raise PhoneNumberError from exc
        if not phonenumbers.is_valid_number(parsed_number):
            raise PhoneNumberError


class USPhoneNumber(PhoneNumber):
    """
    A phone number that defaults to the US
    """
    default_region_code = "US"
