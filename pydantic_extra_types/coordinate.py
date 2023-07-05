from __future__ import annotations

from typing import Any, Callable, ClassVar, Tuple, Union

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler, dataclasses
from pydantic._internal import _repr
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import ArgsKwargs, CoreSchema, PydanticCustomError, core_schema

CoordinateValueType = Union[str, int, float]


class Latitude(float):
    min: ClassVar[float] = -90.00
    max: ClassVar[float] = 90.00

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.float_schema(ge=cls.min, le=cls.max)


class Longitude(float):
    min: ClassVar[float] = -180.00
    max: ClassVar[float] = 180.00

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.float_schema(ge=cls.min, le=cls.max)


CoordinateTuple = Tuple[Latitude, Longitude]
CoordinateType = Union[CoordinateTuple, str, 'Coordinate']


@dataclasses.dataclass
class Coordinate(_repr.Representation):
    latitude: Latitude
    longitude: Longitude

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        field_schema: dict[str, Any] = handler(core_schema)
        field_schema.update(format='coordinate')
        return field_schema

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: type[Any], handler: Callable[[Any], CoreSchema]
    ) -> core_schema.CoreSchema:
        return core_schema.general_before_validator_function(
            cls._validate, handler(source), serialization=core_schema.to_string_ser_schema()
        )

    @classmethod
    def _validate(cls, value: Any, _: Any) -> dict[str, Any]:
        if isinstance(value, ArgsKwargs):
            args = value.args
            kwargs = value.kwargs or {}
        else:
            args = (value,)
            kwargs = {}

        if kwargs:
            if kwargs.keys() != {'latitude', 'longitude'}:
                raise PydanticCustomError(
                    'coordinate_error', 'Coordinate constructor accepts only "latitude" and "longitude" kwargs'
                )
            _validated_tuple = (kwargs['latitude'], kwargs['longitude'])
        else:
            arg = args[0]
            if isinstance(arg, (tuple, list)):
                _validated_tuple = cls.parse_tuple(arg)
            elif isinstance(arg, str):
                _validated_tuple = cls.parse_str(arg)
            elif isinstance(arg, Coordinate):
                _validated_tuple = (arg.latitude, arg.longitude)
            else:
                raise PydanticCustomError(
                    'coordinate_error',
                    'value is not a valid Coordinate: value must be a tuple, list or string',
                )

        return {'latitude': _validated_tuple[0], 'longitude': _validated_tuple[1]}

    def __str__(self) -> str:
        return f'{self.latitude},{self.longitude}'

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Coordinate) and self.latitude == other.latitude and self.longitude == other.longitude

    def __hash__(self) -> int:
        return hash((self.latitude, self.longitude))

    @staticmethod
    def parse_str(value: str) -> CoordinateTuple:
        """
        Parse a string representing a coordinate to a Coordinate tuple.

        Possible formats for the input string include:
        - <latitude>, <longitude>

        Args:
            value (str): The string representation of the coordinate.

        Returns:
            CoordinateTuple: A tuple containing the latitude and longitude values.

        Raises:
            PydanticCustomError: If the input string is not a valid coordinate.
        """
        try:
            _coord = [float(x) for x in value.split(',')]
            if len(_coord) != 2:
                raise PydanticCustomError(
                    'coordinate_error', 'value is not a valid coordinate: string not recognised as a valid coordinate'
                )
        except ValueError:
            raise PydanticCustomError(
                'coordinate_error', 'value is not a valid coordinate: string not recognised as a valid coordinate'
            )

        _lat = Latitude(_coord[0])
        _long = Longitude(_coord[1])

        return _lat, _long

    @staticmethod
    def parse_tuple(value: tuple[Any, ...] | list[Any]) -> CoordinateTuple:
        """
        Parse a tuple representing a coordinate to a Coordinate tuple.

        Args:
            value (Tuple[Any, ...]): The tuple representation of the coordinate.

        Returns:
            CoordinateTuple: A tuple containing the latitude and longitude values.

        Raises:
            PydanticCustomError: If the input tuple is not a valid coordinate.
        """
        if len(value) == 2:
            _lat = Latitude(value[0])
            _long = Longitude(value[1])
            return _lat, _long
        else:
            raise PydanticCustomError('coordinate_error', 'value is not a valid coordinate: tuples must have length 2')
