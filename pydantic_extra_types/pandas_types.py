from __future__ import annotations

try:
    import pandas as pd  # type: ignore[import-untyped]
except ModuleNotFoundError:  # pragma: no cover
    raise RuntimeError(
        'The `pandas_types` module requires "pandas" to be installed. '
        'You can install it with "pip install \'pydantic-extra-types[pandas]\'".'
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

    def __class_getitem__(cls, item: type) -> type:
        return type(f'Series[{item.__name__}]', (cls,), {'_item_type': item})

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
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
    """
    A `pandas.Index` with Pydantic validation support.

    Supports both untyped and typed usage:

    ```python
    from pydantic import BaseModel
    from pydantic_extra_types.pandas_types import Index


    class MyModel(BaseModel):
        idx: Index[str]


    model = MyModel(idx=['a', 'b', 'c'])
    print(model.idx.tolist())  # ['a', 'b', 'c']
    ```
    """

    _item_type: ClassVar[type | None] = None

    def __class_getitem__(cls, item: type) -> type:
        return type(f'Index[{item.__name__}]', (cls,), {'_item_type': item})

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
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
    def _validate(cls, value: Any, handler: core_schema.ValidatorFunctionWrapHandler) -> pd.Index:
        if isinstance(value, pd.Index):
            value = value.tolist()
        elif not isinstance(value, list):
            try:
                value = list(value)
            except Exception as exc:
                raise PydanticCustomError(
                    'index_invalid',
                    'Value must be list-like or a pandas Index, got {type}',
                    {'type': type(value).__name__},
                ) from exc
        validated: list[Any] = handler(value)
        return pd.Index(validated)


class DataFrame:
    """
    A `pandas.DataFrame` with Pydantic validation support.

    Accepts a TypedDict (or any class with ``__annotations__``) as a type parameter
    to validate column names and element types:

    ```python
    from typing import TypedDict
    from pydantic import BaseModel
    from pydantic_extra_types.pandas_types import DataFrame


    class MySchema(TypedDict):
        name: str
        age: int


    class MyModel(BaseModel):
        people: DataFrame[MySchema]


    model = MyModel(people={'name': ['Alice', 'Bob'], 'age': [30, 25]})
    print(model.people)
    ```
    """

    _schema_cls: ClassVar[type | None] = None

    def __class_getitem__(cls, schema_cls: type) -> type:
        return type(f'DataFrame[{schema_cls.__name__}]', (cls,), {'_schema_cls': schema_cls})

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        if cls._schema_cls is not None:
            annotations = cls._schema_cls.__annotations__
            fields = {
                col: core_schema.typed_dict_field(core_schema.list_schema(handler.generate_schema(col_type)))
                for col, col_type in annotations.items()
            }
            inner_schema: core_schema.CoreSchema = core_schema.typed_dict_schema(fields)
        else:
            inner_schema = core_schema.any_schema()

        return core_schema.no_info_wrap_validator_function(
            cls._validate,
            inner_schema,
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda v: {col: v[col].tolist() for col in v.columns},
                info_arg=False,
            ),
        )

    @classmethod
    def _validate(cls, value: Any, handler: core_schema.ValidatorFunctionWrapHandler) -> pd.DataFrame:
        extra_data: dict[str, Any] = {}

        if isinstance(value, pd.DataFrame):
            if cls._schema_cls is not None:
                known_cols = set(cls._schema_cls.__annotations__.keys())
                extra_cols = [c for c in value.columns if c not in known_cols]
                extra_data = {c: value[c].tolist() for c in extra_cols}
                value = {c: value[c].tolist() for c in value.columns if c in known_cols}
            else:
                value = {c: value[c].tolist() for c in value.columns}
        elif not isinstance(value, dict):
            raise PydanticCustomError(
                'dataframe_invalid',
                'Value must be a dict or pandas DataFrame, got {type}',
                {'type': type(value).__name__},
            )

        validated = handler(value)
        result = pd.DataFrame(validated)
        for col, data in extra_data.items():
            result[col] = data
        return result
