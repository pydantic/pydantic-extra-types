"""The `pydantic_extra_types.pandas` module provides the
[`PandasDataFrame`][pydantic_extra_types.pandas.PandasDataFrame] data type.

This class depends on the [pandas](https://pypi.org/project/pandas/) package.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import partial
from typing import Any

from pydantic import GetCoreSchemaHandler
from pydantic_core import PydanticCustomError, core_schema

try:
    import pandas as pd
except ModuleNotFoundError as e:
    raise RuntimeError(
        '`PandasDataFrame` requires "pandas" to be installed. You can install it with "pip install pandas"'
    ) from e


class PandasDataFrame:
    """A wrapper type that validates an object is a `pandas.DataFrame`.

    You can optionally require a set of columns to be present in the
    DataFrame by setting `required_columns` either via subclassing or
    by using the [`PandasDataFrameValidator`][pydantic_extra_types.pandas.PandasDataFrameValidator]
    annotation.

    ## Examples

    ### Basic usage:

    ```python
    import pandas as pd
    from pydantic import BaseModel
    from pydantic_extra_types.pandas import PandasDataFrame


    class Model(BaseModel):
        df: PandasDataFrame


    m = Model(df=pd.DataFrame({'a': [1, 2, 3]}))
    print(m.df)
    ```

    ### With required columns via subclassing:

    ```python
    import pandas as pd
    from pydantic import BaseModel
    from pydantic_extra_types.pandas import PandasDataFrame


    class UserFrame(PandasDataFrame):
        required_columns = ['name', 'email']


    class Model(BaseModel):
        df: UserFrame


    # This will raise a validation error because 'email' is missing
    m = Model(df=pd.DataFrame({'name': ['Alice']}))
    ```

    ### With required columns via annotation:

    ```python
    from typing import Annotated
    import pandas as pd
    from pydantic import BaseModel
    from pydantic_extra_types.pandas import PandasDataFrameValidator

    UserFrame = Annotated[pd.DataFrame, PandasDataFrameValidator(required_columns=['name', 'email'])]


    class Model(BaseModel):
        df: UserFrame


    m = Model(df=pd.DataFrame({'name': ['Alice'], 'email': ['alice@example.com']}))
    print(m.df)
    ```
    """

    required_columns: list[str] | None = None
    """An optional list of column names that the DataFrame must contain."""

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.with_info_after_validator_function(
            cls._validate,
            core_schema.any_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetCoreSchemaHandler
    ) -> dict[str, Any]:
        json_schema = handler(schema)
        json_schema.update({'type': 'object', 'title': 'DataFrame'})
        return json_schema

    @classmethod
    def _validate(cls, value: Any, _: core_schema.ValidationInfo) -> pd.DataFrame:
        if not isinstance(value, pd.DataFrame):
            raise PydanticCustomError(
                'value_error',
                'value is not a valid pandas DataFrame',
            )

        if cls.required_columns:
            missing = [col for col in cls.required_columns if col not in value.columns]
            if missing:
                raise PydanticCustomError(
                    'value_error',
                    'DataFrame is missing required columns: {}'.format(', '.join(missing)),
                )

        return value


def _validate_dataframe(
    required_columns: list[str] | None,
    value: Any,
) -> pd.DataFrame:
    """Validate that *value* is a ``pd.DataFrame`` and (optionally) that it
    contains *required_columns*."""
    if not isinstance(value, pd.DataFrame):
        raise PydanticCustomError(
            'value_error',
            'value is not a valid pandas DataFrame',
        )

    if required_columns:
        missing = [col for col in required_columns if col not in value.columns]
        if missing:
            raise PydanticCustomError(
                'value_error',
                'DataFrame is missing required columns: {}'.format(', '.join(missing)),
            )

    return value


@dataclass(frozen=True)
class PandasDataFrameValidator:
    """An annotation to validate `pd.DataFrame` objects with column constraints.

    Example:
        ```python
        from typing import Annotated
        import pandas as pd
        from pydantic import BaseModel
        from pydantic_extra_types.pandas import PandasDataFrameValidator

        UserFrame = Annotated[pd.DataFrame, PandasDataFrameValidator(required_columns=['name', 'email'])]


        class Model(BaseModel):
            df: UserFrame


        m = Model(df=pd.DataFrame({'name': ['Alice'], 'email': ['alice@example.com']}))
        ```
    """

    required_columns: list[str] | None = None
    """An optional list of column names that the DataFrame must contain."""

    def __get_pydantic_core_schema__(self, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.no_info_before_validator_function(
            partial(
                _validate_dataframe,
                self.required_columns,
            ),
            core_schema.any_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetCoreSchemaHandler
    ) -> dict[str, Any]:
        json_schema = handler(schema)
        json_schema.update({'type': 'object', 'title': 'DataFrame'})
        return json_schema

    def __hash__(self) -> int:
        return super().__hash__()


class PandasSeries:
    """A wrapper type that validates an object is a `pandas.Series`.

    ## Examples

    ```python
    import pandas as pd
    from pydantic import BaseModel
    from pydantic_extra_types.pandas import PandasSeries


    class Model(BaseModel):
        s: PandasSeries


    m = Model(s=pd.Series([1, 2, 3]))
    print(m.s)
    ```
    """

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.with_info_after_validator_function(
            cls._validate,
            core_schema.any_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetCoreSchemaHandler
    ) -> dict[str, Any]:
        json_schema = handler(schema)
        json_schema.update({'type': 'array', 'title': 'Series'})
        return json_schema

    @classmethod
    def _validate(cls, value: Any, _: core_schema.ValidationInfo) -> pd.Series:
        if not isinstance(value, pd.Series):
            raise PydanticCustomError(
                'value_error',
                'value is not a valid pandas Series',
            )

        return value
