"""The `domain_str` module provides the `DomainStr` data type.
This class depends on the `pydantic` package and implements custom validation for domain string format.
"""

from __future__ import annotations

import re
from typing import Any

from pydantic import GetCoreSchemaHandler
from pydantic_core import PydanticCustomError, core_schema


class DomainStr(str):
    """A string subclass with custom validation for domain string format."""

    _domain_re_pattern = (
        r'(?=^.{1,253}$)' r'(^((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.)+' r'([a-zA-Z]{2,63}|xn--[a-zA-Z0-9-]{2,59}(?<!-))$)'
    )

    @classmethod
    def validate(cls, __input_value: Any, /, _: Any) -> str:
        """Validate a domain name from the provided value.

        Args:
            __input_value: The value to be validated.
            _: The source type to be converted.

        Returns:
            str: The parsed domain name.

        """
        return cls._validate(__input_value)

    @classmethod
    def _validate(cls, v: Any) -> DomainStr:
        if not isinstance(v, str):
            raise PydanticCustomError('domain_type', 'Value must be a string')

        v = v.strip()
        if len(v) < 1 or len(v) > 253:
            raise PydanticCustomError('domain_length', 'Domain must be between 1 and 253 characters')

        # Reject non-ASCII input before case folding: Unicode characters such as
        # the Kelvin sign lowercase to ASCII letters and would otherwise be
        # silently converted into a different domain.
        if not v.isascii():
            raise PydanticCustomError('domain_format', 'Invalid domain format')

        v = v.lower()
        if not re.match(cls._domain_re_pattern, v):
            raise PydanticCustomError('domain_format', 'Invalid domain format')

        return cls(v)

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.with_info_before_validator_function(
            cls.validate,
            core_schema.str_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetCoreSchemaHandler
    ) -> dict[str, Any]:
        # Cast the return value to dict[str, Any]
        return dict(handler(schema))
