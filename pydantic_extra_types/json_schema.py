"""The `pydantic_extra_types.json_schema` module provides the
[`JsonSchema`][pydantic_extra_types.json_schema.JsonSchema] data type.
"""

from __future__ import annotations

import json
from copy import deepcopy
from typing import Any

from pydantic import GetCoreSchemaHandler
from pydantic_core import PydanticCustomError, core_schema

try:
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import SchemaError
except ModuleNotFoundError as e:  # pragma: no cover
    raise RuntimeError(
        'The `json_schema` module requires "jsonschema" to be installed. You can install it with "pip install jsonschema".'
    ) from e


class JsonSchema(dict[str, Any]):
    """A JSON Schema validated via [`jsonschema`](https://pypi.org/project/jsonschema/).

    ```py
    from pydantic import BaseModel

    from pydantic_extra_types.json_schema import JsonSchema


    class ToolDefinition(BaseModel):
        input_schema: JsonSchema


    tool = ToolDefinition(input_schema='{"type": "object", "properties": {"name": {"type": "string"}}}')
    print(tool.input_schema)
    # > {'type': 'object', 'properties': {'name': {'type': 'string'}}}
    ```
    """

    @classmethod
    def _validate(cls, __input_value: str | dict[str, Any], _: core_schema.ValidationInfo) -> JsonSchema:
        if isinstance(__input_value, str):
            try:
                schema = json.loads(__input_value)
            except json.JSONDecodeError as exc:
                raise PydanticCustomError('json_schema_invalid_json', 'Input string must be valid JSON') from exc
        else:
            schema = __input_value

        if not isinstance(schema, dict):
            raise PydanticCustomError('json_schema_type', 'JSON Schema must be a JSON object')

        try:
            Draft202012Validator.check_schema(schema)
        except SchemaError as exc:
            raise PydanticCustomError(
                'json_schema_invalid',
                'Input must be a valid JSON Schema: {reason}',
                {'reason': exc.message},
            ) from exc

        return cls(deepcopy(schema))

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source: type[Any],
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        return core_schema.with_info_after_validator_function(
            cls._validate,
            core_schema.union_schema(
                [
                    core_schema.str_schema(),
                    core_schema.dict_schema(
                        keys_schema=core_schema.str_schema(strict=True),
                        values_schema=core_schema.any_schema(),
                    ),
                ]
            ),
        )
