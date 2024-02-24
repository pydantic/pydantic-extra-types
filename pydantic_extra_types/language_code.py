from __future__ import annotations

from typing import Any

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import PydanticCustomError, core_schema

try:
    import pycountry
except ModuleNotFoundError:  # pragma: no cover
    raise RuntimeError(
        'The `language_code` module requires "pycountry" to be installed.'
        ' You can install it with "pip install pycountry".'
    )


class ISO639_3(str):
    # noinspection PyUnresolvedReferences
    allowed_values_list = [lang.alpha_3 for lang in pycountry.languages]
    allowed_values = set(allowed_values_list)

    @classmethod
    def _validate(cls, __input_value: str, _: core_schema.ValidationInfo) -> ISO639_3:
        if __input_value not in cls.allowed_values:
            raise PydanticCustomError(
                'ISO649_3', 'Invalid ISO 639-3 language code. See https://en.wikipedia.org/wiki/ISO_639-3'
            )
        return cls(__input_value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, _: type[Any], __: GetCoreSchemaHandler
    ) -> core_schema.AfterValidatorFunctionSchema:
        return core_schema.with_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(min_length=3, max_length=3),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> dict[str, Any]:
        json_schema = handler(schema)
        json_schema.update({'enum': cls.allowed_values_list})
        return json_schema


class ISO639_5(str):
    # noinspection PyUnresolvedReferences
    allowed_values_list = [lang.alpha_3 for lang in pycountry.language_families]
    allowed_values_list.sort()
    allowed_values = set(allowed_values_list)

    @classmethod
    def _validate(cls, __input_value: str, _: core_schema.ValidationInfo) -> ISO639_5:
        if __input_value not in cls.allowed_values:
            raise PydanticCustomError(
                'ISO649_5', 'Invalid ISO 639-5 language code. See https://en.wikipedia.org/wiki/ISO_639-5'
            )
        return cls(__input_value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, _: type[Any], __: GetCoreSchemaHandler
    ) -> core_schema.AfterValidatorFunctionSchema:
        return core_schema.with_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(min_length=3, max_length=3),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> dict[str, Any]:
        json_schema = handler(schema)
        json_schema.update({'enum': cls.allowed_values_list})
        return json_schema
