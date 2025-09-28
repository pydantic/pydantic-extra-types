"""The `pydantic_extra_types.s3` module provides the
[`S3Path`][pydantic_extra_types.s3.S3Path] data type.

A simpleAWS S3 URLs parser.
It also provides the `Bucket`, `Key` component.
"""

from __future__ import annotations

import re
from typing import Any, ClassVar

from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema


class S3Path(str):
    """An object representing a valid S3 path.
    This type also allows you to access the `bucket` and `key` component of the S3 path.
    It also contains the `last_key` which represents the last part of the path (typically a file).

    ```python
    from pydantic import BaseModel
    from pydantic_extra_types.s3 import S3Path


    class TestModel(BaseModel):
        path: S3Path


    p = 's3://my-data-bucket/2023/08/29/sales-report.csv'
    model = TestModel(path=p)
    model

    # > TestModel(path=S3Path('s3://my-data-bucket/2023/08/29/sales-report.csv'))

    model.path.bucket

    # > 'my-data-bucket'
    ```
    """

    patt: ClassVar[str] = r'^s3://([^/]+)/(.*?([^/]+)/?)$'

    def __init__(self, value: str) -> None:
        self.value = value
        groups: tuple[str, str, str] = re.match(self.patt, self.value).groups()  # type: ignore
        self.bucket: str = groups[0]
        self.key: str = groups[1]
        self.last_key: str = groups[2]

    def __str__(self) -> str:  # pragma: no cover
        return self.value

    def __repr__(self) -> str:  # pragma: no cover
        return f'{self.__class__.__name__}({self.value!r})'

    @classmethod
    def _validate(cls, __input_value: str, _: core_schema.ValidationInfo) -> S3Path:
        return cls(__input_value)

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        _, _ = source, handler
        return core_schema.with_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(pattern=cls.patt),
            field_name=cls.__class__.__name__,
        )
