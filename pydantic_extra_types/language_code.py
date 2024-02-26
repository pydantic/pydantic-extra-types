"""
Language definitions that are based on the [ISO 639-3](https://en.wikipedia.org/wiki/ISO_639-3) & [ISO 639-5](https://en.wikipedia.org/wiki/ISO_639-5).
"""
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
    """ISO639_3 parses Language in the [ISO 639-3 alpha-3](https://en.wikipedia.org/wiki/ISO_639-3_alpha-3)
    format.

    ```py
    from pydantic import BaseModel

    from pydantic_extra_types.language_code import ISO639_3

    class Language(BaseModel):
        alpha_3: ISO639_3

    lang = Language(alpha_3='ssr')
    print(lang)
    # > alpha_3='ssr'
    ```
    """

    allowed_values_list = [lang.alpha_3 for lang in pycountry.languages]
    allowed_values = set(allowed_values_list)

    @classmethod
    def _validate(cls, __input_value: str, _: core_schema.ValidationInfo) -> ISO639_3:
        """
        Validate a ISO 639-3 language code from the provided str value.

        Args:
            __input_value: The str value to be validated.
            _: The Pydantic ValidationInfo.

        Returns:
            The validated ISO 639-3 language code.

        Raises:
            PydanticCustomError: If the ISO 639-3 language code is not valid.
        """
        if __input_value not in cls.allowed_values:
            raise PydanticCustomError(
                'ISO649_3', 'Invalid ISO 639-3 language code. See https://en.wikipedia.org/wiki/ISO_639-3'
            )
        return cls(__input_value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, _: type[Any], __: GetCoreSchemaHandler
    ) -> core_schema.AfterValidatorFunctionSchema:
        """
        Return a Pydantic CoreSchema with the ISO 639-3 language code validation.

        Args:
            _: The source type.
            __: The handler to get the CoreSchema.

        Returns:
            A Pydantic CoreSchema with the ISO 639-3 language code validation.

        """
        return core_schema.with_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(min_length=3, max_length=3),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> dict[str, Any]:
        """
        Return a Pydantic JSON Schema with the ISO 639-3 language code validation.

        Args:
            schema: The Pydantic CoreSchema.
            handler: The handler to get the JSON Schema.

        Returns:
            A Pydantic JSON Schema with the ISO 639-3 language code validation.

        """
        json_schema = handler(schema)
        json_schema.update({'enum': cls.allowed_values_list})
        return json_schema


class ISO639_5(str):
    """ISO639_5 parses Language in the [ISO 639-5 alpha-3](https://en.wikipedia.org/wiki/ISO_639-5_alpha-3)
    format.

    ```py
    from pydantic import BaseModel

    from pydantic_extra_types.language_code import ISO639_5

    class Language(BaseModel):
        alpha_3: ISO639_5

    lang = Language(alpha_3='gem')
    print(lang)
    # > alpha_3='gem'
    ```
    """

    allowed_values_list = [lang.alpha_3 for lang in pycountry.language_families]
    allowed_values_list.sort()
    allowed_values = set(allowed_values_list)

    @classmethod
    def _validate(cls, __input_value: str, _: core_schema.ValidationInfo) -> ISO639_5:
        """
        Validate a ISO 639-5 language code from the provided str value.

        Args:
            __input_value: The str value to be validated.
            _: The Pydantic ValidationInfo.

        Returns:
            The validated ISO 639-3 language code.

        Raises:
            PydanticCustomError: If the ISO 639-5 language code is not valid.
        """
        if __input_value not in cls.allowed_values:
            raise PydanticCustomError(
                'ISO649_5', 'Invalid ISO 639-5 language code. See https://en.wikipedia.org/wiki/ISO_639-5'
            )
        return cls(__input_value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, _: type[Any], __: GetCoreSchemaHandler
    ) -> core_schema.AfterValidatorFunctionSchema:
        """
        Return a Pydantic CoreSchema with the ISO 639-5 language code validation.

        Args:
            _: The source type.
            __: The handler to get the CoreSchema.

        Returns:
            A Pydantic CoreSchema with the ISO 639-5 language code validation.

        """
        return core_schema.with_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(min_length=3, max_length=3),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> dict[str, Any]:
        """
        Return a Pydantic JSON Schema with the ISO 639-5 language code validation.

        Args:
            schema: The Pydantic CoreSchema.
            handler: The handler to get the JSON Schema.

        Returns:
            A Pydantic JSON Schema with the ISO 639-5 language code validation.

        """
        json_schema = handler(schema)
        json_schema.update({'enum': cls.allowed_values_list})
        return json_schema
