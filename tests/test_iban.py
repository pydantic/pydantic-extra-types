from string import printable

import pytest
from pydantic import BaseModel, ValidationError

from pydantic_extra_types.iban import Iban


@pytest.fixture(scope='module', name='IBANFixture')
def iban_fixture():
    class IBANFixture(BaseModel):
        made_in: Iban

    return IBANFixture


@pytest.mark.parametrize(
    'iban',
    [
        'DE89 3704 0044 0532 0130 00',
        'DE89370400440532013000',
        'DE89370400440532013000',
        'NL56ABNA2238591354',
        'GB64BARC20040149326928',
    ],
)
def test_iban_properties(iban, IBANFixture):
    iban_obj = IBANFixture(made_in=iban).made_in

    assert iban_obj.bank == iban_obj.iban.bank
    assert iban_obj.compact == iban_obj.iban.compact
    assert iban_obj.formatted == iban_obj.iban.formatted
    assert iban_obj.account_code == iban_obj.iban.account_code
    assert iban_obj.bank_code == iban_obj.iban.bank_code
    assert iban_obj.numeric == iban_obj.iban.numeric


@pytest.mark.parametrize(
    'iban',
    list(printable),
)
def test_invalid_iban(iban, IBANFixture):
    with pytest.raises(ValidationError, match='Invalid characters in IBAN'):
        IBANFixture(made_in=iban)
