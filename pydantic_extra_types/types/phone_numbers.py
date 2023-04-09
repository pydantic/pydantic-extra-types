from typing import Callable, Generator
from pydantic import PydanticValueError, str_validator

GeneratorCallableStr = Generator[Callable[[str | int], str], None, None]


class PhoneNumberError(PydanticValueError):
    msg_template = "value is not a valid phone number"


class PhoneNumber(str):
    """
    An international phone number
    """
    default_region_code: str | None = None
    MAX_LENGTH: int = 64

    @classmethod
    def __get_validators__(cls) -> GeneratorCallableStr:
        yield str_validator
        yield cls.validate

    @classmethod
    def validate(cls, phone_number: str) -> None:
        if len(phone_number) > cls.MAX_LENGTH:
            raise PhoneNumberError()

        import phonenumbers

        try:
            parsed_number = phonenumbers.parse(phone_number, cls.default_region_code)
        except phonenumbers.phonenumberutil.NumberParseException as exc:
            raise PhoneNumberError() from exc
        if not phonenumbers.is_valid_number(parsed_number):
            raise PhoneNumberError()


class USPhoneNumber(PhoneNumber):
    """
    A phone number that defaults to the US
    """
    default_region_code = "US"
