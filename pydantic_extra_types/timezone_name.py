"""Time zone name validation and serialization module."""

from __future__ import annotations

import importlib
import sys
import warnings
from typing import Any, List

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import PydanticCustomError, core_schema


def _is_available(name: str) -> bool:
    """Check if a module is available for import."""
    try:
        importlib.import_module(name)
        return True
    except ModuleNotFoundError:  # pragma: no cover
        return False


def _tz_provider_from_zone_info() -> set[str]:  # pragma: no cover
    """Get timezones from the zoneinfo module."""
    from zoneinfo import available_timezones

    return set(available_timezones())


def _tz_provider_from_pytz() -> set[str]:  # pragma: no cover
    """Get timezones from the pytz module."""
    from pytz import all_timezones

    return set(all_timezones)


def _warn_about_pytz_usage() -> None:
    """Warn about using pytz with Python 3.9 or later."""
    warnings.warn(  # pragma: no cover
        'Projects using Python 3.9 or later should be using the support now included as part of the standard library'
        'Please consider switching to the standard library (zone-info) module.'
    )


def get_timezones() -> set[str]:
    """Determine the timezone provider and return available timezones."""
    if _is_available('zoneinfo') and _is_available('tzdata'):  # pragma: no cover
        return _tz_provider_from_zone_info()
    elif _is_available('pytz'):  # pragma: no cover
        if sys.version_info[:2] > (3, 8):
            _warn_about_pytz_usage()
        return _tz_provider_from_pytz()
    else:  # pragma: no cover
        if sys.version_info[:2] == (3, 8):
            raise ImportError('No pytz module found. Please install it with "pip install pytz"')
        raise ImportError('No timezone provider found. Please install tzdata with "pip install tzdata"')


class TimeZoneNameSettings(type):
    def __new__(cls, name, bases, dct, **kwargs):  # type: ignore[no-untyped-def]
        dct['strict'] = kwargs.pop('strict', True)
        return super().__new__(cls, name, bases, dct)

    def __init__(cls, name, bases, dct, **kwargs):  # type: ignore[no-untyped-def]
        super().__init__(name, bases, dct)
        cls.strict = kwargs.get('strict', True)


class TimeZoneName(str, metaclass=TimeZoneNameSettings):  # type: ignore[misc]
    """If the mode is not strict matching, it is case-insensitive with whitespace stripped.
    Value is then coerced to the correct case."""

    __slots__: List[str] = []
    allowed_values = set(get_timezones())
    allowed_values_list = list(allowed_values)
    allowed_values_list.sort()
    allowed_values_upper_to_correct = {val.upper(): val for val in allowed_values}

    @classmethod
    def _validate(cls, __input_value: str, _: core_schema.ValidationInfo) -> TimeZoneName:
        """
        Validate a time zone name from the provided str value.

        Args:
            __input_value: The str value to be validated.
            _: The Pydantic ValidationInfo.

        Returns:
            The validated time zone name.

        Raises:
            PydanticCustomError: If the timezone name is not valid.
        """
        if __input_value not in cls.allowed_values:  # be fast for the most common case
            if not cls.strict:
                upper_value = __input_value.strip().upper()
                if upper_value in cls.allowed_values_upper_to_correct:
                    return cls(cls.allowed_values_upper_to_correct[upper_value])
            raise PydanticCustomError('TimeZoneName', 'Invalid timezone name.')
        return cls(__input_value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, _: type[Any], __: GetCoreSchemaHandler
    ) -> core_schema.AfterValidatorFunctionSchema:
        """
        Return a Pydantic CoreSchema with the ISO 639-3 language code validation.

        Args:
            _: The source type.
            __: The handler to get the CoreSchema.

        Returns:
            A Pydantic CoreSchema with the ISO 639-3 language code validation.

        """
        return core_schema.with_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(min_length=1),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> dict[str, Any]:
        """
        Return a Pydantic JSON Schema with the ISO 639-3 language code validation.

        Args:
            schema: The Pydantic CoreSchema.
            handler: The handler to get the JSON Schema.

        Returns:
            A Pydantic JSON Schema with the ISO 639-3 language code validation.

        """
        json_schema = handler(schema)
        json_schema.update({'enum': cls.allowed_values_list})
        return json_schema
