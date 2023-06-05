"""
Country definitions that are based on the ISO 3166 format
Based on: https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes
"""
from dataclasses import dataclass
from functools import lru_cache
from typing import Dict, List, Optional, Type, TypeVar

import pycountry
from pydantic_core import PydanticCustomError, core_schema

from pydantic import GetCoreSchemaHandler

T = TypeVar('T')


@dataclass
class CountryInfo:
    alpha2: str
    alpha3: str
    numeric_code: str
    short_name: str
    # NOTICE: Not all countries have an official name
    official_name: Optional[str]


@lru_cache()
def _countries() -> List[CountryInfo]:
    return [
        CountryInfo(
            alpha2=country.alpha_2,
            alpha3=country.alpha_3,
            numeric_code=country.numeric,
            short_name=country.name,
            official_name=getattr(country, 'official_name', ''),
        )
        for country in pycountry.countries
    ]


@lru_cache()
def _index_by_alpha2() -> Dict[str, CountryInfo]:
    return {country.alpha2: country for country in _countries()}


@lru_cache()
def _index_by_alpha3() -> Dict[str, CountryInfo]:
    return {country.alpha3: country for country in _countries()}


@lru_cache()
def _index_by_numeric_code() -> Dict[str, CountryInfo]:
    return {country.numeric_code: country for country in _countries()}


@lru_cache()
def _index_by_short_name() -> Dict[str, CountryInfo]:
    return {country.short_name: country for country in _countries()}


@lru_cache()
def _index_by_official_name() -> Dict[str, CountryInfo]:
    return {country.official_name: country for country in _countries() if country.official_name is not None}


class CountryAlpha2(str):
    @classmethod
    def _validate(cls, __input_value: str, _: core_schema.ValidationInfo) -> 'CountryAlpha2':
        if __input_value not in _index_by_alpha2():
            raise PydanticCustomError('country_alpha2', 'Invalid country alpha2 code')
        return cls(__input_value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: Type[T], handler: GetCoreSchemaHandler
    ) -> core_schema.AfterValidatorFunctionSchema:
        return core_schema.general_after_validator_function(
            cls._validate,
            core_schema.str_schema(to_upper=True),
        )

    @property
    def alpha3(self) -> str:
        return _index_by_alpha2()[self].alpha3

    @property
    def numeric_code(self) -> str:
        return _index_by_alpha2()[self].numeric_code

    @property
    def short_name(self) -> str:
        return _index_by_alpha2()[self].short_name

    @property
    def official_name(self) -> str:
        country = _index_by_alpha2()[self]
        return country.official_name if country.official_name is not None else ''


class CountryAlpha3(str):
    @classmethod
    def _validate(cls, __input_value: str, _: core_schema.ValidationInfo) -> 'CountryAlpha3':
        if __input_value not in _index_by_alpha3():
            raise PydanticCustomError('country_alpha3', 'Invalid country alpha3 code')
        return cls(__input_value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: Type[T], handler: GetCoreSchemaHandler
    ) -> core_schema.AfterValidatorFunctionSchema:
        return core_schema.general_after_validator_function(
            cls._validate,
            core_schema.str_schema(to_upper=True),
            serialization=core_schema.to_string_ser_schema(),
        )

    @property
    def alpha2(self) -> str:
        return _index_by_alpha3()[self].alpha2

    @property
    def numeric_code(self) -> str:
        return _index_by_alpha3()[self].numeric_code

    @property
    def short_name(self) -> str:
        return _index_by_alpha3()[self].short_name

    @property
    def official_name(self) -> str:
        country = _index_by_alpha3()[self]
        return country.official_name if country.official_name is not None else ''


class CountryNumericCode(str):
    @classmethod
    def _validate(cls, __input_value: str, _: core_schema.ValidationInfo) -> 'CountryNumericCode':
        if __input_value not in _index_by_numeric_code():
            raise PydanticCustomError('country_numeric_code', 'Invalid country numeric code')
        return cls(__input_value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: Type[T], handler: GetCoreSchemaHandler
    ) -> core_schema.AfterValidatorFunctionSchema:
        return core_schema.general_after_validator_function(
            cls._validate,
            core_schema.str_schema(to_upper=True),
            serialization=core_schema.to_string_ser_schema(),
        )

    @property
    def alpha2(self) -> str:
        return _index_by_numeric_code()[self].alpha2

    @property
    def alpha3(self) -> str:
        return _index_by_numeric_code()[self].alpha3

    @property
    def short_name(self) -> str:
        return _index_by_numeric_code()[self].short_name

    @property
    def official_name(self) -> str:
        country = _index_by_numeric_code()[self]
        return country.official_name if country.official_name is not None else ''


class CountryShortName(str):
    @classmethod
    def _validate(cls, __input_value: str, _: core_schema.ValidationInfo) -> 'CountryShortName':
        if __input_value not in _index_by_short_name():
            raise PydanticCustomError('country_short_name', 'Invalid country short name')
        return cls(__input_value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: Type[T], handler: GetCoreSchemaHandler
    ) -> core_schema.AfterValidatorFunctionSchema:
        return core_schema.general_after_validator_function(
            cls._validate,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )

    @property
    def alpha2(self) -> str:
        return _index_by_short_name()[self].alpha2

    @property
    def alpha3(self) -> str:
        return _index_by_short_name()[self].alpha3

    @property
    def numeric_code(self) -> str:
        return _index_by_short_name()[self].numeric_code

    @property
    def official_name(self) -> str:
        country = _index_by_short_name()[self]
        return country.official_name if country.official_name is not None else ''


class CountryOfficialName(str):
    @classmethod
    def _validate(cls, __input_value: str, _: core_schema.ValidationInfo) -> 'CountryOfficialName':
        if __input_value not in _index_by_official_name():
            raise PydanticCustomError('country_numeric_code', 'Invalid country official name')
        return cls(__input_value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: Type[T], handler: GetCoreSchemaHandler
    ) -> core_schema.AfterValidatorFunctionSchema:
        return core_schema.general_after_validator_function(
            cls._validate,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )

    @property
    def alpha2(self) -> str:
        return _index_by_official_name()[self].alpha2

    @property
    def alpha3(self) -> str:
        return _index_by_official_name()[self].alpha3

    @property
    def numeric_code(self) -> str:
        return _index_by_official_name()[self].numeric_code

    @property
    def short_name(self) -> str:
        return _index_by_official_name()[self].short_name
