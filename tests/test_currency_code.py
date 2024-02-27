import re

import pycountry
import pytest
from pydantic import BaseModel, ValidationError

from pydantic_extra_types import currency_code


class ISO4217CheckingModel(BaseModel):
    currency: currency_code.ISO4217


class CurrencyCheckingModel(BaseModel):
    currency: currency_code.Currency


forbidden_currencies = sorted(currency_code._CODES_FOR_BONDS_METAL_TESTING)


@pytest.mark.parametrize('currency', map(lambda code: code.alpha_3, pycountry.currencies))
def test_ISO4217_code_ok(currency: str):
    model = ISO4217CheckingModel(currency=currency)
    assert model.currency == currency
    assert model.model_dump() == {'currency': currency}  # test serialization


@pytest.mark.parametrize(
    'currency',
    filter(
        lambda code: code not in currency_code._CODES_FOR_BONDS_METAL_TESTING,
        map(lambda code: code.alpha_3, pycountry.currencies),
    ),
)
def test_everyday_code_ok(currency: str):
    model = CurrencyCheckingModel(currency=currency)
    assert model.currency == currency
    assert model.model_dump() == {'currency': currency}  # test serialization


def test_ISO4217_fails():
    with pytest.raises(
        ValidationError,
        match=re.escape(
            '1 validation error for ISO4217CheckingModel\ncurrency\n  '
            'Invalid ISO 4217 currency code. See https://en.wikipedia.org/wiki/ISO_4217 '
            "[type=ISO4217, input_value='OMG', input_type=str]"
        ),
    ):
        ISO4217CheckingModel(currency='OMG')


@pytest.mark.parametrize('forbidden_currency', forbidden_currencies)
def test_forbidden_everyday(forbidden_currency):
    with pytest.raises(
        ValidationError,
        match=re.escape(
            '1 validation error for CurrencyCheckingModel\ncurrency\n  '
            'Invalid currency code. See https://en.wikipedia.org/wiki/ISO_4217. '
            'Bonds, testing and precious metals codes are not allowed. '
            f"[type=InvalidCurrency, input_value='{forbidden_currency}', input_type=str]"
        ),
    ):
        CurrencyCheckingModel(currency=forbidden_currency)
