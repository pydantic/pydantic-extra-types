from string import printable

import pytest
from pydantic import BaseModel, ValidationError

from pydantic_extra_types.country import (
    CountryAlpha2,
    CountryAlpha3,
    CountryInfo,
    CountryNumericCode,
    CountryOfficialName,
    CountryShortName,
    _index_by_alpha2,
    _index_by_alpha3,
    _index_by_numeric_code,
    _index_by_official_name,
    _index_by_short_name,
)

PARAMS_AMOUNT = 20


@pytest.fixture(scope='module', name='ProductAlpha2')
def product_alpha2_fixture():
    class Product(BaseModel):
        made_in: CountryAlpha2

    return Product


@pytest.fixture(scope='module', name='ProductAlpha3')
def product_alpha3_fixture():
    class Product(BaseModel):
        made_in: CountryAlpha3

    return Product


@pytest.fixture(scope='module', name='ProductShortName')
def product_short_name_fixture():
    class Product(BaseModel):
        made_in: CountryShortName

    return Product


@pytest.fixture(scope='module', name='ProductNumericCode')
def product_numeric_code_fixture():
    class Product(BaseModel):
        made_in: CountryNumericCode

    return Product


@pytest.fixture(scope='module', name='ProductOfficialName')
def product_official_name_fixture():
    class Product(BaseModel):
        made_in: CountryOfficialName

    return Product


@pytest.mark.parametrize(
    'alpha2, country_data',
    [(alpha2, country_data) for alpha2, country_data in _index_by_alpha2().items()][:PARAMS_AMOUNT],
)
def test_valid_alpha2(alpha2: str, country_data: CountryInfo, ProductAlpha2):
    banana = ProductAlpha2(made_in=alpha2)
    assert banana.made_in == country_data.alpha2
    assert banana.made_in.alpha3 == country_data.alpha3
    assert banana.made_in.numeric_code == country_data.numeric_code
    assert banana.made_in.short_name == country_data.short_name
    assert banana.made_in.official_name == country_data.official_name


@pytest.mark.parametrize('alpha2', list(printable))
def test_invalid_alpha2(alpha2: str, ProductAlpha2):
    with pytest.raises(ValidationError, match='Invalid country alpha2 code'):
        ProductAlpha2(made_in=alpha2)


@pytest.mark.parametrize(
    'alpha3, country_data',
    [(alpha3, country_data) for alpha3, country_data in _index_by_alpha3().items()][:PARAMS_AMOUNT],
)
def test_valid_alpha3(alpha3: str, country_data: CountryInfo, ProductAlpha3):
    banana = ProductAlpha3(made_in=alpha3)
    assert banana.made_in == country_data.alpha3
    assert banana.made_in.alpha2 == country_data.alpha2
    assert banana.made_in.numeric_code == country_data.numeric_code
    assert banana.made_in.short_name == country_data.short_name
    assert banana.made_in.official_name == country_data.official_name


@pytest.mark.parametrize('alpha3', list(printable))
def test_invalid_alpha3(alpha3: str, ProductAlpha3):
    with pytest.raises(ValidationError, match='Invalid country alpha3 code'):
        ProductAlpha3(made_in=alpha3)


@pytest.mark.parametrize(
    'short_name, country_data',
    [(short_name, country_data) for short_name, country_data in _index_by_short_name().items()][:PARAMS_AMOUNT],
)
def test_valid_short_name(short_name: str, country_data: CountryInfo, ProductShortName):
    banana = ProductShortName(made_in=short_name)
    assert banana.made_in == country_data.short_name
    assert banana.made_in.alpha2 == country_data.alpha2
    assert banana.made_in.alpha3 == country_data.alpha3
    assert banana.made_in.numeric_code == country_data.numeric_code
    assert banana.made_in.official_name == country_data.official_name


@pytest.mark.parametrize('short_name', list(printable))
def test_invalid_short_name(short_name: str, ProductShortName):
    with pytest.raises(ValidationError, match='Invalid country short name'):
        ProductShortName(made_in=short_name)


@pytest.mark.parametrize(
    'official_name, country_data',
    [(official_name, country_data) for official_name, country_data in _index_by_official_name().items()][
        :PARAMS_AMOUNT
    ],
)
def test_valid_official_name(official_name: str, country_data: CountryInfo, ProductOfficialName):
    banana = ProductOfficialName(made_in=official_name)
    assert banana.made_in == country_data.official_name
    assert banana.made_in.alpha2 == country_data.alpha2
    assert banana.made_in.alpha3 == country_data.alpha3
    assert banana.made_in.short_name == country_data.short_name
    assert banana.made_in.numeric_code == country_data.numeric_code


@pytest.mark.parametrize('official_name', list(printable))
def test_invalid_official_name(official_name: str, ProductOfficialName):
    with pytest.raises(ValidationError, match='Invalid country official name'):
        ProductOfficialName(made_in=official_name)


@pytest.mark.parametrize(
    'numeric_code, country_data',
    [(numeric_code, country_data) for numeric_code, country_data in _index_by_numeric_code().items()][:PARAMS_AMOUNT],
)
def test_valid_numeric_code(numeric_code: str, country_data: CountryInfo, ProductNumericCode):
    banana = ProductNumericCode(made_in=numeric_code)
    assert banana.made_in == country_data.numeric_code
    assert banana.made_in.alpha2 == country_data.alpha2
    assert banana.made_in.alpha3 == country_data.alpha3
    assert banana.made_in.short_name == country_data.short_name
    assert banana.made_in.official_name == country_data.official_name


@pytest.mark.parametrize('numeric_code', list(printable))
def test_invalid_numeric_code(numeric_code: str, ProductNumericCode):
    with pytest.raises(ValidationError, match='Invalid country numeric code'):
        ProductNumericCode(made_in=numeric_code)
