"""Native Whenever object implementations. This module provides a Pydantic
CoreSchema implementation for whenever objects, thus allowing Pydantic to validate them.
"""

from datetime import datetime, timedelta
from typing import Any

from pydantic import GetCoreSchemaHandler
from pydantic_core import PydanticCustomError, core_schema

try:
    from whenever import (
        DateDelta,
        DateTimeDelta,
        Instant,
        LocalDateTime,
        OffsetDateTime,
        SystemDateTime,
        TimeDelta,
        ZonedDateTime,
    )
except ModuleNotFoundError as e:  # pragma: no cover
    raise RuntimeError(
        'The `whenever` module requires "whenever" to be installed. You can install it with "pip install whenever".'
    ) from e


# ==== Core types ======================================================================================================


class InstantAnnotation:
    """A type annotation `whenever.Instant` object. Because `whenever` objects are declared as `@final`, it is not
    possible to create a derived class with pydantic core schema implementations. However, by adding this annotation to
    a field with type `whenever.Instant`, serialization and validation works as expected.

    ```python
    from pydantic import BaseModel
    from pydantic_extra_types.whenever import InstantAnnotation
    from whenever import Instant


    class TestModel(BaseModel):
        instant: Annotated[Instant, InstantAnnotation]


    print(InstantTestModel(instant='2025-04-14 14:00:00Z'))

    # > instant=Instant(2025-04-14 14:00:00Z)
    ```
    """

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        """Return a Pydantic CoreSchema with Instant validation

        Args:
            source: The source type to be converted.
            handler: The handler to get the CoreSchema.

        Returns:
            A Pydantic CoreSchema with Instant validation.
        """
        return core_schema.no_info_wrap_validator_function(
            cls._validate,
            core_schema.datetime_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: instance.format_common_iso(),
                when_used='json-unless-none',
            ),
        )

    @staticmethod
    def _validate(value: Any, _: core_schema.ValidatorFunctionWrapHandler) -> Instant:
        """Validate the Instant object and return it.

        Args:
            value: The value to validate.
            handler: The handler to get the CoreSchema.

        Returns:
            The validated value or raises a PydanticCustomError or ValueError.
        """
        if isinstance(value, Instant):
            return value
        elif isinstance(value, datetime):
            return Instant.from_py_datetime(value)
        elif isinstance(value, str):
            try:
                return Instant.parse_common_iso(value)
            except Exception:
                pass

            try:
                return Instant.parse_rfc3339(value)
            except Exception:
                pass

            try:
                return Instant.parse_rfc2822(value)
            except Exception:
                pass

            raise ValueError(f'no parsers from Instant could convert string value {value}')
        else:
            raise ValueError(f'value conversion from {value} of type {type(value)} to Instant is not supported')


class LocalDateTimeAnnotation:
    """A type annotation `whenever.LocalDateTime` object. Because `whenever` objects are declared as `@final`, it is not
    possible to create a derived class with pydantic core schema implementations. However, by adding this annotation to
    a field with type `whenever.LocalDateTime`, serialization and validation works as expected.

    ```python
    from pydantic import BaseModel
    from pydantic_extra_types.whenever import LocalDateTimeAnnotation
    from whenever import LocalDateTime


    class TestModel(BaseModel):
        local_dt: Annotated[LocalDateTime, LocalDateTimeAnnotation]


    print(LocalDateTimeTestModel(local_dt='2025-04-14T14:00:00'))

    # > local_dt=LocalDateTime(2025-04-14 14:00:00)
    ```
    """

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        """Return a Pydantic CoreSchema with LocalDateTime validation

        Args:
            source: The source type to be converted.
            handler: The handler to get the CoreSchema.

        Returns:
            A Pydantic CoreSchema with LocalDateTime validation.
        """
        return core_schema.no_info_wrap_validator_function(
            cls._validate,
            core_schema.datetime_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: instance.format_common_iso(),
                when_used='json-unless-none',
            ),
        )

    @staticmethod
    def _validate(value: Any, _: core_schema.ValidatorFunctionWrapHandler) -> LocalDateTime:
        """Validate the LocalDateTime object and return it.

        Args:
            value: The value to validate.
            handler: The handler to get the CoreSchema.

        Returns:
            The validated value or raises a PydanticCustomError or ValueError.
        """
        if isinstance(value, LocalDateTime):
            return value
        elif isinstance(value, datetime):
            return LocalDateTime.from_py_datetime(value)
        elif isinstance(value, str):
            try:
                return LocalDateTime.parse_common_iso(value)
            except Exception:
                raise ValueError(f'no parsers from LocalDateTime could convert string value {value}')
        else:
            raise ValueError(f'value conversion from {value} of type {type(value)} to LocalDateTime is not supported')


