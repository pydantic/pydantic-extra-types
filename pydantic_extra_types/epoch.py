import datetime
from typing import Any, Callable

from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, core_schema

EPOCH = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)


class Epoch(datetime.datetime):
    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        field_schema: dict[str, Any] = {}
        field_schema.update(type='number', format='date-time')
        return field_schema

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: type[Any], handler: Callable[[Any], CoreSchema]
    ) -> core_schema.CoreSchema:
        def f(value, serializer):
            return serializer(value.timestamp())
        return core_schema.with_info_after_validator_function(
                cls._validate, core_schema.float_schema(),
                serialization=core_schema.wrap_serializer_function_ser_schema(f, return_schema=core_schema.float_schema())
        )

    @classmethod
    def _validate(cls, __input_value: Any, _: Any) -> "Epoch":
        return EPOCH + datetime.timedelta(seconds=__input_value)


