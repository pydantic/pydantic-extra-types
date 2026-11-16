import pytest
from pydantic import TypeAdapter, ValidationError

from pydantic_extra_types.country import CountryAlpha2, CountryAlpha3
from pydantic_extra_types.currency_code import ISO4217, Currency
from pydantic_extra_types.language_code import LanguageAlpha2
from pydantic_extra_types.script_code import ISO_15924


@pytest.mark.parametrize(
    'code_type,value',
    [
        (CountryAlpha2, 'U\u017f'),
        (CountryAlpha3, 'U\u017fA'),
        (CountryAlpha3, '\u00dfD'),
        (ISO4217, 'U\u017fD'),
        (Currency, 'U\u017fD'),
        (LanguageAlpha2, '\u212ao'),
        (ISO_15924, 'Ma\u212aa'),
    ],
)
def test_non_ascii_code_is_rejected(code_type: type[str], value: str) -> None:
    with pytest.raises(ValidationError):
        TypeAdapter(code_type).validate_python(value)
    with pytest.raises(ValidationError):
        TypeAdapter(code_type).validate_json(f'"{value}"')


@pytest.mark.parametrize(
    'code_type,value,expected',
    [
        (CountryAlpha2, ' us ', 'US'),
        (CountryAlpha3, ' usa ', 'USA'),
        (ISO4217, ' usd ', 'USD'),
        (Currency, ' usd ', 'USD'),
        (LanguageAlpha2, ' KO ', 'ko'),
        (ISO_15924, ' MAKA ', 'Maka'),
    ],
)
def test_ascii_case_normalization(code_type: type[str], value: str, expected: str) -> None:
    assert TypeAdapter(code_type).validate_python(value) == expected
