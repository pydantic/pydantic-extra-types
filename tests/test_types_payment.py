from collections import namedtuple
from typing import Any

import pytest
from pydantic import BaseModel, ValidationError
from pydantic_core._pydantic_core import PydanticCustomError

from pydantic_extra_types.payment import PaymentCardBrand, PaymentCardNumber

VALID_AMEX = '370000000000002'
VALID_MC = '5100000000000003'
VALID_VISA_13 = '4050000000001'
VALID_VISA_16 = '4050000000000001'
VALID_VISA_19 = '4050000000000000001'
VALID_MIR_16 = '2200000000000004'
VALID_MIR_17 = '22000000000000004'
VALID_MIR_18 = '220000000000000004'
VALID_MIR_19 = '2200000000000000004'
VALID_DISCOVER = '6011000000000004'
VALID_VERVE_16 = '5061000000000001'
VALID_VERVE_18 = '506100000000000001'
VALID_VERVE_19 = '5061000000000000001'
VALID_DANKORT = '5019000000000000'
VALID_UNIONPAY_16 = '6200000000000001'
VALID_UNIONPAY_19 = '8100000000000000001'
VALID_JCB_16 = '3528000000000001'
VALID_JCB_19 = '3528000000000000001'
VALID_MAESTRO = '6759649826438453'
VALID_TROY = '9792000000000001'
VALID_OTHER = '2000000000000000008'
VALID_DINERS_CLUB_14 = '30500000000000'
VALID_DINERS_CLUB_16 = '3050000000000009'
VALID_DINERS_CLUB_17 = '30500000000000009'
VALID_DINERS_CLUB_19 = '3050000000000000009'
LUHN_INVALID = '4000000000000000'
LEN_INVALID = '40000000000000006'


# Mock PaymentCardNumber
PCN = namedtuple('PaymentCardNumber', ['card_number', 'brand'])
PCN.__len__ = lambda v: len(v.card_number)


@pytest.fixture(scope='session', name='PaymentCard')
def payment_card_model_fixture():
    class PaymentCard(BaseModel):
        card_number: PaymentCardNumber

    return PaymentCard


def test_validate_digits():
    digits = '12345'
    assert PaymentCardNumber.validate_digits(digits) is None
    with pytest.raises(PydanticCustomError, match='Card number is not all digits'):
        PaymentCardNumber.validate_digits('hello')
    with pytest.raises(PydanticCustomError, match='Card number is not all digits'):
        PaymentCardNumber.validate_digits('²')


@pytest.mark.parametrize(
    'card_number, valid',
    [
        ('0', True),
        ('00', True),
        ('18', True),
        ('0000000000000000', True),
        ('4242424242424240', False),
        ('4242424242424241', False),
        ('4242424242424242', True),
        ('4242424242424243', False),
        ('4242424242424244', False),
        ('4242424242424245', False),
        ('4242424242424246', False),
        ('4242424242424247', False),
        ('4242424242424248', False),
        ('4242424242424249', False),
        ('42424242424242426', True),
        ('424242424242424267', True),
        ('4242424242424242675', True),
        ('5164581347216566', True),
        ('4345351087414150', True),
        ('343728738009846', True),
        ('5164581347216567', False),
        ('4345351087414151', False),
        ('343728738009847', False),
        ('000000018', True),
        ('99999999999999999999', True),
        ('99999999999999999999999999999999999999999999999999999999999999999997', True),
    ],
)
def test_validate_luhn_check_digit(card_number: str, valid: bool):
    if valid:
        assert PaymentCardNumber.validate_luhn_check_digit(card_number) == card_number
    else:
        with pytest.raises(PydanticCustomError, match='Card number is not luhn valid'):
            PaymentCardNumber.validate_luhn_check_digit(card_number)


