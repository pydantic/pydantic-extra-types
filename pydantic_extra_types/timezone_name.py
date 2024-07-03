"""Time zone name validation and serialization module."""

from __future__ import annotations

import importlib
import sys
import warnings
from typing import Any, Callable, List, Set, Type, cast

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import PydanticCustomError, core_schema


def _is_available(name: str) -> bool:
    """Check if a module is available for import."""
    try:
        importlib.import_module(name)
        return True
    except ModuleNotFoundError:  # pragma: no cover
        return False


def _tz_provider_from_zone_info() -> Set[str]:  # pragma: no cover
    """Get timezones from the zoneinfo module."""
    from zoneinfo import available_timezones

    return set(available_timezones())


def _tz_provider_from_pytz() -> Set[str]:  # pragma: no cover
    """Get timezones from the pytz module."""
    from pytz import all_timezones

    return set(all_timezones)


def _warn_about_pytz_usage() -> None:
    """Warn about using pytz with Python 3.9 or later."""
    warnings.warn(  # pragma: no cover
        'Projects using Python 3.9 or later should be using the support now included as part of the standard library. '
        'Please consider switching to the standard library (zoneinfo) module.'
    )


def get_timezones() -> Set[str]:
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
    def __new__(cls, name: str, bases: tuple[type, ...], dct: dict[str, Any], **kwargs: Any) -> Type[TimeZoneName]:
        dct['strict'] = kwargs.pop('strict', True)
        return cast(Type[TimeZoneName], super().__new__(cls, name, bases, dct))

    def __init__(cls, name: str, bases: tuple[type, ...], dct: dict[str, Any], **kwargs: Any) -> None:
        super().__init__(name, bases, dct)
        cls.strict = kwargs.get('strict', True)


def timezone_name_settings(**kwargs: Any) -> Callable[[Type[TimeZoneName]], Type[TimeZoneName]]:
    def wrapper(cls: Type[TimeZoneName]) -> Type[TimeZoneName]:
        cls.strict = kwargs.get('strict', True)
        return cls

    return wrapper


@timezone_name_settings(strict=True)
class TimeZoneName(str):
    """
    TimeZoneName is a custom string subclass for validating and serializing timezone names.

    The TimeZoneName class uses the IANA Time Zone Database for validation.
    It supports both strict and non-strict modes for timezone name validation.


    ## Examples:

    Some examples of using the TimeZoneName class:

    ### Normal usage:

    ```python
    from pydantic_extra_types.timezone_name import TimeZoneName
    from pydantic import BaseModel
    class Location(BaseModel):
        city: str
        timezone: TimeZoneName

    loc = Location(city="New York", timezone="America/New_York")
    print(loc.timezone)

    >> America/New_York

    ```

    ### Non-strict mode:

    ```python

    from pydantic_extra_types.timezone_name import TimeZoneName, timezone_name_settings

    @timezone_name_settings(strict=False)
    class TZNonStrict(TimeZoneName):
        pass

    tz = TZNonStrict("america/new_york")

    print(tz)

    >> america/new_york

    ```
    """

    __slots__: List[str] = []
    allowed_values: Set[str] = set(get_timezones())
    allowed_values_list: List[str] = sorted(allowed_values)
    allowed_values_upper_to_correct: dict[str, str] = {val.upper(): val for val in allowed_values}
    strict: bool

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
        cls, _: Type[Any], __: GetCoreSchemaHandler
    ) -> core_schema.AfterValidatorFunctionSchema:
        """
        Return a Pydantic CoreSchema with the timezone name validation.

        Args:
            _: The source type.
            __: The handler to get the CoreSchema.

        Returns:
            A Pydantic CoreSchema with the timezone name validation.
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
        Return a Pydantic JSON Schema with the timezone name validation.

        Args:
            schema: The Pydantic CoreSchema.
            handler: The handler to get the JSON Schema.

        Returns:
            A Pydantic JSON Schema with the timezone name validation.
        """
        json_schema = handler(schema)
        json_schema.update({'enum': cls.allowed_values_list})
        return json_schema
