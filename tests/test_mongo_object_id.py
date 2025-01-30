"""Tests for the mongo_object_id module."""

import pytest
from pydantic import BaseModel, GetCoreSchemaHandler, ValidationError
from pydantic.json_schema import JsonSchemaMode

from pydantic_extra_types.mongo_object_id import MongoObjectId


class MongoDocument(BaseModel):
    object_id: MongoObjectId


@pytest.mark.parametrize(
    'object_id, result, valid',
    [
        # Valid ObjectId for str format
        ('611827f2878b88b49ebb69fc', '611827f2878b88b49ebb69fc', True),
        ('611827f2878b88b49ebb69fd', '611827f2878b88b49ebb69fd', True),
        # Invalid ObjectId for str format
        ('611827f2878b88b49ebb69f', None, False),  # Invalid ObjectId (short length)
        ('611827f2878b88b49ebb69fca', None, False),  # Invalid ObjectId (long length)
        # Valid ObjectId for bytes format
    ],
)
def test_format_for_object_id(object_id: str, result: str, valid: bool) -> None:
    """Test the MongoObjectId validation."""
    if valid:
        assert str(MongoDocument(object_id=object_id).object_id) == result
    else:
        with pytest.raises(ValidationError):
            MongoDocument(object_id=object_id)
        with pytest.raises(
            ValueError,
            match=f"Invalid ObjectId {object_id} has to be 24 characters long and in the format '5f9f2f4b9d3c5a7b4c7e6c1d'.",
        ):
            MongoObjectId.validate(object_id)


@pytest.mark.parametrize(
    'schema_mode',
    [
        'validation',
        'serialization',
    ],
)
def test_json_schema(schema_mode: JsonSchemaMode) -> None:
    """Test the MongoObjectId model_json_schema implementation."""
    expected_json_schema = {
        'properties': {
            'object_id': {
                'maxLength': MongoObjectId.OBJECT_ID_LENGTH,
                'minLength': MongoObjectId.OBJECT_ID_LENGTH,
                'title': 'Object Id',
                'type': 'string',
            }
        },
        'required': ['object_id'],
        'title': 'MongoDocument',
        'type': 'object',
    }
    assert MongoDocument.model_json_schema(mode=schema_mode) == expected_json_schema


def test_get_pydantic_core_schema() -> None:
    """Test the __get_pydantic_core_schema__ method override."""
    schema = MongoObjectId.__get_pydantic_core_schema__(MongoObjectId, GetCoreSchemaHandler())
    assert isinstance(schema, dict)
    assert 'json_schema' in schema
    assert 'python_schema' in schema
    assert schema['json_schema']['type'] == 'str'
