from typing import Annotated

import pandas as pd
import pytest
from pydantic import BaseModel, TypeAdapter, ValidationError

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
    required_columns = ['name', 'email']


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
