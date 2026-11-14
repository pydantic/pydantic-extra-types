import pytest
from pydantic import TypeAdapter, ValidationError

from pydantic_extra_types.payment import PaymentCardBrand, PaymentCardNumber


# JCB PANs have 16 through 19 digits, with prefixes 3528 through 3589:
# https://developer.cybersource.com/docs/cybs/en-us/test-data/developer/all/so/test-data.html
@pytest.mark.parametrize(
    'number',
    [
        '3528000000000007',
        '35280000000000007',
        '352800000000000007',
        '3528000000000000007',
        '3589000000000003',
        '35890000000000009',
        '358900000000000003',
        '3589000000000000009',
    ],
)
def test_jcb_accepts_all_supported_lengths(number: str) -> None:
    card = TypeAdapter(PaymentCardNumber).validate_python(number)
    assert card.brand == PaymentCardBrand.jcb
    assert str(card) == number


@pytest.mark.parametrize(
    'number', ['352800000000007', '358900000000009', '35280000000000000007', '35890000000000000003']
)
def test_jcb_rejects_lengths_outside_the_supported_range(number: str) -> None:
    # These inputs pass Luhn, so their lengths are the reason for rejection.
    assert PaymentCardNumber.validate_luhn_check_digit(number) == number
    with pytest.raises(ValidationError):
        TypeAdapter(PaymentCardNumber).validate_python(number)
