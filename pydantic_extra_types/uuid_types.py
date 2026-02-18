"""The `pydantic_extra_types.uuid_types` module provides UUID version 6, 7, and 8 types."""

from __future__ import annotations

import sys
import uuid
from datetime import datetime, timezone
from typing import Annotated, Any, Callable

from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema

_UUID7_TIMESTAMP_BITMASK = (1 << 48) - 1


class _UuidVersion:
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

    On Python 3.14+, uses ``uuid.uuid7()`` from the standard library.
    On older versions, requires the ``uuid-utils`` package.
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
    """Extract the embedded datetime from a UUID version 7.

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
