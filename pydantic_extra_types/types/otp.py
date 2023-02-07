from typing import Any, ClassVar

from pydantic_core import PydanticCustomError, core_schema

# Default OTP Number of Digits
OTP_ALPHABET = '0123456789'


class OTP(str):
    """
    One-time password
    """

    strip_whitespace: ClassVar[bool] = True
    min_length: ClassVar[int] = 6
    max_length: ClassVar[int] = 6

    def __init__(self, otp: str):
        self.validate_digits(otp)
        self.validate_length(otp)

    @classmethod
    def __get_pydantic_core_schema__(cls, **_kwargs: Any) -> core_schema.FunctionSchema:
        return core_schema.function_after_schema(
            core_schema.str_schema(
                min_length=cls.min_length, max_length=cls.max_length, strip_whitespace=cls.strip_whitespace
            ),
            cls.validate,
        )

    @classmethod
    def validate(cls, __input_value: str, **_kwargs: Any) -> 'OTP':
        return cls(__input_value)

    @classmethod
    def validate_digits(cls, otp: str) -> None:
        if not otp.isdigit():
            raise PydanticCustomError('otp_digits', 'OTP is not all digits')

    @classmethod
    def validate_length(cls, otp: str) -> None:
        if len(otp) != cls.max_length:
            raise PydanticCustomError('otp_length', 'OTP must be {length} digits', {'length': cls.max_length})
