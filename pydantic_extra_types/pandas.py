"""The `pydantic_extra_types.pandas` module provides pandas-backed data types.

This module depends on the [pandas](https://pandas.pydata.org/) package.
"""

from __future__ import annotations

from typing import Any

from pydantic import GetCoreSchemaHandler
from pydantic_core import PydanticCustomError, core_schema

try:
    import pandas as pd
except ModuleNotFoundError as e:  # pragma: no cover
    raise RuntimeError(
        'The `pandas` module requires "pandas" to be installed. You can install it with "pip install pandas".'
    ) from e


class Series(pd.Series):
    """A pandas `Series` with Pydantic validation support.

    ```py
    from pydantic import BaseModel

    from pydantic_extra_types.pandas import Series


    class Model(BaseModel):
        values: Series


    model = Model(values=[1, 2, 3])
    print(model.values)
    # > 0    1
    # > 1    2
    # > 2    3
    # > dtype: int64
    ```
    """

    @classmethod
    def _validate(cls, __input_value: pd.Series[Any] | list[Any], _: core_schema.ValidationInfo) -> Series:
        try:
            return cls(__input_value)
        except (TypeError, ValueError) as exc:
            raise PydanticCustomError('pandas_series_type', 'Input should be a valid pandas Series') from exc

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source: type[Any],
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        from_list_schema = core_schema.list_schema(items_schema=core_schema.any_schema())

        return core_schema.json_or_python_schema(
            json_schema=core_schema.with_info_after_validator_function(cls._validate, from_list_schema),
            python_schema=core_schema.with_info_after_validator_function(
                cls._validate,
                core_schema.union_schema([core_schema.is_instance_schema(pd.Series), from_list_schema]),
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda value: value.tolist(), when_used='json'
            ),
        )


class DataFrame(pd.DataFrame):
    """A pandas `DataFrame` with Pydantic validation support.

    ```py
    from pydantic import BaseModel

    from pydantic_extra_types.pandas import DataFrame


    class Model(BaseModel):
        table: DataFrame


    model = Model(table=[{'name': 'alice'}, {'name': 'bob'}])
    print(model.table)
    # >     name
    # > 0  alice
    # > 1    bob
    ```
    """

    @classmethod
    def _validate(
        cls,
        __input_value: pd.DataFrame | list[dict[str, Any]] | dict[str, list[Any]],
        _: core_schema.ValidationInfo,
    ) -> DataFrame:
        try:
            return cls(__input_value)
        except (TypeError, ValueError) as exc:
            raise PydanticCustomError('pandas_dataframe_type', 'Input should be a valid pandas DataFrame') from exc

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source: type[Any],
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        records_schema = core_schema.list_schema(
            items_schema=core_schema.dict_schema(
                keys_schema=core_schema.str_schema(),
                values_schema=core_schema.any_schema(),
            )
        )
        columnar_schema = core_schema.dict_schema(
            keys_schema=core_schema.str_schema(),
            values_schema=core_schema.list_schema(items_schema=core_schema.any_schema()),
        )
        from_data_schema = core_schema.union_schema([records_schema, columnar_schema])

        return core_schema.json_or_python_schema(
            json_schema=core_schema.with_info_after_validator_function(cls._validate, from_data_schema),
            python_schema=core_schema.with_info_after_validator_function(
                cls._validate,
                core_schema.union_schema([core_schema.is_instance_schema(pd.DataFrame), from_data_schema]),
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda value: value.to_dict(orient='records'),
                when_used='json',
            ),
        )
