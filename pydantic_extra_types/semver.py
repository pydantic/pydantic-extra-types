"""
The SemVer module provides functionality to parse and validate Semantic Versioning (SemVer) strings.

This class depends on the [semver](https://python-semver.readthedocs.io/en/latest/index.html) package.
"""

try:
    from semver import Version
except ModuleNotFoundError as e:  # pragma: no cover
    raise RuntimeError(
        '`SemVer` requires "semver" to be installed. You can install it with "pip install semver"'
    ) from e


class SemVer(Version):
    """
    Represents a Semantic Versioning (SemVer).

    This is a wrapper around the [`semver.Version`](https://python-semver.readthedocs.io/en/latest/index.html) class.
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.parse

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")
