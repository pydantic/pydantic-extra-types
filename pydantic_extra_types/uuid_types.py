"""UUID version 6, 7, and 8 types for Pydantic.

Provides UUID version-specific validation types and generation functions.
For UUID generation on Python < 3.14, requires the optional ``uuid-utils`` package.
On Python >= 3.14, uses the standard library ``uuid`` module.

Ref: https://github.com/pydantic/pydantic-extra-types/issues/204
"""

from __future__ import annotations

import sys
import uuid
from datetime import datetime, timezone
from typing import Any, Callable

from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema

_UUID7_TIMESTAMP_BITMASK = (1 << 48) - 1


class _UuidVersion:
    """Marker class to attach version-specific UUID schema to an Annotated type."""

    def __init__(self, version: int) -> None:
        self.version = version

    def __get_pydantic_core_schema__(
        self,
        source_type: type[Any],
        handler: Callable[[Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:
        return core_schema.uuid_schema(version=self.version)  # type: ignore[arg-type]

    def __get_pydantic_json_schema__(
        self,
        _core_schema: core_schema.CoreSchema,
        handler: GetJsonSchemaHandler,
    ) -> JsonSchemaValue:
        return handler(core_schema.uuid_schema(version=self.version))  # type: ignore[arg-type]

    def __repr__(self) -> str:
        return f'UuidVersion(uuid_version={self.version})'

    def __hash__(self) -> int:
        return hash(self.version)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, _UuidVersion):
            return self.version == other.version
        return NotImplemented


if sys.version_info >= (3, 9):
    from typing import Annotated
else:
    from typing_extensions import Annotated  # pragma: no cover


UUID6 = Annotated[uuid.UUID, _UuidVersion(6)]
"""A UUID that must be version 6 (reordered time-based).

```py
from pydantic import BaseModel

from pydantic_extra_types.uuid_types import UUID6


class Model(BaseModel):
    id: UUID6


m = Model(id='1ef21d2f-6aa3-6d00-a327-541a2bda5190')
print(m.id)
# > 1ef21d2f-6aa3-6d00-a327-541a2bda5190
print(m.id.version)
# > 6
```
"""

UUID7 = Annotated[uuid.UUID, _UuidVersion(7)]
"""A UUID that must be version 7 (Unix Epoch time-based, sortable).

UUIDv7 embeds a Unix timestamp in milliseconds in the high 48 bits,
making it naturally sortable by creation time.

```py
from pydantic import BaseModel

from pydantic_extra_types.uuid_types import UUID7


class Document(BaseModel):
    id: UUID7


doc = Document(id='018f0e8c-7a6a-7b1c-a3e4-fdf3e0ef7a4a')
print(doc.id)
# > 018f0e8c-7a6a-7b1c-a3e4-fdf3e0ef7a4a
print(doc.id.version)
# > 7
```
"""

UUID8 = Annotated[uuid.UUID, _UuidVersion(8)]
"""A UUID that must be version 8 (custom/experimental).

```py
from pydantic import BaseModel

from pydantic_extra_types.uuid_types import UUID8


class Model(BaseModel):
    id: UUID8
```
"""


def uuid7() -> uuid.UUID:
    """Generate a new UUID version 7.

    Uses the standard library ``uuid.uuid7()`` on Python 3.14+.
    On older Python versions, uses the ``uuid-utils`` package.

    Returns:
        A new UUID version 7 instance.

    Raises:
        ImportError: If running on Python < 3.14 and ``uuid-utils`` is not installed.

    ```py
    from pydantic_extra_types.uuid_types import uuid7

    new_id = uuid7()
    print(new_id)
    # > 018f0e8c-7a6a-7b1c-a3e4-fdf3e0ef7a4a  (example)
    print(new_id.version)
    # > 7
    ```
    """
    if sys.version_info >= (3, 14):
        return uuid.uuid7()
    else:  # pragma: no cover
        try:
            import uuid_utils

            return uuid.UUID(str(uuid_utils.uuid7()))
        except ModuleNotFoundError as e:
            raise ImportError(
                'Generating UUID v7 on Python < 3.14 requires the "uuid-utils" package. '
                'Install it with: pip install uuid-utils'
            ) from e


def uuid7_to_datetime(value: uuid.UUID) -> datetime:
    """Extract the datetime from a UUID version 7.

    UUIDv7 encodes a Unix timestamp in milliseconds in the high 48 bits.

    Args:
        value: A UUID version 7 instance.

    Returns:
        A timezone-aware datetime (UTC) corresponding to the embedded timestamp.

    Raises:
        ValueError: If the UUID is not version 7.

    ```py
    import uuid

    from pydantic_extra_types.uuid_types import uuid7_to_datetime

    u = uuid.UUID('018f0e8c-7a6a-7b1c-a3e4-fdf3e0ef7a4a')
    print(uuid7_to_datetime(u))
    # > 2024-04-25 23:07:27.818000+00:00
    ```
    """
    if value.version != 7:
        raise ValueError(f'Expected UUID version 7, got version {value.version}')

    timestamp_ms = value.int >> 80 & _UUID7_TIMESTAMP_BITMASK
    return datetime.fromtimestamp(timestamp_ms / 1000.0, tz=timezone.utc)
