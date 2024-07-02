"""
SemanticVersion definition that is based on the Semantiv Versioning Specification [semver](https://semver.org/).
"""

from typing import Any, Callable

from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema

try:
    import semver
except ModuleNotFoundError as e:  # pragma: no cover
    raise RuntimeError(
        'The `semantic_version` module requires "semver" to be installed. You can install it with "pip install semver".'
    ) from e


class SemanticVersion:
    """
    Semantic version based on the official [semver thread](https://python-semver.readthedocs.io/en/latest/advanced/combine-pydantic-and-semver.html).
    """

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: Callable[[Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:
        def validate_from_str(value: str) -> semver.Version:
            return semver.Version.parse(value)

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
                    core_schema.is_instance_schema(semver.Version),
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
