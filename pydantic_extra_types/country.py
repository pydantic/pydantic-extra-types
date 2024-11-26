"""Country definitions that are based on the [ISO 3166](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes)."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Any

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import PydanticCustomError, core_schema

try:
    import pycountry
except ModuleNotFoundError as e:  # pragma: no cover
    raise RuntimeError(
        'The `country` module requires "pycountry" to be installed. You can install it with "pip install pycountry".'
    ) from e


@dataclass
class CountryInfo:
    alpha2: str
    alpha3: str
    numeric_code: str
    short_name: str


@lru_cache
def _countries() -> list[CountryInfo]:
    return [
        CountryInfo(
            alpha2=country.alpha_2,
            alpha3=country.alpha_3,
            numeric_code=country.numeric,
            short_name=country.name,
        )
        for country in pycountry.countries
    ]


@lru_cache
def _index_by_alpha2() -> dict[str, CountryInfo]:
    return {country.alpha2: country for country in _countries()}


@lru_cache
def _index_by_alpha3() -> dict[str, CountryInfo]:
    return {country.alpha3: country for country in _countries()}


@lru_cache
def _index_by_numeric_code() -> dict[str, CountryInfo]:
    return {country.numeric_code: country for country in _countries()}


@lru_cache
def _index_by_short_name() -> dict[str, CountryInfo]:
    return {country.short_name: country for country in _countries()}


class CountryAlpha2(str):
    """CountryAlpha2 parses country codes in the [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)
    format.

    ```py
    from pydantic import BaseModel

    from pydantic_extra_types.country import CountryAlpha2


    class Product(BaseModel):
        made_in: CountryAlpha2


    product = Product(made_in='ES')
    print(product)
    # > made_in='ES'
    ```
    """

    @classmethod
    def _validate(cls, __input_value: str, _: core_schema.ValidationInfo) -> CountryAlpha2:
        if __input_value not in _index_by_alpha2():
            raise PydanticCustomError('country_alpha2', 'Invalid country alpha2 code')
        return cls(__input_value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.AfterValidatorFunctionSchema:
        return core_schema.with_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(to_upper=True),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> dict[str, Any]:
        json_schema = handler(schema)
        json_schema.update({'pattern': r'^\w{2}$'})
        return json_schema

    @property
    def alpha3(self) -> str:
        """The country code in the [ISO 3166-1 alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) format."""
        return _index_by_alpha2()[self].alpha3

    @property
    def numeric_code(self) -> str:
        """The country code in the [ISO 3166-1 numeric](https://en.wikipedia.org/wiki/ISO_3166-1_numeric) format."""
        return _index_by_alpha2()[self].numeric_code

    @property
    def short_name(self) -> str:
        """The country short name."""
        return _index_by_alpha2()[self].short_name


class CountryAlpha3(str):
    """CountryAlpha3 parses country codes in the [ISO 3166-1 alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3)
    format.

    ```py
    from pydantic import BaseModel

    from pydantic_extra_types.country import CountryAlpha3


    class Product(BaseModel):
        made_in: CountryAlpha3


    product = Product(made_in='USA')
    print(product)
    # > made_in='USA'
    ```
    """

    @classmethod
    def _validate(cls, __input_value: str, _: core_schema.ValidationInfo) -> CountryAlpha3:
        if __input_value not in _index_by_alpha3():
            raise PydanticCustomError('country_alpha3', 'Invalid country alpha3 code')
        return cls(__input_value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.AfterValidatorFunctionSchema:
        return core_schema.with_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(to_upper=True),
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> dict[str, Any]:
        json_schema = handler(schema)
        json_schema.update({'pattern': r'^\w{3}$'})
        return json_schema

    @property
    def alpha2(self) -> str:
        """The country code in the [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) format."""
        return _index_by_alpha3()[self].alpha2

    @property
    def numeric_code(self) -> str:
        """The country code in the [ISO 3166-1 numeric](https://en.wikipedia.org/wiki/ISO_3166-1_numeric) format."""
        return _index_by_alpha3()[self].numeric_code

    @property
    def short_name(self) -> str:
        """The country short name."""
        return _index_by_alpha3()[self].short_name


class CountryNumericCode(str):
    """CountryNumericCode parses country codes in the
    [ISO 3166-1 numeric](https://en.wikipedia.org/wiki/ISO_3166-1_numeric) format.

    ```py
    from pydantic import BaseModel

    from pydantic_extra_types.country import CountryNumericCode


    class Product(BaseModel):
        made_in: CountryNumericCode


    product = Product(made_in='840')
    print(product)
    # > made_in='840'
    ```
    """

    @classmethod
    def _validate(cls, __input_value: str, _: core_schema.ValidationInfo) -> CountryNumericCode:
        if __input_value not in _index_by_numeric_code():
            raise PydanticCustomError('country_numeric_code', 'Invalid country numeric code')
        return cls(__input_value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.AfterValidatorFunctionSchema:
        return core_schema.with_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(to_upper=True),
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> dict[str, Any]:
        json_schema = handler(schema)
        json_schema.update({'pattern': r'^[0-9]{3}$'})
        return json_schema

    @property
    def alpha2(self) -> str:
        """The country code in the [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) format."""
        return _index_by_numeric_code()[self].alpha2

    @property
    def alpha3(self) -> str:
        """The country code in the [ISO 3166-1 alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) format."""
        return _index_by_numeric_code()[self].alpha3

    @property
    def short_name(self) -> str:
        """The country short name."""
        return _index_by_numeric_code()[self].short_name


class CountryShortName(str):
    """CountryShortName parses country codes in the short name format.

    ```py
    from pydantic import BaseModel

    from pydantic_extra_types.country import CountryShortName


    class Product(BaseModel):
        made_in: CountryShortName


    product = Product(made_in='United States')
    print(product)
    # > made_in='United States'
    ```
    """

    @classmethod
    def _validate(cls, __input_value: str, _: core_schema.ValidationInfo) -> CountryShortName:
        if __input_value not in _index_by_short_name():
            raise PydanticCustomError('country_short_name', 'Invalid country short name')
        return cls(__input_value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.AfterValidatorFunctionSchema:
        return core_schema.with_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )

    @property
    def alpha2(self) -> str:
        """The country code in the [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) format."""
        return _index_by_short_name()[self].alpha2

    @property
    def alpha3(self) -> str:
        """The country code in the [ISO 3166-1 alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) format."""
        return _index_by_short_name()[self].alpha3

    @property
    def numeric_code(self) -> str:
        """The country code in the [ISO 3166-1 numeric](https://en.wikipedia.org/wiki/ISO_3166-1_numeric) format."""
        return _index_by_short_name()[self].numeric_code
