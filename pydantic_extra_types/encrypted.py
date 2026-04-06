"""The `pydantic_extra_types.encrypted` module provides tools for field-level string transformation.

This can be used to implement automatic encryption/decryption patterns with user-provided callables.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Literal

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import PydanticCustomError, core_schema


@dataclass(frozen=True)
class CipherString:
    """Apply a string transform function either before or after validation.

    `mode='after'` is useful for request-time encryption (validate plaintext, then encrypt).
    `mode='before'` is useful for response-time decryption (decrypt first, then validate).

    ```py
    from typing import Annotated

    from pydantic import BaseModel

    from pydantic_extra_types.encrypted import CipherString


    def encrypt(value: str) -> str:
        return f'enc::{value}'


    def decrypt(value: str) -> str:
        return value.removeprefix('enc::')


    class RequestModel(BaseModel):
        sensitive: Annotated[str, CipherString(encrypt)]


    class ResponseModel(BaseModel):
        sensitive: Annotated[str, CipherString(decrypt, mode='before')]
    ```
    """

    transform: Callable[[str], str]
    """Function used to transform string values."""

    mode: Literal['before', 'after'] = 'after'
    """Apply transform before validation (`before`) or after validation (`after`)."""

    def __post_init__(self) -> None:
        if not callable(self.transform):
            raise ValueError('`transform` must be callable')
        if self.mode not in {'before', 'after'}:
            raise ValueError('`mode` must be either "before" or "after"')

    def _apply(self, value: Any, _: core_schema.ValidationInfo) -> Any:
        if value is None:
            return None
        if not isinstance(value, str):
            raise PydanticCustomError('cipher_string_type', 'Input should be a valid string')

        try:
            transformed = self.transform(value)
        except Exception as exc:  # pragma: no cover
            raise PydanticCustomError('cipher_string_transform', 'Failed to transform value') from exc

        if not isinstance(transformed, str):
            raise PydanticCustomError('cipher_string_result_type', 'Transform function must return a string')
        return transformed

    def __get_pydantic_core_schema__(self, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        schema = handler(source)
        if self.mode == 'before':
            return core_schema.with_info_before_validator_function(self._apply, schema)
        return core_schema.with_info_after_validator_function(self._apply, schema)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> dict[str, Any]:
        return handler(schema)

    @classmethod
    def encrypt(cls, transform: Callable[[str], str]) -> CipherString:
        """Create an encryption-style transformer that runs after validation."""
        return cls(transform=transform, mode='after')

    @classmethod
    def decrypt(cls, transform: Callable[[str], str]) -> CipherString:
        """Create a decryption-style transformer that runs before validation."""
        return cls(transform=transform, mode='before')
