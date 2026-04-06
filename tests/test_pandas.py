import pandas as pd
import pytest
from pydantic import BaseModel, ValidationError

from pydantic_extra_types.pandas import DataFrame, Series


class SeriesModel(BaseModel):
    values: Series


class DataFrameModel(BaseModel):
    table: DataFrame


def test_series_from_list() -> None:
    model = SeriesModel(values=[1, 2, 3])

    assert isinstance(model.values, pd.Series)
    assert model.values.tolist() == [1, 2, 3]


def test_series_from_series() -> None:
    input_series = pd.Series([1, 2, 3])
    model = SeriesModel(values=input_series)

    assert isinstance(model.values, pd.Series)
    assert model.values.tolist() == [1, 2, 3]


def test_series_rejects_invalid_input() -> None:
    with pytest.raises(ValidationError):
        SeriesModel(values='not-a-series')


def test_dataframe_from_records() -> None:
    model = DataFrameModel(table=[{'name': 'alice'}, {'name': 'bob'}])

    assert isinstance(model.table, pd.DataFrame)
    assert model.table.to_dict(orient='records') == [{'name': 'alice'}, {'name': 'bob'}]


def test_dataframe_from_columnar_dict() -> None:
    model = DataFrameModel(table={'name': ['alice', 'bob']})

    assert isinstance(model.table, pd.DataFrame)
    assert model.table.to_dict(orient='records') == [{'name': 'alice'}, {'name': 'bob'}]


def test_dataframe_from_dataframe() -> None:
    input_dataframe = pd.DataFrame([{'name': 'alice'}, {'name': 'bob'}])
    model = DataFrameModel(table=input_dataframe)

    assert isinstance(model.table, pd.DataFrame)
    assert model.table.to_dict(orient='records') == [{'name': 'alice'}, {'name': 'bob'}]


def test_dataframe_rejects_invalid_input() -> None:
    with pytest.raises(ValidationError):
        DataFrameModel(table=[1, 2, 3])


def test_series_json_schema() -> None:
    assert SeriesModel.model_json_schema() == {
        'properties': {'values': {'items': {}, 'title': 'Values', 'type': 'array'}},
        'required': ['values'],
        'title': 'SeriesModel',
        'type': 'object',
    }


def test_dataframe_json_schema() -> None:
    assert DataFrameModel.model_json_schema() == {
        'properties': {
            'table': {
                'anyOf': [
                    {'items': {'additionalProperties': True, 'type': 'object'}, 'type': 'array'},
                    {'additionalProperties': {'items': {}, 'type': 'array'}, 'type': 'object'},
                ],
                'title': 'Table',
            }
        },
        'required': ['table'],
        'title': 'DataFrameModel',
        'type': 'object',
    }


def test_json_serialization() -> None:
    model = DataFrameModel(table=[{'name': 'alice'}, {'name': 'bob'}])

    assert model.model_dump_json() == '{"table":[{"name":"alice"},{"name":"bob"}]}'
