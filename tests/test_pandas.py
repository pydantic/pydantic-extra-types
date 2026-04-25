from __future__ import annotations

import datetime as dt

import pytest

pd = pytest.importorskip('pandas')

from pydantic import BaseModel, ValidationError  # noqa: E402

from pydantic_extra_types.pandas_types import DataFrame, Series, Timestamp  # noqa: E402


class _TimestampModel(BaseModel):
    ts: Timestamp


class _SeriesModel(BaseModel):
    model_config = {'arbitrary_types_allowed': True}
    s: Series


class _DataFrameModel(BaseModel):
    model_config = {'arbitrary_types_allowed': True}
    df: DataFrame


def test_timestamp_from_iso_string() -> None:
    m = _TimestampModel(ts='2024-01-02T03:04:05')
    assert isinstance(m.ts, pd.Timestamp)
    assert m.ts == pd.Timestamp('2024-01-02T03:04:05')


def test_timestamp_from_existing_pandas_timestamp() -> None:
    ts = pd.Timestamp('2024-06-15')
    m = _TimestampModel(ts=ts)
    assert m.ts == ts


def test_timestamp_from_datetime() -> None:
    native = dt.datetime(2024, 1, 1, 12, 30)
    m = _TimestampModel(ts=native)
    assert m.ts == pd.Timestamp(native)


def test_timestamp_from_unix_seconds() -> None:
    # pandas treats ints as nanoseconds since epoch by default.
    m = _TimestampModel(ts=0)
    assert m.ts == pd.Timestamp(0)


def test_timestamp_invalid_string_raises() -> None:
    with pytest.raises(ValidationError):
        _TimestampModel(ts='not-a-real-date')


def test_timestamp_invalid_type_raises() -> None:
    with pytest.raises(ValidationError):
        _TimestampModel(ts=object())


def test_timestamp_json_serialization() -> None:
    m = _TimestampModel(ts='2024-01-02T03:04:05')
    dumped = m.model_dump(mode='json')
    assert dumped['ts'] == '2024-01-02T03:04:05'


def test_timestamp_json_schema() -> None:
    schema = _TimestampModel.model_json_schema()
    prop = schema['properties']['ts']
    assert prop['type'] == 'string'
    assert prop['format'] == 'date-time'


def test_series_passthrough() -> None:
    s = pd.Series([1, 2, 3])
    m = _SeriesModel(s=s)
    assert m.s.equals(s)


def test_series_from_list() -> None:
    m = _SeriesModel(s=[1, 2, 3])
    assert isinstance(m.s, pd.Series)
    assert m.s.tolist() == [1, 2, 3]


def test_series_invalid_type() -> None:
    with pytest.raises(ValidationError):
        _SeriesModel(s=12345)


def test_series_json_serialization() -> None:
    m = _SeriesModel(s=pd.Series([1, 2, 3]))
    assert m.model_dump(mode='json')['s'] == [1, 2, 3]


def test_series_json_schema() -> None:
    schema = _SeriesModel.model_json_schema()
    assert schema['properties']['s']['type'] == 'array'


def test_dataframe_passthrough() -> None:
    df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
    m = _DataFrameModel(df=df)
    assert m.df.equals(df)


def test_dataframe_from_records() -> None:
    records = [{'a': 1, 'b': 3}, {'a': 2, 'b': 4}]
    m = _DataFrameModel(df=records)
    assert isinstance(m.df, pd.DataFrame)
    assert m.df.to_dict(orient='records') == records


def test_dataframe_invalid_type() -> None:
    with pytest.raises(ValidationError):
        _DataFrameModel(df=42)


def test_dataframe_json_serialization() -> None:
    df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
    m = _DataFrameModel(df=df)
    dumped = m.model_dump(mode='json')
    assert dumped['df'] == [{'a': 1, 'b': 3}, {'a': 2, 'b': 4}]


def test_dataframe_json_schema() -> None:
    schema = _DataFrameModel.model_json_schema()
    assert schema['properties']['df']['type'] == 'array'
    assert schema['properties']['df']['items']['type'] == 'object'
