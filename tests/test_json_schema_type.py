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


@pytest.mark.parametrize('as_json_string', [False, True])
@pytest.mark.parametrize(
    'input_schema',
    [
        {
            '$schema': 'http://json-schema.org/draft-07/schema#',
            'type': 'array',
            'items': [{'type': 'string'}, {'type': 'integer'}],
        },
        {
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': 'number',
            'minimum': 0,
            'exclusiveMinimum': True,
        },
    ],
)
def test_json_schema_uses_declared_draft(input_schema, as_json_string) -> None:
    value = json.dumps(input_schema) if as_json_string else input_schema

    assert JsonSchemaModel(json_schema=value).json_schema == input_schema


def test_json_schema_rejects_invalid_declared_draft_schema() -> None:
    with pytest.raises(ValidationError, match='json_schema_invalid'):
        JsonSchemaModel(
            json_schema={
                '$schema': 'http://json-schema.org/draft-07/schema#',
                'items': [{'type': 'unsupported'}],
            }
        )


def test_json_schema_defaults_to_draft_2020_12() -> None:
    with pytest.raises(ValidationError, match='json_schema_invalid'):
        JsonSchemaModel(json_schema={'items': [{'type': 'string'}]})


def test_json_schema_model_dump_serializes_dict() -> None:
    input_schema = {'type': 'object', 'properties': {'x': {'type': 'number'}}}
    model = JsonSchemaModel(json_schema=input_schema)

    assert model.model_dump() == {'json_schema': input_schema}
