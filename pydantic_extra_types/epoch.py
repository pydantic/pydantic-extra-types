import datetime
from typing import Any, Callable, Optional

import pydantic_core.core_schema
from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, core_schema

EPOCH = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)


class _Base(datetime.datetime):
    TYPE: str = ''
    CLS: Optional[Callable[[Any], Any]]
    SCHEMA: pydantic_core.core_schema.CoreSchema

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        field_schema: dict[str, Any] = {}
        field_schema.update(type=cls.TYPE, format='date-time')
        return field_schema

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: type[Any], handler: Callable[[Any], CoreSchema]
    ) -> core_schema.CoreSchema:
        def f(value: Any, serializer: Callable[[datetime.datetime], float]) -> float:
            ts = value.timestamp()
            return serializer(cls.CLS(ts) if cls.CLS is not None else ts)

        return core_schema.with_info_after_validator_function(
            cls._validate,
            cls.SCHEMA,
            serialization=core_schema.wrap_serializer_function_ser_schema(f, return_schema=cls.SCHEMA),
        )

    @classmethod
    def _validate(cls, __input_value: Any, _: Any) -> datetime.datetime:
        return EPOCH + datetime.timedelta(seconds=__input_value)


class Number(_Base):
    TYPE = 'number'
    CLS = None
    SCHEMA = core_schema.float_schema()


class Integer(_Base):
    TYPE = 'integer'
    CLS = int
    SCHEMA = core_schema.int_schema()
