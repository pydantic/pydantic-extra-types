import pytest
from pydantic import TypeAdapter, ValidationError

from pydantic_extra_types.payment import PaymentCardBrand, PaymentCardNumber


@pytest.mark.parametrize(
    'number',
    [
        '6200000000000005',
        '62000000000000000',
        '620000000000000005',
        '6200000000000000000',
        '8100000000000002',
        '81000000000000000',
        '810000000000000002',
        '8100000000000000000',
    ],
)
def test_unionpay_accepts_all_supported_lengths(number: str) -> None:
    card = TypeAdapter(PaymentCardNumber).validate_python(number)
    assert card.brand == PaymentCardBrand.unionpay
    assert str(card) == number


@pytest.mark.parametrize('number', ['620000000000000', '810000000000000', '62000000000000000005'])
def test_unionpay_rejects_lengths_outside_supported_range(number: str) -> None:
    assert PaymentCardNumber.validate_luhn_check_digit(number) == number
    with pytest.raises(ValidationError):
        TypeAdapter(PaymentCardNumber).validate_python(number)
