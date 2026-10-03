"""The `pydantic_extra_types.sha256` module provides the `Sha256Str` data type.

A SHA-256 digest is 32 bytes long and is usually written as 64 hexadecimal characters,
like the output of `hashlib.sha256(...).hexdigest()` or `sha256sum`.
"""

from __future__ import annotations

from typing import Any

from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema


class Sha256Str(str):
    """A hex-encoded SHA-256 digest, normalized to lowercase.

    ```py
    from pydantic import BaseModel

    from pydantic_extra_types.sha256 import Sha256Str


    class Artifact(BaseModel):
        checksum: Sha256Str


    artifact = Artifact(checksum='E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855')
    print(artifact)
    # > checksum='e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
    ```
    """

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        """Return a Pydantic CoreSchema with the SHA-256 digest validation.

        Args:
            source: The source type to be converted.
            handler: The handler to get the CoreSchema.

        Returns:
            A Pydantic CoreSchema with the SHA-256 digest validation.
        """
        return core_schema.no_info_after_validator_function(
            cls,
            core_schema.str_schema(pattern=r'^[0-9a-fA-F]{64}$', strip_whitespace=True, to_lower=True),
        )
