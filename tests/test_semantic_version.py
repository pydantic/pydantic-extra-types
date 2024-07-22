import pytest
from pydantic import BaseModel, ValidationError

from pydantic_extra_types.semantic_version import SemanticVersion


@pytest.fixture(scope='module', name='SemanticVersionObject')
def application_object_fixture():
    class Application(BaseModel):
        version: SemanticVersion

    return Application


def test_valid_semantic_version(SemanticVersionObject):
    application = SemanticVersionObject(version='1.0.0')
    assert application.version
    assert application.model_dump() == {'version': '1.0.0'}


def test_invalid_semantic_version(SemanticVersionObject):
    with pytest.raises(ValidationError):
        SemanticVersionObject(version='Peter Maffay')
