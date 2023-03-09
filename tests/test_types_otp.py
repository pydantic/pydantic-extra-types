import pyotp
import pytest
from pydantic_core import PydanticCustomError

from pydantic_extra_types import OTPToken


def test_model_validate():
    secret = 'JBSWY3DPEHPK3PXP'
    totp = pyotp.TOTP(secret)
    value = totp.now()
    context = {'otp_secret': secret}
    # Test a valid OTP token
    result = OTPToken.model_validate(value, context=context)
    assert result == value

    # Test an invalid OTP token
    with pytest.raises(PydanticCustomError, match='Invalid one-time password'):
        OTPToken.model_validate('Invalid one-time password', context=context)


def test_json_encoder():
    secret = 'JBSWY3DPEHPK3PXP'
    totp = pyotp.TOTP(secret)
    value = totp.now()

    # Test the custom JSON encoder
    json_encoded_value = OTPToken.Config.json_encoders[pyotp.TOTP](totp)
    assert json_encoded_value == value


def test___get_pydantic_core_schema__():
    # Test the get_validators method
    validators = list(OTPToken.__get_pydantic_core_schema__())
    assert validators == [OTPToken.model_validate]