class ZonedDateTimeAnnotation:
    """A type annotation `whenever.ZonedDateTime` object. Because `whenever` objects are declared as `@final`, it is not
    possible to create a derived class with pydantic core schema implementations. However, by adding this annotation to
    a field with type `whenever.ZonedDateTime`, serialization and validation works as expected.

    ```python
    from pydantic import BaseModel
    from pydantic_extra_types.whenever import ZonedDateTimeAnnotation
    from whenever import ZonedDateTime


    class TestModel(BaseModel):
        zoned_dt: Annotated[ZonedDateTime, ZonedDateTimeAnnotation]


    print(ZonedDateTimeTestModel(zoned_dt='2025-04-14T21:11:00-07:00[America/Los_Angeles]'))

    # > zoned_dt=ZonedDateTime(2025-04-14 21:11:00-07:00[America/Los_Angeles])
    ```
    """

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        """Return a Pydantic CoreSchema with ZonedDateTime validation

        Args:
            source: The source type to be converted.
            handler: The handler to get the CoreSchema.

        Returns:
            A Pydantic CoreSchema with ZonedDateTime validation.
        """
        return core_schema.no_info_wrap_validator_function(
            cls._validate,
            core_schema.datetime_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: instance.format_common_iso(),
                when_used='json-unless-none',
            ),
        )

    @staticmethod
    def _validate(value: Any, _: core_schema.ValidatorFunctionWrapHandler) -> ZonedDateTime:
        """Validate the ZonedDateTime object and return it.

        Args:
            value: The value to validate.
            handler: The handler to get the CoreSchema.

        Returns:
            The validated value or raises a PydanticCustomError or ValueError.
        """
        if isinstance(value, ZonedDateTime):
            return value
        elif isinstance(value, datetime):
            return ZonedDateTime.from_py_datetime(value)
        elif isinstance(value, str):
            try:
                return ZonedDateTime.parse_common_iso(value)
            except Exception:
                raise ValueError(f'no parsers from ZonedDateTime could convert string value {value}')
        else:
            raise ValueError(f'value conversion from {value} of type {type(value)} to ZonedDateTime is not supported')


# ==== Advanced types ==================================================================================================


class OffsetDateTimeAnnotation:
    """A type annotation `whenever.OffsetDateTime` object. Because `whenever` objects are declared as `@final`, it is
    not possible to create a derived class with pydantic core schema implementations. However, by adding this annotation
    to a field with type `whenever.OffsetDateTime`, serialization and validation works as expected.

    ```python
    from pydantic import BaseModel
    from pydantic_extra_types.whenever import OffsetDateTimeAnnotation
    from whenever import OffsetDateTime


    class TestModel(BaseModel):
        offset_dt: Annotated[OffsetDateTime, OffsetDateTimeAnnotation]


    print(OffsetDateTimeTestModel(offset_dt='2025-04-14 14:00:00-07:00'))

    # > offset_dt=OffsetDateTime(2025-04-14 14:00:00-07:00)
    ```
    """

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        """Return a Pydantic CoreSchema with OffsetDateTime validation

        Args:
            source: The source type to be converted.
            handler: The handler to get the CoreSchema.

        Returns:
            A Pydantic CoreSchema with OffsetDateTime validation.
        """
        return core_schema.no_info_wrap_validator_function(
            cls._validate,
            core_schema.datetime_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: instance.format_common_iso(),
                when_used='json-unless-none',
            ),
        )

    @staticmethod
    def _validate(value: Any, _: core_schema.ValidatorFunctionWrapHandler) -> OffsetDateTime:
        """Validate the OffsetDateTime object and return it.

        Args:
            value: The value to validate.
            handler: The handler to get the CoreSchema.

        Returns:
            The validated value or raises a PydanticCustomError or ValueError.
        """
        if isinstance(value, OffsetDateTime):
            return value
        elif isinstance(value, datetime):
            return OffsetDateTime.from_py_datetime(value)
        elif isinstance(value, str):
            try:
                return OffsetDateTime.parse_common_iso(value)
            except Exception:
                pass

            try:
                return OffsetDateTime.parse_rfc3339(value)
            except Exception:
                pass

            try:
                return OffsetDateTime.parse_rfc2822(value)
            except Exception:
                pass

            raise ValueError(f'no parsers from OffsetDateTime could convert string value {value}')
        else:
            raise ValueError(f'value conversion from {value} of type {type(value)} to OffsetDateTime is not supported')


