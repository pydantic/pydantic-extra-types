from dataclasses import dataclass
from typing import Any, ClassVar, Tuple, Type, Union

from pydantic import GetCoreSchemaHandler
from pydantic._internal import _repr
from pydantic_core import ArgsKwargs, PydanticCustomError, core_schema

CoordinateValueType = Union[str, int, float]


class Latitude(float):
    min: ClassVar[float] = -90.00
    max: ClassVar[float] = 90.00

    @classmethod
    def __get_pydantic_core_schema__(cls, source: Type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.float_schema(ge=cls.min, le=cls.max)


class Longitude(float):
    min: ClassVar[float] = -180.00
    max: ClassVar[float] = 180.00

    @classmethod
    def __get_pydantic_core_schema__(cls, source: Type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.float_schema(ge=cls.min, le=cls.max)


@dataclass
class Coordinate(_repr.Representation):
    _NULL_ISLAND: ClassVar[Tuple[float, float]] = (0.0, 0.0)

    latitude: Latitude
    longitude: Longitude

    @classmethod
    def __get_pydantic_core_schema__(cls, source: Type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        schema_chain = [
            core_schema.no_info_wrap_validator_function(cls._parse_str, core_schema.str_schema()),
            core_schema.no_info_wrap_validator_function(
                cls._parse_tuple,
                handler.generate_schema(Tuple[float, float]),
            ),
            handler(source),
        ]

        chain_length = len(schema_chain)
        chain_schemas = [core_schema.chain_schema(schema_chain[x:]) for x in range(chain_length - 1, -1, -1)]
        return core_schema.no_info_wrap_validator_function(
            cls._parse_args, core_schema.union_schema(chain_schemas)  # type: ignore[arg-type]
        )

    @classmethod
    def _parse_args(cls, value: Any, handler: core_schema.ValidatorFunctionWrapHandler) -> Any:
        if isinstance(value, ArgsKwargs) and not value.kwargs:
            n_args = len(value.args)
            if n_args == 0:
                value = cls._NULL_ISLAND
            elif n_args == 1:
                value = value.args[0]
        return handler(value)

    @classmethod
    def _parse_str(cls, value: Any, handler: core_schema.ValidatorFunctionWrapHandler) -> Any:
        if not isinstance(value, str):
            return value
        try:
            value = tuple(float(x) for x in value.split(','))
        except ValueError:
            raise PydanticCustomError(
                'coordinate_error',
                'value is not a valid coordinate: string is not recognized as a valid coordinate',
            )
        return ArgsKwargs(args=value)

    @classmethod
    def _parse_tuple(cls, value: Any, handler: core_schema.ValidatorFunctionWrapHandler) -> Any:
        if not isinstance(value, tuple):
            return value
        return ArgsKwargs(args=handler(value))

    def __str__(self) -> str:
        return f'{self.latitude},{self.longitude}'

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Coordinate) and self.latitude == other.latitude and self.longitude == other.longitude

    def __hash__(self) -> int:
        return hash((self.latitude, self.longitude))
