"""The `pydantic_extra_types.jwt` module provides the [`JWTStr`][pydantic_extra_types.jwt.JWTStr] data type.

This class depends on the `pydantic` package and implements structural validation of JWT format (RFC 7519). It does not verify the cryptographic signature.
"""

from __future__ import annotations

import base64
import binascii
import json
from typing import Any, cast

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import PydanticCustomError, core_schema


class JWTStr(str):
    """A string subclass with structural validation for JWT (JSON Web Token) format.

        ## Examples
    ```python
        from pydantic import BaseModel

        from pydantic_extra_types.jwt import JWTStr


        class Auth(BaseModel):
            token: JWTStr


        auth = Auth(token='eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dGVzdA')
        print(auth.token.header)
        #> {'alg': 'HS256'}
        print(auth.token.payload)
        #> {'sub': '1234567890'}
        print(auth.token.signature)
        #> b'test'
    ```
    """

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.with_info_after_validator_function(cls.validate, core_schema.str_schema())

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> dict[str, Any]:
        json_schema = handler(schema)
        json_schema.update(
            {'type': 'string', 'format': 'jwt', 'examples': ['eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dGVzdA']}
        )
        return json_schema

    def __new__(cls, value: Any) -> JWTStr:
        cls._validate(value)
        return cast('JWTStr', super().__new__(cls, value))

    @classmethod
    def validate(cls, value: Any, _: core_schema.ValidationInfo) -> JWTStr:
        """Validate and construct a JWTStr from the provided value."""
        return cls(value)

    @classmethod
    def _validate(cls, value: Any) -> None:
        if not isinstance(value, str):
            raise PydanticCustomError('jwt_type', 'Value must be a string')

        parts = value.split('.')
        if len(parts) != 3:
            raise PydanticCustomError(
                'jwt_format', 'Value must include header, payload, and signature separated by dots'
            )

        try:
            header_bytes = cls._decode_segment(parts[0])
            payload_bytes = cls._decode_segment(parts[1])
            cls._decode_segment(parts[2])  # signature
        except (ValueError, binascii.Error):
            raise PydanticCustomError('jwt_format', 'Headers, payload and signature must be valid urlsafe base64')

        try:
            header = json.loads(header_bytes.decode())
            payload = json.loads(payload_bytes.decode())
        except (json.JSONDecodeError, UnicodeDecodeError):
            raise PydanticCustomError('jwt_format', 'Header and payload must be valid JSON')

        if not isinstance(header, dict):
            raise PydanticCustomError('jwt_type', 'Header must be a JSON object')
        if not isinstance(payload, dict):
            raise PydanticCustomError('jwt_type', 'Payload must be a JSON object')

        alg = header.get('alg')
        if not alg or not isinstance(alg, str):
            raise PydanticCustomError('jwt_format', 'Header must contain non-empty alg')

    @property
    def header(self) -> dict[str, Any]:
        """Return the decoded JWT header."""
        return json.loads(self._decode_segment(self.split('.')[0]).decode())

    @property
    def payload(self) -> dict[str, Any]:
        """Return the decoded JWT payload."""
        return json.loads(self._decode_segment(self.split('.')[1]).decode())

    @property
    def signature(self) -> bytes:
        """Return the raw JWT signature bytes."""
        return self._decode_segment(self.split('.')[2])

    @staticmethod
    def _decode_segment(segment: str) -> bytes:
        padded = segment + '=' * (-len(segment) % 4)
        return base64.b64decode(padded, altchars=b'-_', validate=True)
