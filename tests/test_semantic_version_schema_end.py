import pytest
from jsonschema import Draft202012Validator
from pydantic import TypeAdapter, ValidationError

from pydantic_extra_types.semantic_version import SemanticVersion


@pytest.mark.parametrize('version', ['1.2.3', '0.0.0-alpha.1+build.2'])
@pytest.mark.parametrize('suffix', ['', '\n', '\r', '\r\n', '\u2028', '\u2029'])
def test_semantic_version_schema_requires_the_complete_string(version: str, suffix: str) -> None:
    adapter = TypeAdapter(SemanticVersion)
    value = version + suffix
    validator = Draft202012Validator(adapter.json_schema())

    if suffix:
        with pytest.raises(ValidationError):
            adapter.validate_python(value)
        assert not validator.is_valid(value)
    else:
        assert str(adapter.validate_python(value)) == version
        validator.validate(value)
