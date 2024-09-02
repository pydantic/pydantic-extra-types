import pytest
from pydantic import BaseModel, ValidationError

from pydantic_extra_types.semantic_version import SemanticVersion


@pytest.fixture(scope='module', name='SemanticVersionObject')
def application_object_fixture():
    class Application(BaseModel):
        version: SemanticVersion

    return Application


@pytest.mark.parametrize('version', ['1.0.0', '1.0.0-alpha.1', '1.0.0-alpha.1+build.1', '1.2.3'])
def test_valid_semantic_version(SemanticVersionObject, version):
    application = SemanticVersionObject(version=version)
    assert application.version
    assert application.model_dump() == {'version': version}


@pytest.mark.parametrize('invalid_version', ['no dots string', 'with.dots.string', ''])
def test_invalid_semantic_version(SemanticVersionObject, invalid_version):
    with pytest.raises(ValidationError):
        SemanticVersionObject(version=invalid_version)
