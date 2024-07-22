"""
The SemVer module provides functionality to parse and validate Semantic Versioning (SemVer) strings.

This class depends on the [semver](https://python-semver.readthedocs.io/en/latest/index.html) package.
"""

from typing import Annotated, Any, Callable
from pydantic import GetJsonSchemaHandler
from pydantic_core import core_schema
from pydantic.json_schema import JsonSchemaValue
from semver import Version


class _VersionPydanticAnnotation(Version):
    """
    Represents a Semantic Versioning (SemVer).

    Warps the `version` type from `semver`.
    """

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: Callable[[Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:
        def validate_from_str(value: str) -> Version:
            return Version.parse(value)

        from_str_schema = core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(validate_from_str),
            ]
        )

        return core_schema.json_or_python_schema(
            json_schema=from_str_schema,
            python_schema=core_schema.union_schema(
                [
                    core_schema.is_instance_schema(Version),
                    from_str_schema,
                ]
            ),
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return handler(core_schema.str_schema())


ManifestVersion = Annotated[Version, _VersionPydanticAnnotation]
