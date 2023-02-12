from typing import Any

import pyotp
from pydantic_core import PydanticCustomError


class OTPToken(str):
    """A one-time password token.

    This is a custom type that can be used to validate a one-time password token
    against a secret key. The secret key is passed in the context argument of
    the model_validate method.

    The type also has a custom JSON encoder that returns the current one-time
    password token for the secret key.
    """

    @staticmethod
    def model_validate(value: Any, *, context: Any) -> Any:
        if not pyotp.TOTP(context['otp_secret']).verify(value):
            raise PydanticCustomError('Invalid one-time password', value)
        return value

    @classmethod
    def get_validators(cls) -> Any:
        yield cls.model_validate

    class Config:
        json_encoders = {pyotp.TOTP: lambda v: v.now()}
