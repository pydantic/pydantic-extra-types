from string import printable

import pytest

from pydantic import BaseModel, ValidationError
from pydantic_extra_types import CurrencyCode, CurrencyDisplayName, CurrencyNumericCode
from pydantic_extra_types.types.money import Currency, _index_by_code, _index_by_display_name, _index_by_numeric_code

PARAMS_AMOUNT = 10


def random_int():
    import random

    return random.randint(0, 7)


@pytest.fixture(scope='module', name='CurrencyCode')
def currency_code_fixture():
    class Product(BaseModel):
        price: CurrencyCode

    return Product


@pytest.mark.parametrize('code, currency_data', list(_index_by_code().items())[:PARAMS_AMOUNT])
def test_valid_currency_code(code: str, currency_data: Currency, CurrencyCode):
    banana = CurrencyCode(price=code)
    assert banana.price == currency_data.code
    assert banana.price.display_name == currency_data.display_name
    assert banana.price.numeric_code == currency_data.numeric_code
    assert banana.price.default_fraction_digits == currency_data.default_fraction_digits
    assert banana.price.sub_unit == currency_data.sub_unit


@pytest.mark.parametrize('code', list(printable))
def test_invalid_currency_code(code: str, CurrencyCode):
    with pytest.raises(ValidationError, match='invalid currency code'):
        CurrencyCode(price=code)


@pytest.fixture(scope='module', name='CurrencyDisplayName')
def currency_display_name_fixture():
    class Product(BaseModel):
        price: CurrencyDisplayName

    return Product


@pytest.mark.parametrize('currency_display_name, currency_data', list(_index_by_display_name().items())[:PARAMS_AMOUNT])
def test_valid_currency_display_name(currency_display_name: str, currency_data: Currency, CurrencyDisplayName):
    banana = CurrencyDisplayName(price=currency_display_name)
    assert banana.price == currency_data.display_name
    assert banana.price.code == currency_data.code
    assert banana.price.numeric_code == currency_data.numeric_code
    assert banana.price.default_fraction_digits == currency_data.default_fraction_digits
    assert banana.price.sub_unit == currency_data.sub_unit


@pytest.mark.parametrize('display_name', list(printable))
def test_invalid_currency_display_name(display_name: str, CurrencyDisplayName):
    with pytest.raises(ValidationError, match='invalid currency display name'):
        CurrencyDisplayName(price=display_name)


@pytest.fixture(scope='module', name='CurrencyNumericCode')
def currency_numeric_code_fixture():
    class Product(BaseModel):
        price: CurrencyNumericCode

    return Product


@pytest.mark.parametrize('currency_numeric_code, currency_data', list(_index_by_numeric_code().items())[:PARAMS_AMOUNT])
def test_valid_currency_numeric_code(currency_numeric_code: int, currency_data: Currency, CurrencyNumericCode):
    banana = CurrencyNumericCode(price=currency_numeric_code)
    assert banana.price == currency_data.numeric_code
    assert banana.price.code == currency_data.code
    assert banana.price.display_name == currency_data.display_name
    assert banana.price.default_fraction_digits == currency_data.default_fraction_digits
    assert banana.price.sub_unit == currency_data.sub_unit


@pytest.mark.parametrize('numeric_code', [random_int() for _ in range(7)])
def test_invalid_currency_numeric_code(numeric_code: int, CurrencyNumericCode):
    with pytest.raises(ValidationError, match='invalid currency numeric code'):
        CurrencyNumericCode(price=numeric_code)
