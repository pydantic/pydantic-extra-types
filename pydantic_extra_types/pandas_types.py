from __future__ import annotations

try:
    import pandas as pd
except ModuleNotFoundError:  # pragma: no cover
    raise RuntimeError(
        'The `pandas_types` module requires "pandas" to be installed. '
        "You can install it with \"pip install 'pydantic-extra-types[pandas]'\"."
    )

from typing import Any, ClassVar

from pydantic import GetCoreSchemaHandler
from pydantic_core import PydanticCustomError, core_schema


class Series(pd.Series):  # type: ignore[misc]
    """
    A `pandas.Series` with Pydantic validation support.

    Supports both untyped and typed usage:

    ```python
    from pydantic import BaseModel
    from pydantic_extra_types.pandas_types import Series

    class MyModel(BaseModel):
        values: Series[int]

    model = MyModel(values=[1, 2, 3])
    print(model.values.tolist())  # [1, 2, 3]
    ```
    """

    _item_type: ClassVar[type | None] = None

    def __class_getitem__(cls, item: type) -> type:  # type: ignore[override]
        return type(f'Series[{item.__name__}]', (cls,), {'_item_type': item})

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        if cls._item_type is not None:
            item_schema = handler.generate_schema(cls._item_type)
        else:
            item_schema = core_schema.any_schema()

        list_schema = core_schema.list_schema(item_schema)

        return core_schema.no_info_wrap_validator_function(
            cls._validate,
            list_schema,
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda v: v.tolist(),
                info_arg=False,
                return_schema=core_schema.list_schema(item_schema),
            ),
        )

    @classmethod
    def _validate(cls, value: Any, handler: core_schema.ValidatorFunctionWrapHandler) -> Series:
        if isinstance(value, pd.Series):
            value = value.tolist()
        elif not isinstance(value, list):
            try:
                value = list(value)
            except Exception as exc:
                raise PydanticCustomError(
                    'series_invalid',
                    'Value must be list-like or a pandas Series, got {type}',
                    {'type': type(value).__name__},
                ) from exc
        validated: list[Any] = handler(value)
        return Series(validated)


class Index:
    """Stub — to be implemented (Tasks 5/6)."""

    @classmethod
    def __class_getitem__(cls, item: type) -> type:
        return type(f'Index[{item.__name__}]', (cls,), {'_item_type': item})

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        def _not_implemented(v: Any) -> None:
            raise NotImplementedError('Index validation not yet implemented')

        return core_schema.no_info_plain_validator_function(_not_implemented)


class DataFrame:
    """Stub — to be implemented (Tasks 5/6)."""

    @classmethod
    def __class_getitem__(cls, item: type) -> type:
        return type(f'DataFrame[{item.__name__}]', (cls,), {'_schema_type': item})

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        def _not_implemented(v: Any) -> None:
            raise NotImplementedError('DataFrame validation not yet implemented')

        return core_schema.no_info_plain_validator_function(_not_implemented)
