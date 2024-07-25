import pytest
from pydantic import BaseModel

from pydantic_extra_types.semver import _VersionPydanticAnnotation


class SomethingWithAVersion(BaseModel):
    version: _VersionPydanticAnnotation


def test_valid_semver() -> None:
    SomethingWithAVersion(version='1.2.3')


def test_valid_semver_with_prerelease() -> None:
    SomethingWithAVersion(version='1.2.3-alpha.1')


def test_invalid_semver() -> None:
    with pytest.raises(ValueError):
        SomethingWithAVersion(version='jim.was.here')