class SystemDateTimeAnnotation:
    """A type annotation `whenever.SystemDateTime` object. Because `whenever` objects are declared as `@final`, it is
    not possible to create a derived class with pydantic core schema implementations. However, by adding this annotation
    to a field with type `whenever.SystemDateTime`, serialization and validation works as expected.

    ```python
    from pydantic import BaseModel
    from pydantic_extra_types.whenever import SystemDateTimeAnnotation
    from whenever import SystemDateTime


    class TestModel(BaseModel):
        system_dt: Annotated[SystemDateTime, SystemDateTimeAnnotation]


    print(SystemDateTimeTestModel(system_dt='2025-04-14T14:00:00-07:00'))

    # > system_dt=SystemDateTime(2025-04-14 14:00:00-07:00)
    ```
    """

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        """Return a Pydantic CoreSchema with SystemDateTime validation

        Args:
            source: The source type to be converted.
            handler: The handler to get the CoreSchema.

        Returns:
            A Pydantic CoreSchema with SystemDateTime validation.
        """
        return core_schema.no_info_wrap_validator_function(
            cls._validate,
            core_schema.datetime_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: instance.format_common_iso(),
                when_used='json-unless-none',
            ),
        )

    @staticmethod
    def _validate(value: Any, _: core_schema.ValidatorFunctionWrapHandler) -> SystemDateTime:
        """Validate the SystemDateTime object and return it.

        Args:
            value: The value to validate.
            handler: The handler to get the CoreSchema.

        Returns:
            The validated value or raises a PydanticCustomError or ValueError.
        """
        if isinstance(value, SystemDateTime):
            return value
        elif isinstance(value, datetime):
            return SystemDateTime.from_py_datetime(value)
        elif isinstance(value, str):
            try:
                return SystemDateTime.parse_common_iso(value)
            except Exception:
                raise ValueError(f'no parsers from SystemDateTime could convert string value {value}')
        else:
            raise ValueError(f'value conversion from {value} of type {type(value)} to SystemDateTime is not supported')


# ==== Deltas ==========================================================================================================


class TimeDeltaAnnotation:
    """A type annotation `whenever.TimeDelta` object. Because `whenever` objects are declared as `@final`, it is not
    possible to create a derived class with pydantic core schema implementations. However, by adding this annotation to
    a field with type `whenever.TimeDelta`, serialization and validation works as expected.

    ```python
    from pydantic import BaseModel
    from pydantic_extra_types.whenever import TimeDeltaAnnotation
    from whenever import TimeDelta


    class TestModel(BaseModel):
        delta_t: Annotated[TimeDelta, TimeDeltaAnnotation]


    print(TimeDeltaTestModel(delta_t='PT23H11M11S'))

    # > delta_t=TimeDelta(23:11:11)
    ```
    """

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        """Return a Pydantic CoreSchema with TimeDelta validation

        Args:
            source: The source type to be converted.
            handler: The handler to get the CoreSchema.

        Returns:
            A Pydantic CoreSchema with TimeDelta validation.
        """
        return core_schema.no_info_wrap_validator_function(
            cls._validate,
            core_schema.timedelta_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: instance.format_common_iso(),
                when_used='json-unless-none',
            ),
        )

    @staticmethod
    def _validate(value: Any, _: core_schema.ValidatorFunctionWrapHandler) -> TimeDelta:
        """Validate the TimeDelta object and return it.

        Args:
            value: The value to validate.
            handler: The handler to get the CoreSchema.

        Returns:
            The validated value or raises a PydanticCustomError or ValueError.
        """
        if isinstance(value, TimeDelta):
            return value
        elif isinstance(value, timedelta):
            return TimeDelta.from_py_timedelta(value)
        elif isinstance(value, str):
            try:
                return TimeDelta.parse_common_iso(value)
            except Exception as exc:
                raise PydanticCustomError('value_error', 'value string format is not supported by TimeDelta') from exc
        else:
            raise ValueError(f'value conversion from {value} of type {type(value)} to TimeDelta is not supported')


