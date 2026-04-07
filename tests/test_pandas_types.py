from __future__ import annotations

from typing import TypedDict

import pandas as pd
import pytest
from pydantic import BaseModel, ValidationError

from pydantic_extra_types.pandas_types import DataFrame, Index, Series

# ---------------------------------------------------------------------------
# Series
# ---------------------------------------------------------------------------


class UntypedSeriesModel(BaseModel):
    data: Series


class IntSeriesModel(BaseModel):
    data: Series[int]


class StrSeriesModel(BaseModel):
    data: Series[str]


@pytest.mark.parametrize(
    'value,expected',
    [
        ([1, 2, 3], [1, 2, 3]),
        ([], []),
        ((10, 20, 30), [10, 20, 30]),
        (pd.Series([1, 2, 3]), [1, 2, 3]),
        ([1, 'a', None], [1, 'a', None]),
    ],
)
def test_series_untyped_accepts_any(value, expected):
    model = UntypedSeriesModel(data=value)
    assert isinstance(model.data, pd.Series)
    assert model.data.tolist() == expected


@pytest.mark.parametrize(
    'value,expected',
    [
        ([1, 2, 3], [1, 2, 3]),
        (pd.Series([4, 5, 6]), [4, 5, 6]),
        ((7, 8, 9), [7, 8, 9]),
    ],
)
def test_series_typed_int_valid(value, expected):
    model = IntSeriesModel(data=value)
    assert isinstance(model.data, pd.Series)
    assert model.data.tolist() == expected


def test_series_typed_int_rejects_strings():
    with pytest.raises(ValidationError):
        IntSeriesModel(data=['a', 'b'])


def test_series_typed_str_valid():
    model = StrSeriesModel(data=['hello', 'world'])
    assert model.data.tolist() == ['hello', 'world']


def test_series_typed_str_rejects_ints():
    with pytest.raises(ValidationError):
        StrSeriesModel(data=[1, 2, 3])


def test_series_invalid_input_type():
    with pytest.raises(ValidationError):
        IntSeriesModel(data=42)


def test_series_is_pd_series():
    model = IntSeriesModel(data=[1, 2, 3])
    assert isinstance(model.data, pd.Series)


# ---------------------------------------------------------------------------
# Index
# ---------------------------------------------------------------------------


class UntypedIndexModel(BaseModel):
    idx: Index


class IntIndexModel(BaseModel):
    idx: Index[int]


class StrIndexModel(BaseModel):
    idx: Index[str]


@pytest.mark.parametrize(
    'value,expected',
    [
        ([1, 2, 3], [1, 2, 3]),
        (['a', 'b', 'c'], ['a', 'b', 'c']),
        (pd.Index([10, 20]), [10, 20]),
    ],
)
def test_index_untyped_accepts_any(value, expected):
    model = UntypedIndexModel(idx=value)
    assert isinstance(model.idx, pd.Index)
    assert model.idx.tolist() == expected


@pytest.mark.parametrize(
    'value,expected',
    [
        ([1, 2, 3], [1, 2, 3]),
        (pd.Index([4, 5, 6]), [4, 5, 6]),
    ],
)
def test_index_typed_int_valid(value, expected):
    model = IntIndexModel(idx=value)
    assert isinstance(model.idx, pd.Index)
    assert model.idx.tolist() == expected


def test_index_typed_int_rejects_strings():
    with pytest.raises(ValidationError):
        IntIndexModel(idx=['a', 'b'])


def test_index_typed_str_valid():
    model = StrIndexModel(idx=['x', 'y', 'z'])
    assert model.idx.tolist() == ['x', 'y', 'z']


def test_index_typed_str_rejects_ints():
    with pytest.raises(ValidationError):
        StrIndexModel(idx=[1, 2, 3])


def test_index_invalid_input_type():
    with pytest.raises(ValidationError):
        IntIndexModel(idx=99)


def test_index_is_pd_index():
    model = IntIndexModel(idx=[1, 2])
    assert isinstance(model.idx, pd.Index)


# ---------------------------------------------------------------------------
# DataFrame
# ---------------------------------------------------------------------------


class MySchema(TypedDict):
    col_a: int
    col_b: str


class UntypedDataFrameModel(BaseModel):
    df: DataFrame


class TypedDataFrameModel(BaseModel):
    df: DataFrame[MySchema]


def test_dataframe_untyped_from_dict():
    model = UntypedDataFrameModel(df={'x': [1, 2], 'y': [3, 4]})
    assert isinstance(model.df, pd.DataFrame)
    assert list(model.df.columns) == ['x', 'y']


def test_dataframe_untyped_from_pd_dataframe():
    df = pd.DataFrame({'a': [1], 'b': [2]})
    model = UntypedDataFrameModel(df=df)
    assert isinstance(model.df, pd.DataFrame)


def test_dataframe_typed_from_dict():
    model = TypedDataFrameModel(df={'col_a': [1, 2], 'col_b': ['x', 'y']})
    assert isinstance(model.df, pd.DataFrame)
    assert model.df['col_a'].tolist() == [1, 2]
    assert model.df['col_b'].tolist() == ['x', 'y']


def test_dataframe_typed_from_pd_dataframe():
    df = pd.DataFrame({'col_a': [10, 20], 'col_b': ['a', 'b']})
    model = TypedDataFrameModel(df=df)
    assert isinstance(model.df, pd.DataFrame)
    assert model.df['col_a'].tolist() == [10, 20]


def test_dataframe_typed_preserves_extra_columns():
    df = pd.DataFrame({'col_a': [1], 'col_b': ['x'], 'extra': [99]})
    model = TypedDataFrameModel(df=df)
    assert 'extra' in model.df.columns
    assert model.df['extra'].tolist() == [99]


def test_dataframe_typed_missing_column_raises():
    with pytest.raises(ValidationError):
        TypedDataFrameModel(df={'col_a': [1, 2]})  # col_b missing


def test_dataframe_typed_wrong_element_type_raises():
    with pytest.raises(ValidationError):
        TypedDataFrameModel(df={'col_a': ['not_int', 'not_int'], 'col_b': ['x', 'y']})


def test_dataframe_invalid_input_type():
    with pytest.raises(ValidationError):
        TypedDataFrameModel(df='not a dataframe')


def test_dataframe_is_pd_dataframe():
    model = TypedDataFrameModel(df={'col_a': [1], 'col_b': ['a']})
    assert isinstance(model.df, pd.DataFrame)
