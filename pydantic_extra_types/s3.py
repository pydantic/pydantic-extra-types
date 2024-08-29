"""
The `pydantic_extra_types.s3` module provides the
[`S3Path`][pydantic_extra_types.s3.S3Path] data type.

A simpleAWS S3 URLs parser.
It also provides the `Bucket`, `Key` component.
"""

import re
from typing import Any, ClassVar, Type

from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema


class S3Path(str):
    patt: ClassVar[str] = r'^s3://([^/]+)/(.*?([^/]+)/?)$'

    def __init__(self, value: str) -> None:
        self.value = value
        self.bucket, self.key, self.last_key = re.match(self.patt, self.value).groups()

    def __str__(self) -> str:  # pragma: no cover
        return self.value

    def __repr__(self) -> str:  # pragma: no cover
        return f'{self.__class__.__name__}({self.value!r})'

    @classmethod
    def _validate(cls, __input_value: str, _: core_schema.ValidationInfo) -> 'S3Path':
        return cls(__input_value)

    @classmethod
    def __get_pydantic_core_schema__(cls, source: Type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        _, _ = source, handler
        return core_schema.with_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(pattern=cls.patt),
            field_name=cls.__class__.__name__,
        )