class DateDeltaAnnotation:
    """A type annotation `whenever.DateDelta` object. Because `whenever` objects are declared as `@final`, it is not
    possible to create a derived class with pydantic core schema implementations. However, by adding this annotation to
    a field with type `whenever.DateDelta`, serialization and validation works as expected.

    ```python
    from pydantic import BaseModel
    from pydantic_extra_types.whenever import DateDeltaAnnotation
    from whenever import DateDelta


    class TestModel(BaseModel):
        delta_d: Annotated[DateDelta, DateDeltaAnnotation]


    print(DateDeltaTestModel(delta_d='P1Y2M3D'))

    # > delta_d=DateDelta(P1Y2M3D)
    ```
    """

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        """Return a Pydantic CoreSchema with DateDelta validation

        Args:
            source: The source type to be converted.
            handler: The handler to get the CoreSchema.

        Returns:
            A Pydantic CoreSchema with DateDelta validation.
        """
        return core_schema.no_info_wrap_validator_function(
            cls._validate,
            core_schema.timedelta_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: instance.format_common_iso(),
                when_used='json-unless-none',
            ),
        )

    @staticmethod
    def _validate(value: Any, _: core_schema.ValidatorFunctionWrapHandler) -> DateDelta:
        """Validate the DateTimeDelta object and return it.

        Args:
            value: The value to validate.
            handler: The handler to get the CoreSchema.

        Returns:
            The validated value or raises a PydanticCustomError or ValueError.
        """
        if isinstance(value, DateDelta):
            return value
        elif isinstance(value, str):
            try:
                return DateDelta.parse_common_iso(value)
            except Exception as exc:
                raise PydanticCustomError('value_error', 'value string format is not supported by DateDelta') from exc
        else:
            raise ValueError(f'value conversion from {value} of type {type(value)} to DateDelta is not supported')


class DateTimeDeltaAnnotation:
    """A type annotation `whenever.DateTimeDelta` object. Because `whenever` objects are declared as `@final`, it is not
    possible to create a derived class with pydantic core schema implementations. However, by adding this annotation to
    a field with type `whenever.DateTimeDelta`, serialization and validation works as expected.

    ```python
    from pydantic import BaseModel
    from pydantic_extra_types.whenever import DateTimeDeltaAnnotation
    from whenever import DateTimeDelta


    class TestModel(BaseModel):
        delta_dt: Annotated[DateTimeDelta, DateTimeDeltaAnnotation]


    print(DateTimeTestModel(delta_dt='P1DT23H'))

    # > delta_dt=DateTimeDelta(P1DT23H)
    ```
    """

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        """Return a Pydantic CoreSchema with DateTimeDelta validation

        Args:
            source: The source type to be converted.
            handler: The handler to get the CoreSchema.

        Returns:
            A Pydantic CoreSchema with DateTimeDelta validation.
        """
        return core_schema.no_info_wrap_validator_function(
            cls._validate,
            core_schema.timedelta_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: instance.format_common_iso(),
                when_used='json-unless-none',
            ),
        )

    @staticmethod
    def _validate(value: Any, _: core_schema.ValidatorFunctionWrapHandler) -> DateTimeDelta:
        """Validate the DateTimeDelta object and return it.

        Args:
            value: The value to validate.
            handler: The handler to get the CoreSchema.

        Returns:
            The validated value or raises a PydanticCustomError or ValueError.
        """
        if isinstance(value, DateTimeDelta):
            return value
        elif isinstance(value, str):
            try:
                return DateTimeDelta.parse_common_iso(value)
            except Exception as exc:
                raise PydanticCustomError(
                    'value_error', 'value string format is not supported by DateTimeDelta'
                ) from exc
        else:
            raise ValueError(f'value conversion from {value} of type {type(value)} to DateTimeDelta is not supported')