@pytest.mark.parametrize(
    'card_number, brand, valid',
    [
        (VALID_VISA_13, PaymentCardBrand.visa, True),
        (VALID_VISA_16, PaymentCardBrand.visa, True),
        (VALID_VISA_19, PaymentCardBrand.visa, True),
        (VALID_MC, PaymentCardBrand.mastercard, True),
        (VALID_AMEX, PaymentCardBrand.amex, True),
        (VALID_MIR_16, PaymentCardBrand.mir, True),
        (VALID_MIR_17, PaymentCardBrand.mir, True),
        (VALID_MIR_18, PaymentCardBrand.mir, True),
        (VALID_MIR_19, PaymentCardBrand.mir, True),
        (VALID_DISCOVER, PaymentCardBrand.discover, True),
        (VALID_VERVE_16, PaymentCardBrand.verve, True),
        (VALID_VERVE_18, PaymentCardBrand.verve, True),
        (VALID_VERVE_19, PaymentCardBrand.verve, True),
        (VALID_DANKORT, PaymentCardBrand.dankort, True),
        (VALID_UNIONPAY_16, PaymentCardBrand.unionpay, True),
        (VALID_UNIONPAY_19, PaymentCardBrand.unionpay, True),
        (VALID_JCB_16, PaymentCardBrand.jcb, True),
        (VALID_JCB_19, PaymentCardBrand.jcb, True),
        (LEN_INVALID, PaymentCardBrand.visa, False),
        (VALID_MAESTRO, PaymentCardBrand.maestro, True),
        (VALID_TROY, PaymentCardBrand.troy, True),
        (VALID_DINERS_CLUB_14, PaymentCardBrand.diners_club, True),
        (VALID_DINERS_CLUB_16, PaymentCardBrand.diners_club, True),
        (VALID_DINERS_CLUB_19, PaymentCardBrand.diners_club, True),
        (VALID_OTHER, PaymentCardBrand.other, True),
    ],
)
def test_length_for_brand(card_number: str, brand: PaymentCardBrand, valid: bool):
    # pcn = PCN(card_number, brand)
    if valid:
        assert PaymentCardNumber.validate_brand(card_number) == brand
    else:
        with pytest.raises(PydanticCustomError) as exc_info:
            PaymentCardNumber.validate_brand(card_number)
        assert exc_info.value.type == 'payment_card_number_brand'


@pytest.mark.parametrize(
    'card_number, brand',
    [
        (VALID_AMEX, PaymentCardBrand.amex),
        (VALID_MC, PaymentCardBrand.mastercard),
        (VALID_VISA_16, PaymentCardBrand.visa),
        (VALID_MIR_16, PaymentCardBrand.mir),
        (VALID_DISCOVER, PaymentCardBrand.discover),
        (VALID_VERVE_16, PaymentCardBrand.verve),
        (VALID_DANKORT, PaymentCardBrand.dankort),
        (VALID_UNIONPAY_16, PaymentCardBrand.unionpay),
        (VALID_JCB_16, PaymentCardBrand.jcb),
        (VALID_OTHER, PaymentCardBrand.other),
        (VALID_MAESTRO, PaymentCardBrand.maestro),
        (VALID_DINERS_CLUB_14, PaymentCardBrand.diners_club),
        (VALID_DINERS_CLUB_16, PaymentCardBrand.diners_club),
        (VALID_DINERS_CLUB_17, PaymentCardBrand.diners_club),
        (VALID_DINERS_CLUB_19, PaymentCardBrand.diners_club),
        (VALID_TROY, PaymentCardBrand.troy),
    ],
)
def test_get_brand(card_number: str, brand: PaymentCardBrand):
    assert PaymentCardNumber.validate_brand(card_number) == brand


def test_valid(PaymentCard):
    card = PaymentCard(card_number=VALID_VISA_16)
    assert str(card.card_number) == VALID_VISA_16
    assert card.card_number.masked == '405000******0001'


@pytest.mark.parametrize(
    'card_number, error_message',
    [
        (None, 'type=string_type'),
        ('1' * 11, 'type=string_too_short,'),
        ('1' * 20, 'type=string_too_long,'),
        ('h' * 16, 'type=payment_card_number_digits'),
        (LUHN_INVALID, 'type=payment_card_number_luhn,'),
        (LEN_INVALID, 'type=payment_card_number_brand,'),
    ],
)
def test_error_types(card_number: Any, error_message: str, PaymentCard):
    with pytest.raises(ValidationError, match=error_message):
        PaymentCard(card_number=card_number)


def test_payment_card_brand():
    b = PaymentCardBrand.visa
    assert str(b) == 'Visa'
    assert b is PaymentCardBrand.visa
    assert b == PaymentCardBrand.visa
    assert b in {PaymentCardBrand.visa, PaymentCardBrand.mastercard}

    b = 'Visa'
    assert b is not PaymentCardBrand.visa
    assert b == PaymentCardBrand.visa
    assert b in {PaymentCardBrand.visa, PaymentCardBrand.mastercard}

    b = PaymentCardBrand.amex
    assert b is not PaymentCardBrand.visa
    assert b != PaymentCardBrand.visa
    assert b not in {PaymentCardBrand.visa, PaymentCardBrand.mastercard}
