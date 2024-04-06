"""
Native Pendulum DateTime object implementation. This is a copy of the Pendulum DateTime object, but with a Pydantic
CoreSchema implementation. This allows Pydantic to validate the DateTime object.
"""

try:
    from pendulum import Date as _Date
    from pendulum import DateTime as _DateTime
    from pendulum import Duration as _Duration
    from pendulum import parse
except ModuleNotFoundError:  # pragma: no cover
    raise RuntimeError(
        'The `pendulum_dt` module requires "pendulum" to be installed. You can install it with "pip install pendulum".'
    )
from typing import Any, List, Type

from pydantic import GetCoreSchemaHandler
from pydantic_core import PydanticCustomError, core_schema


class DateTime(_DateTime):
    """
    A `pendulum.DateTime` object. At runtime, this type decomposes into pendulum.DateTime automatically.
    This type exists because Pydantic throws a fit on unknown types.

    ```python
    from pydantic import BaseModel
    from pydantic_extra_types.pendulum_dt import DateTime

    class test_model(BaseModel):
        dt: DateTime

    print(test_model(dt='2021-01-01T00:00:00+00:00'))

    #> test_model(dt=DateTime(2021, 1, 1, 0, 0, 0, tzinfo=FixedTimezone(0, name="+00:00")))
    ```
    """

    __slots__: List[str] = []

    @classmethod
    def __get_pydantic_core_schema__(cls, source: Type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        """
        Return a Pydantic CoreSchema with the Datetime validation

        Args:
            source: The source type to be converted.
            handler: The handler to get the CoreSchema.

        Returns:
            A Pydantic CoreSchema with the Datetime validation.
        """
        return core_schema.no_info_wrap_validator_function(cls._validate, core_schema.datetime_schema())

    @classmethod
    def _validate(cls, value: Any, handler: core_schema.ValidatorFunctionWrapHandler) -> Any:
        """
        Validate the datetime object and return it.

        Args:
            value: The value to validate.
            handler: The handler to get the CoreSchema.

        Returns:
            The validated value or raises a PydanticCustomError.
        """
        # if we are passed an existing instance, pass it straight through.
        if isinstance(value, _DateTime):
            return handler(value)

        # otherwise, parse it.
        try:
            data = parse(value)
        except Exception as exc:
            raise PydanticCustomError('value_error', 'value is not a valid timestamp') from exc
        return handler(data)


class Date(_Date):
    """
    A `pendulum.Date` object. At runtime, this type decomposes into pendulum.Date automatically.
    This type exists because Pydantic throws a fit on unknown types.

    ```python
    from pydantic import BaseModel
    from pydantic_extra_types.pendulum_dt import Date

    class test_model(BaseModel):
        dt: Date

    print(test_model(dt='2021-01-01'))

    #> test_model(dt=Date(2021, 1, 1))
    ```
    """

    __slots__: List[str] = []

    @classmethod
    def __get_pydantic_core_schema__(cls, source: Type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        """
        Return a Pydantic CoreSchema with the Date validation

        Args:
            source: The source type to be converted.
            handler: The handler to get the CoreSchema.

        Returns:
            A Pydantic CoreSchema with the Date validation.
        """
        return core_schema.no_info_wrap_validator_function(cls._validate, core_schema.date_schema())

    @classmethod
    def _validate(cls, value: Any, handler: core_schema.ValidatorFunctionWrapHandler) -> Any:
        """
        Validate the date object and return it.

        Args:
            value: The value to validate.
            handler: The handler to get the CoreSchema.

        Returns:
            The validated value or raises a PydanticCustomError.
        """
        # if we are passed an existing instance, pass it straight through.
        if isinstance(value, _Date):
            return handler(value)

        # otherwise, parse it.
        try:
            data = parse(value)
        except Exception as exc:
            raise PydanticCustomError('value_error', 'value is not a valid date') from exc
        return handler(data)


class Duration(_Duration):
    """
    A `pendulum.Duration` object. At runtime, this type decomposes into pendulum.Duration automatically.
    This type exists because Pydantic throws a fit on unknown types.

    ```python
    from pydantic import BaseModel
    from pydantic_extra_types.pendulum_dt import Duration

    class test_model(BaseModel):
        delta_t: Duration

    print(test_model(delta_t='P1DT25H'))

    #> test_model(delta_t=Duration(days=2, hours=1))
    ```
    """

    __slots__: List[str] = []

    @classmethod
    def __get_pydantic_core_schema__(cls, source: Type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        """
        Return a Pydantic CoreSchema with the Duration validation

        Args:
            source: The source type to be converted.
            handler: The handler to get the CoreSchema.

        Returns:
            A Pydantic CoreSchema with the Duration validation.
        """
        return core_schema.no_info_wrap_validator_function(cls._validate, core_schema.timedelta_schema())

    @classmethod
    def _validate(cls, value: Any, handler: core_schema.ValidatorFunctionWrapHandler) -> Any:
        """
        Validate the Duration object and return it.

        Args:
            value: The value to validate.
            handler: The handler to get the CoreSchema.

        Returns:
            The validated value or raises a PydanticCustomError.
        """
        # if we are passed an existing instance, pass it straight through.
        if isinstance(value, _Duration):
            return handler(value)

        # otherwise, parse it.
        try:
            data = parse(value)
        except Exception as exc:
            raise PydanticCustomError('value_error', 'value is not a valid duration') from exc
        return handler(data)
