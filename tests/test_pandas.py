import builtins
import importlib.util
import sys
from typing import Annotated, ClassVar

import pandas as pd
import pytest
from pydantic import BaseModel, TypeAdapter, ValidationError

import pydantic_extra_types.pandas as pandas_module
from pydantic_extra_types.pandas import (
    PandasDataFrame,
    PandasDataFrameValidator,
    PandasSeries,
)


class DataFrameModel(BaseModel):
    df: PandasDataFrame


class SeriesModel(BaseModel):
    s: PandasSeries


def test_valid_dataframe() -> None:
    df = pd.DataFrame({'a': [1, 2, 3]})
    result = DataFrameModel(df=df)
    assert isinstance(result.df, pd.DataFrame)
    assert result.df.equals(df)


def test_invalid_dataframe_not_a_dataframe() -> None:
    with pytest.raises(ValidationError, match='value is not a valid pandas DataFrame'):
        DataFrameModel(df='not a dataframe')


def test_invalid_dataframe_none() -> None:
    with pytest.raises(ValidationError, match='value is not a valid pandas DataFrame'):
        DataFrameModel(df=None)


def test_invalid_dataframe_int() -> None:
    with pytest.raises(ValidationError, match='value is not a valid pandas DataFrame'):
        DataFrameModel(df=42)


def test_valid_series() -> None:
    s = pd.Series([1, 2, 3])
    result = SeriesModel(s=s)
    assert isinstance(result.s, pd.Series)
    assert result.s.equals(s)


def test_invalid_series_not_a_series() -> None:
    with pytest.raises(ValidationError, match='value is not a valid pandas Series'):
        SeriesModel(s='not a series')


def test_invalid_series_none() -> None:
    with pytest.raises(ValidationError, match='value is not a valid pandas Series'):
        SeriesModel(s=None)


def test_invalid_series_int() -> None:
    with pytest.raises(ValidationError, match='value is not a valid pandas Series'):
        SeriesModel(s=42)


def test_empty_dataframe() -> None:
    df = pd.DataFrame()
    result = DataFrameModel(df=df)
    assert isinstance(result.df, pd.DataFrame)


def test_empty_series() -> None:
    s = pd.Series(dtype='float64')
    result = SeriesModel(s=s)
    assert isinstance(result.s, pd.Series)


def test_dataframe_with_multiple_columns() -> None:
    df = pd.DataFrame({'name': ['Alice', 'Bob'], 'age': [30, 25]})
    result = DataFrameModel(df=df)
    assert list(result.df.columns) == ['name', 'age']


class RequiredColumnsFrame(PandasDataFrame):
    required_columns: ClassVar[list[str]] = ['name', 'email']


class RequiredColumnsModel(BaseModel):
    df: RequiredColumnsFrame


def test_dataframe_with_required_columns_passes() -> None:
    df = pd.DataFrame({'name': ['Alice'], 'email': ['alice@example.com']})
    result = RequiredColumnsModel(df=df)
    assert isinstance(result.df, pd.DataFrame)


def test_dataframe_with_required_columns_fails() -> None:
    df = pd.DataFrame({'name': ['Alice']})
    with pytest.raises(ValidationError, match='missing required columns'):
        RequiredColumnsModel(df=df)


def test_dataframe_with_required_columns_multiple_missing() -> None:
    df = pd.DataFrame({'foo': [1]})
    with pytest.raises(ValidationError, match='missing required columns'):
        RequiredColumnsModel(df=df)


def test_dataframe_with_required_columns_extra_columns_allowed() -> None:
    df = pd.DataFrame({'name': ['Alice'], 'email': ['alice@example.com'], 'age': [30]})
    result = RequiredColumnsModel(df=df)
    assert isinstance(result.df, pd.DataFrame)


AnnotatedFrame = Annotated[
    pd.DataFrame,
    PandasDataFrameValidator(required_columns=['name', 'email']),
]


class AnnotatedModel(BaseModel):
    df: AnnotatedFrame


def test_annotated_validator_passes() -> None:
    df = pd.DataFrame({'name': ['Alice'], 'email': ['alice@example.com']})
    result = AnnotatedModel(df=df)
    assert isinstance(result.df, pd.DataFrame)


def test_annotated_validator_fails() -> None:
    df = pd.DataFrame({'name': ['Alice']})
    with pytest.raises(ValidationError, match='missing required columns'):
        AnnotatedModel(df=df)


def test_annotated_validator_not_a_dataframe() -> None:
    with pytest.raises(ValidationError, match='value is not a valid pandas DataFrame'):
        AnnotatedModel(df='not a dataframe')


def test_annotated_validator_without_required_columns() -> None:
    adapter = TypeAdapter(Annotated[pd.DataFrame, PandasDataFrameValidator()])
    df = pd.DataFrame({'a': [1]})
    assert adapter.validate_python(df) is df


def test_annotated_validator_json_schema() -> None:
    adapter = TypeAdapter(Annotated[pd.DataFrame, PandasDataFrameValidator()])
    assert adapter.json_schema()['title'] == 'DataFrame'


def test_missing_pandas_dependency_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    original_import = builtins.__import__

    def import_without_pandas(name: str, *args, **kwargs):
        if name == 'pandas':
            raise ModuleNotFoundError("No module named 'pandas'")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, '__import__', import_without_pandas)
    module_name = 'pandas_without_dependency'
    spec = importlib.util.spec_from_file_location(module_name, pandas_module.__file__)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, module_name, module)

    with pytest.raises(RuntimeError, match='requires "pandas" to be installed'):
        spec.loader.exec_module(module)


def test_type_adapter_dataframe() -> None:
    adapter = TypeAdapter(PandasDataFrame)
    df = pd.DataFrame({'x': [1]})
    result = adapter.validate_python(df)
    assert isinstance(result, pd.DataFrame)
    assert result.equals(df)


def test_type_adapter_dataframe_fails() -> None:
    adapter = TypeAdapter(PandasDataFrame)
    with pytest.raises(ValidationError, match='value is not a valid pandas DataFrame'):
        adapter.validate_python(42)


def test_type_adapter_series() -> None:
    adapter = TypeAdapter(PandasSeries)
    s = pd.Series([1, 2, 3])
    result = adapter.validate_python(s)
    assert isinstance(result, pd.Series)
    assert result.equals(s)
