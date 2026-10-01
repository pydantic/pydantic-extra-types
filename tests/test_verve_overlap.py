import pytest
from pydantic import TypeAdapter, ValidationError

from pydantic_extra_types.payment import PaymentCardBrand, PaymentCardNumber


@pytest.mark.parametrize('prefix', ['650002', '650027'])
@pytest.mark.parametrize('length', [16, 18, 19])
def test_verve_takes_precedence_over_discover(prefix: str, length: int) -> None:
    base = prefix + '0' * (length - 7)
    for digit in '0123456789':
        number = base + digit
        try:
            PaymentCardNumber.validate_luhn_check_digit(number)
        except ValueError:
            continue
        break
    card = TypeAdapter(PaymentCardNumber).validate_python(number)
    assert card.brand == PaymentCardBrand.verve
    assert card.bin == prefix
    assert card.last4 == number[-4:]


@pytest.mark.parametrize('prefix', ['650001', '650028', '651000'])
def test_discover_outside_verve_range(prefix: str) -> None:
    assert PaymentCardNumber.validate_brand(prefix + '0' * 10) == PaymentCardBrand.discover


def test_verve_overlap_enforces_verve_lengths() -> None:
    # This 17-digit number passes Luhn, but only Discover accepts that length.
    with pytest.raises(ValidationError, match='Length for a Verve card'):
        TypeAdapter(PaymentCardNumber).validate_python('65000200000000009')
