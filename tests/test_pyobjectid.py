import pytest
from pydantic import BaseModel, ValidationError

from pydantic_extra_types.mongo_objectId import ObjectIdField


class Something(BaseModel):
    object_id: ObjectIdField


@pytest.mark.parametrize(
    "object_id, result, valid",
    [
        # Valid ObjectId for str format
        ("611827f2878b88b49ebb69fc", "611827f2878b88b49ebb69fc", True),
        ("611827f2878b88b49ebb69fd", "611827f2878b88b49ebb69fd", True),
        # Invalid ObjectId for str format
        ("611827f2878b88b49ebb69f", None, False),  # Invalid ObjectId (short length)
        ("611827f2878b88b49ebb69fca", None, False),  # Invalid ObjectId (long length)
        # Valid ObjectId for bytes format
    ],
)
def test_format_for_object_id(object_id, result, valid):
    if valid:
        assert str(Something(object_id=object_id).object_id) == result
    else:
        with pytest.raises(ValidationError):
            Something(object_id=object_id)


def test_json_schema():
    assert Something.model_json_schema(mode="validation") == {
        "properties": {"object_id": {"title": "Object Id", "type": "string"}},
        "required": ["object_id"],
        "title": "Something",
        "type": "object",
    }
    assert Something.model_json_schema(mode="serialization") == {
        "properties": {
            "object_id": {
                "anyOf": [{"type": "string"}],
                "title": "Object Id",
            }
        },
        "required": ["object_id"],
        "title": "Something",
        "type": "object",
    }
