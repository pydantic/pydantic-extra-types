"""Pydantic-compatible wrappers for pandas types.

This module provides a Pydantic ``CoreSchema`` for ``pandas.Timestamp`` so it can be used directly
as a field annotation on a ``BaseModel``. It also exposes lightweight ``Series`` and ``DataFrame``
annotations that pass instances through unchanged (no schema enforcement) and serialize to
JSON-friendly Python objects.

pandas is an optional dependency. Install with ``pip install 'pydantic-extra-types[pandas]'``.
"""

from __future__ import annotations

try:
    import pandas as pd
except ModuleNotFoundError as e:  # pragma: no cover
    raise RuntimeError(
        'The `pandas_types` module requires "pandas" to be installed. '
        'You can install it with "pip install pandas" or "pip install pydantic-extra-types[pandas]".'
    ) from e

from datetime import datetime
from typing import Any

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, PydanticCustomError, core_schema


class Timestamp(pd.Timestamp):
    """A `pandas.Timestamp` annotation usable directly on a Pydantic model.

    ```python
    from pydantic import BaseModel
    from pydantic_extra_types.pandas_types import Timestamp


    class Event(BaseModel):
        ts: Timestamp


    event = Event(ts='2024-01-01T00:00:00')
    # > event.ts -> Timestamp('2024-01-01 00:00:00')
    ```
    """

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> CoreSchema:
        return core_schema.no_info_plain_validator_function(
            cls._validate,
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: instance.isoformat(),
                when_used='json-unless-none',
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, _schema: CoreSchema, handler: GetJsonSchemaHandler) -> JsonSchemaValue:
        return {'type': 'string', 'format': 'date-time'}

    @classmethod
    def _validate(cls, value: Any) -> pd.Timestamp:
        # Pass through existing pandas / datetime instances.
        if isinstance(value, pd.Timestamp):
            return value
        if isinstance(value, datetime):
            return pd.Timestamp(value)
        if isinstance(value, (str, int, float)):
            try:
                return pd.Timestamp(value)
            except (ValueError, TypeError) as exc:
                raise PydanticCustomError('value_error', 'value is not a valid pandas Timestamp') from exc
        raise PydanticCustomError('value_error', 'value is not a valid pandas Timestamp')


class Series:
    """Annotation for a `pandas.Series`.

    The Series instance is passed through unchanged (no element-level validation since pandas
    does not carry that schema information). For JSON serialization the Series is converted via
    ``Series.to_list()``.
    """

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> CoreSchema:
        return core_schema.no_info_plain_validator_function(
            cls._validate,
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: instance.to_list(),
                when_used='json-unless-none',
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, _schema: CoreSchema, handler: GetJsonSchemaHandler) -> JsonSchemaValue:
        return {'type': 'array', 'items': {}}

    @classmethod
    def _validate(cls, value: Any) -> pd.Series:
        if isinstance(value, pd.Series):
            return value
        if isinstance(value, (list, tuple)):
            return pd.Series(list(value))
        raise PydanticCustomError('value_error', 'value is not a valid pandas Series')


class DataFrame:
    """Annotation for a `pandas.DataFrame`.

    The DataFrame instance is passed through unchanged. For JSON serialization the DataFrame is
    converted via ``DataFrame.to_dict(orient='records')``.
    """

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> CoreSchema:
        return core_schema.no_info_plain_validator_function(
            cls._validate,
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: instance.to_dict(orient='records'),
                when_used='json-unless-none',
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, _schema: CoreSchema, handler: GetJsonSchemaHandler) -> JsonSchemaValue:
        return {'type': 'array', 'items': {'type': 'object'}}

    @classmethod
    def _validate(cls, value: Any) -> pd.DataFrame:
        if isinstance(value, pd.DataFrame):
            return value
        # Accept list of dicts or a dict-of-lists (common pandas constructors).
        if isinstance(value, (list, dict)):
            try:
                return pd.DataFrame(value)
            except (ValueError, TypeError) as exc:
                raise PydanticCustomError('value_error', 'value is not a valid pandas DataFrame') from exc
        raise PydanticCustomError('value_error', 'value is not a valid pandas DataFrame')
