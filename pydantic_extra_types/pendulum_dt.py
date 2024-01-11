try:
    from pendulum import DateTime as _DateTime
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
    A pendulum.DateTime object.
    At runtime, this type decomposes into pendulum.DateTime automagically.
    This type exists because Pydantic throws a fit on unknown types.
    """

    __slots__: List[str] = []

    @classmethod
    def __get_pydantic_core_schema__(cls, source: Type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.no_info_wrap_validator_function(
            cls._validate_datetime, core_schema.is_instance_schema(_DateTime)
        )

    @classmethod
    def _validate_datetime(cls, value: Any, handler: core_schema.ValidatorFunctionWrapHandler) -> Any:
        # if we are passed an existing instance, pass it straight through.
        if isinstance(value, _DateTime):
            return handler(value)

        # otherwise, parse it.
        try:
            data = parse(value)
        except Exception as exc:
            raise PydanticCustomError('value_error', 'value is not a valid timestamp') from exc
        return handler(data)
