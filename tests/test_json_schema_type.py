import json

import pytest
from pydantic import BaseModel, ValidationError

from pydantic_extra_types.json_schema import JsonSchema


class JsonSchemaModel(BaseModel):
    json_schema: JsonSchema


def test_json_schema_accepts_dict() -> None:
    input_schema = {'type': 'object', 'properties': {'name': {'type': 'string'}}}
    model = JsonSchemaModel(json_schema=input_schema)

    assert isinstance(model.json_schema, JsonSchema)
    assert model.json_schema == input_schema
    assert model.json_schema is not input_schema


def test_json_schema_accepts_json_string() -> None:
    input_schema = {'type': 'object', 'properties': {'value': {'type': 'integer'}}}
    input_json = json.dumps(input_schema)

    model = JsonSchemaModel(json_schema=input_json)
    assert model.json_schema == input_schema


def test_json_schema_rejects_invalid_json_string() -> None:
    with pytest.raises(ValidationError, match='json_schema_invalid_json'):
        JsonSchemaModel(json_schema='{"type": "object"')


def test_json_schema_rejects_non_object_json() -> None:
    with pytest.raises(ValidationError, match='json_schema_type'):
        JsonSchemaModel(json_schema='["type", "object"]')


def test_json_schema_rejects_invalid_schema() -> None:
    with pytest.raises(ValidationError, match='json_schema_invalid'):
        JsonSchemaModel(json_schema={'type': 'unsupported'})


def test_json_schema_model_dump_serializes_dict() -> None:
    input_schema = {'type': 'object', 'properties': {'x': {'type': 'number'}}}
    model = JsonSchemaModel(json_schema=input_schema)

    assert model.model_dump() == {'json_schema': input_schema}
