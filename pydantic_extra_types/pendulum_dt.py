"""Native Pendulum DateTime object implementation. This is a copy of the Pendulum DateTime object, but with a Pydantic
CoreSchema implementation. This allows Pydantic to validate the DateTime object.
"""

from __future__ import annotations

try:
    from pendulum import Date as _Date
    from pendulum import DateTime as _DateTime
    from pendulum import Duration as _Duration
    from pendulum import Time as _Time
    from pendulum import parse
except ModuleNotFoundError as e:  # pragma: no cover
    raise RuntimeError(
        'The `pendulum_dt` module requires "pendulum" to be installed. You can install it with "pip install pendulum".'
    ) from e
from datetime import date, datetime, time, timedelta
from typing import Any

from pydantic import GetCoreSchemaHandler
from pydantic_core import PydanticCustomError, core_schema


class DateTimeSettings(type):
    def __new__(cls, name, bases, dct, **kwargs):  # type: ignore[no-untyped-def]
        dct['strict'] = kwargs.pop('strict', True)
        return super().__new__(cls, name, bases, dct)

    def __init__(cls, name, bases, dct, **kwargs):  # type: ignore[no-untyped-def]
        super().__init__(name, bases, dct)
        cls.strict = kwargs.get('strict', True)


class DateTime(_DateTime, metaclass=DateTimeSettings):
    """A `pendulum.DateTime` object. At runtime, this type decomposes into pendulum.DateTime automatically.
    This type exists because Pydantic throws a fit on unknown types.

    ```python
    from pydantic import BaseModel
    from pydantic_extra_types.pendulum_dt import DateTime


    class test_model(BaseModel):
        dt: DateTime


    print(test_model(dt='2021-01-01T00:00:00+00:00'))

    # > test_model(dt=DateTime(2021, 1, 1, 0, 0, 0, tzinfo=FixedTimezone(0, name="+00:00")))
    ```
    """

    __slots__: list[str] = []

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        """Return a Pydantic CoreSchema with the Datetime validation

        Args:
            source: The source type to be converted.
            handler: The handler to get the CoreSchema.

        Returns:
            A Pydantic CoreSchema with the Datetime validation.
        """
        return core_schema.no_info_wrap_validator_function(cls._validate, core_schema.datetime_schema())

    @classmethod
    def _validate(cls, value: Any, handler: core_schema.ValidatorFunctionWrapHandler) -> DateTime:
        """Validate the datetime object and return it.

        Args:
            value: The value to validate.
            handler: The handler to get the CoreSchema.

        Returns:
            The validated value or raises a PydanticCustomError.
        """
        # if we are passed an existing instance, pass it straight through.
        if isinstance(value, (_DateTime, datetime)):
            return DateTime.instance(value)
        try:
            # probably the best way to have feature parity with
            # https://docs.pydantic.dev/latest/api/standard_library_types/#datetimedatetime
            value = handler(value)
            return DateTime.instance(value)
        except ValueError:
            try:
                value = parse(value, strict=cls.strict)
                if isinstance(value, _DateTime):
                    return DateTime.instance(value)
                raise ValueError(f'value is not a valid datetime it is a {type(value)}')
            except ValueError:
                raise
            except Exception as exc:
                raise PydanticCustomError('value_error', 'value is not a valid datetime') from exc


class Time(_Time):
    """A `pendulum.Time` object. At runtime, this type decomposes into pendulum.Time automatically.
    This type exists because Pydantic throws a fit on unknown types.

    ```python
    from pydantic import BaseModel
    from pydantic_extra_types.pendulum_dt import Time


    class test_model(BaseModel):
        dt: Time


    print(test_model(dt='00:00:00'))

    # > test_model(dt=Time(0, 0, 0))
    ```
    """

    __slots__: list[str] = []

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        """Return a Pydantic CoreSchema with the Time validation

        Args:
            source: The source type to be converted.
            handler: The handler to get the CoreSchema.

        Returns:
            A Pydantic CoreSchema with the Time validation.
        """
        return core_schema.no_info_wrap_validator_function(cls._validate, core_schema.time_schema())

    @classmethod
    def _validate(cls, value: Any, handler: core_schema.ValidatorFunctionWrapHandler) -> Time:
        """Validate the Time object and return it.

        Args:
            value: The value to validate.
            handler: The handler to get the CoreSchema.

        Returns:
            The validated value or raises a PydanticCustomError.
        """
        # if we are passed an existing instance, pass it straight through.
        if isinstance(value, (_Time, time)):
            return Time.instance(value, tz=value.tzinfo)

        # otherwise, parse it.
        try:
            parsed = parse(value, exact=True)
            if isinstance(parsed, _DateTime):
                dt = DateTime.instance(parsed)
                return Time.instance(dt.time())
            if isinstance(parsed, _Time):
                return Time.instance(parsed)
            raise ValueError(f'value is not a valid time it is a {type(parsed)}')
        except Exception as exc:
            raise PydanticCustomError('value_error', 'value is not a valid time') from exc


