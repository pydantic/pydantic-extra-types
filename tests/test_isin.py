from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

from pydantic_extra_types.isin import ISIN


class Security(BaseModel):
    isin: ISIN


valid_isin_test_cases = [
    ('US0378331005', 'US0378331005'),
    ('US5949181045', 'US5949181045'),
    ('GB0002634946', 'GB0002634946'),
    ('AU0000XVGZA3', 'AU0000XVGZA3'),
    ('us0378331005', 'US0378331005'),
]


@pytest.mark.parametrize('input_isin, output_isin', valid_isin_test_cases)
def test_valid_isin(input_isin: str, output_isin: str) -> None:
    assert Security(isin=ISIN(input_isin)).isin == output_isin


isin_length_test_cases = [
    ('US037833100', False),
    ('US03783310055', False),
    ('', False),
]


@pytest.mark.parametrize('input_isin, valid', isin_length_test_cases)
def test_isin_length(input_isin: str, valid: bool) -> None:
    if valid:
        Security(isin=ISIN(input_isin))
    else:
        with pytest.raises(ValidationError, match='isin_length'):
            Security(isin=ISIN(input_isin))


@pytest.mark.parametrize('input_isin', ['U10378331005', 'US037833100A'])
def test_isin_country_and_check_digit_format(input_isin: str) -> None:
    with pytest.raises(ValidationError, match='isin_invalid'):
        Security(isin=ISIN(input_isin))


@pytest.mark.parametrize('input_isin', ['US037833100$', 'US03 8331005'])
def test_isin_invalid_characters(input_isin: str) -> None:
    with pytest.raises(ValidationError, match='isin_invalid_characters'):
        Security(isin=ISIN(input_isin))


@pytest.mark.parametrize('input_isin', ['US0378331004', 'GB0002634947'])
def test_isin_invalid_check_digit(input_isin: str) -> None:
    with pytest.raises(ValidationError, match='isin_invalid_check_digit'):
        Security(isin=ISIN(input_isin))


@pytest.mark.parametrize('isin_value', [None, 123456789012, object()])
def test_isin_requires_string(isin_value: Any) -> None:
    with pytest.raises(ValidationError, match='Input should be a valid string'):
        Security(isin=isin_value)
