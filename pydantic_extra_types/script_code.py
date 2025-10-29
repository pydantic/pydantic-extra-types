"""script definitions that are based on the [ISO 15924](https://en.wikipedia.org/wiki/ISO_15924)"""

from __future__ import annotations

from typing import Any

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import PydanticCustomError, core_schema

try:
    import pycountry
except ModuleNotFoundError as e:  # pragma: no cover
    raise RuntimeError(
        'The `script_code` module requires "pycountry" to be installed.'
        ' You can install it with "pip install pycountry".'
    ) from e


class ISO_15924(str):
    """ISO_15924 parses script in the [ISO 15924](https://en.wikipedia.org/wiki/ISO_15924)
    format.

    ```py
    from pydantic import BaseModel

    from pydantic_extra_types.script_code import ISO_15924


    class Script(BaseModel):
        alpha_4: ISO_15924


    script = Script(alpha_4='Java')
    print(lang)
    # > script='Java'
    ```
    """

    allowed_values_list = [script.alpha_4 for script in pycountry.scripts]
    allowed_values = set(allowed_values_list)

    @classmethod
    def _validate(cls, __input_value: str, _: core_schema.ValidationInfo) -> ISO_15924:
        """Validate a ISO 15924 language code from the provided str value.

        Args:
            __input_value: The str value to be validated.
            _: The Pydantic ValidationInfo.

        Returns:
            The validated ISO 15924 script code.

        Raises:
            PydanticCustomError: If the ISO 15924 script code is not valid.
        """
        if __input_value not in cls.allowed_values:
            raise PydanticCustomError(
                'ISO_15924', 'Invalid ISO 15924 script code. See https://en.wikipedia.org/wiki/ISO_15924'
            )
        return cls(__input_value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, _: type[Any], __: GetCoreSchemaHandler
    ) -> core_schema.AfterValidatorFunctionSchema:
        """Return a Pydantic CoreSchema with the ISO 639-3 language code validation.

        Args:
            _: The source type.
            __: The handler to get the CoreSchema.

        Returns:
            A Pydantic CoreSchema with the ISO 639-3 language code validation.

        """
        return core_schema.with_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(min_length=4, max_length=4),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> dict[str, Any]:
        """Return a Pydantic JSON Schema with the ISO 639-3 language code validation.

        Args:
            schema: The Pydantic CoreSchema.
            handler: The handler to get the JSON Schema.

        Returns:
            A Pydantic JSON Schema with the ISO 639-3 language code validation.

        """
        json_schema = handler(schema)
        json_schema.update({'enum': cls.allowed_values_list})
        return json_schema