class Date(_Date):
    """A `pendulum.Date` object. At runtime, this type decomposes into pendulum.Date automatically.
    This type exists because Pydantic throws a fit on unknown types.

    ```python
    from pydantic import BaseModel
    from pydantic_extra_types.pendulum_dt import Date


    class test_model(BaseModel):
        dt: Date


    print(test_model(dt='2021-01-01'))

    # > test_model(dt=Date(2021, 1, 1))
    ```
    """

    __slots__: list[str] = []

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        """Return a Pydantic CoreSchema with the Date validation

        Args:
            source: The source type to be converted.
            handler: The handler to get the CoreSchema.

        Returns:
            A Pydantic CoreSchema with the Date validation.
        """
        return core_schema.no_info_wrap_validator_function(cls._validate, core_schema.date_schema())

    @classmethod
    def _validate(cls, value: Any, handler: core_schema.ValidatorFunctionWrapHandler) -> Date:
        """Validate the date object and return it.

        Args:
            value: The value to validate.
            handler: The handler to get the CoreSchema.

        Returns:
            The validated value or raises a PydanticCustomError.
        """
        # if we are passed an existing instance, pass it straight through.
        if isinstance(value, (_Date, date)):
            return Date(value.year, value.month, value.day)

        # otherwise, parse it.
        try:
            parsed = parse(value)
            if isinstance(parsed, (_DateTime, _Date)):
                return Date(parsed.year, parsed.month, parsed.day)
            raise ValueError(f'value is not a valid date it is a {type(parsed)}')
        except Exception as exc:
            raise PydanticCustomError('value_error', 'value is not a valid date') from exc


class Duration(_Duration):
    """A `pendulum.Duration` object. At runtime, this type decomposes into pendulum.Duration automatically.
    This type exists because Pydantic throws a fit on unknown types.

    ```python
    from pydantic import BaseModel
    from pydantic_extra_types.pendulum_dt import Duration


    class test_model(BaseModel):
        delta_t: Duration


    print(test_model(delta_t='P1DT25H'))

    # > test_model(delta_t=Duration(days=2, hours=1))
    ```
    """

    __slots__: list[str] = []

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        """Return a Pydantic CoreSchema with the Duration validation

        Args:
            source: The source type to be converted.
            handler: The handler to get the CoreSchema.

        Returns:
            A Pydantic CoreSchema with the Duration validation.
        """
        return core_schema.no_info_wrap_validator_function(
            cls._validate,
            core_schema.timedelta_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: instance.to_iso8601_string(), when_used='json-unless-none'
            ),
        )

    def to_iso8601_string(self) -> str:
        """
        Convert a Duration object to an ISO 8601 string.

        In addition to the standard ISO 8601 format, this method also supports the representation of fractions of a second and negative durations.

        Returns:
            The ISO 8601 string representation of the duration.
        """
        # Extracting components from the Duration object
        years = self.years
        months = self.months
        days = self._days
        hours = self.hours
        minutes = self.minutes
        seconds = self.remaining_seconds
        milliseconds = self.microseconds // 1000
        microseconds = self.microseconds % 1000

        # Constructing the ISO 8601 duration string
        iso_duration = 'P'
        if years or months or days:
            if years:
                iso_duration += f'{years}Y'
            if months:
                iso_duration += f'{months}M'
            if days:
                iso_duration += f'{days}D'

        if hours or minutes or seconds or milliseconds or microseconds:
            iso_duration += 'T'
            if hours:
                iso_duration += f'{hours}H'
            if minutes:
                iso_duration += f'{minutes}M'
            if seconds or milliseconds or microseconds:
                iso_duration += f'{seconds}'
                if milliseconds or microseconds:
                    iso_duration += f'.{milliseconds:03d}'
                if microseconds:
                    iso_duration += f'{microseconds:03d}'
                iso_duration += 'S'

        # Prefix with '-' if the duration is negative
        if self.total_seconds() < 0:
            iso_duration = '-' + iso_duration

        if iso_duration == 'P':
            iso_duration = 'P0D'

        return iso_duration

    @classmethod
    def _validate(cls, value: Any, handler: core_schema.ValidatorFunctionWrapHandler) -> Duration:
        """Validate the Duration object and return it.

        Args:
            value: The value to validate.
            handler: The handler to get the CoreSchema.

        Returns:
            The validated value or raises a PydanticCustomError.
        """

        if isinstance(value, _Duration):
            return Duration(
                years=value.years,
                months=value.months,
                weeks=value.weeks,
                days=value.remaining_days,
                hours=value.hours,
                minutes=value.minutes,
                seconds=value.remaining_seconds,
                microseconds=value.microseconds,
            )

        if isinstance(value, timedelta):
            return Duration(
                days=value.days,
                seconds=value.seconds,
                microseconds=value.microseconds,
            )

        assert isinstance(value, str)
        try:
            # https://github.com/python-pendulum/pendulum/issues/532
            if value.startswith('-'):
                parsed = parse(value.lstrip('-'), exact=True)
            else:
                parsed = parse(value, exact=True)
            if not isinstance(parsed, _Duration):
                raise ValueError(f'value is not a valid duration it is a {type(parsed)}')
            if value.startswith('-'):
                parsed = -parsed

            return Duration(
                years=parsed.years,
                months=parsed.months,
                weeks=parsed.weeks,
                days=parsed.remaining_days,
                hours=parsed.hours,
                minutes=parsed.minutes,
                seconds=parsed.remaining_seconds,
                microseconds=parsed.microseconds,
            )
        except Exception as exc:
            raise PydanticCustomError('value_error', 'value is not a valid duration') from exc
