"""
The `pydantic_extra_types.ULID` module provides the [`ULID`] data type.

This class depends on the [python-ulid] package, which is a validate by the [ULID-spec](https://github.com/ulid/spec#implementations-in-other-languages).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Union

from pydantic import GetCoreSchemaHandler
from pydantic._internal import _repr
from pydantic_core import PydanticCustomError, core_schema

try:
    from ulid import ULID as _ULID
except ModuleNotFoundError as e:  # pragma: no cover
    raise RuntimeError(
        'The `ulid` module requires "python-ulid" to be installed. You can install it with "pip install python-ulid".'
    ) from e

UlidType = Union[str, bytes, int]


@dataclass
class ULID(_repr.Representation):
    """
    A wrapper around [python-ulid](https://pypi.org/project/python-ulid/) package, which
    is a validate by the [ULID-spec](https://github.com/ulid/spec#implementations-in-other-languages).
    """

    ulid: _ULID

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.no_info_wrap_validator_function(
            cls._validate_ulid,
            core_schema.union_schema(
                [
                    core_schema.is_instance_schema(_ULID),
                    core_schema.int_schema(),
                    core_schema.bytes_schema(),
                    core_schema.str_schema(),
                ]
            ),
        )

    @classmethod
    def _validate_ulid(cls, value: Any, handler: core_schema.ValidatorFunctionWrapHandler) -> Any:
        ulid: _ULID
        try:
            if isinstance(value, int):
                ulid = _ULID.from_int(value)
            elif isinstance(value, str):
                ulid = _ULID.from_str(value)
            elif isinstance(value, _ULID):
                ulid = value
            else:
                ulid = _ULID.from_bytes(value)
        except ValueError as e:
            raise PydanticCustomError('ulid_format', 'Unrecognized format') from e
        return handler(ulid)
