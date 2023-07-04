from typing import Any, Callable, ClassVar, Tuple, Type, Union

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic._internal import _repr
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, PydanticCustomError, core_schema

LatitudeType = Union[str, int, float]


class Latitude(float):
    ge: ClassVar[float] = -90.00
    le: ClassVar[float] = 90.00

    def __init__(self, value: LatitudeType):
        self.validate_lat(value)

    @classmethod
    def __get_pydantic_core_schema__(cls, source: Type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.general_after_validator_function(
            cls._validate, core_schema.float_schema(ge=cls.ge, le=cls.le)
        )

    @classmethod
    def _validate(cls, __input_value: Any, _: core_schema.ValidationInfo) -> 'Latitude':
        return cls(__input_value)

    @classmethod
    def validate_lat(cls, value: LatitudeType) -> None:
        """
        Validate the latitude value.

        Raises:
            PydanticCustomError: If the latitude value is not within the valid range.
        """
        try:
            if float(value) > cls.le or float(value) < cls.ge:
                raise PydanticCustomError('latitude_error', 'Latitude must be between -90 and 90')
        except ValueError:
            raise PydanticCustomError(
                'latitude_error',
                'value is not a valid Latitude: value must be a str, int or float',
            )


LongitudeType = Union[str, int, float]


class Longitude(float):
    ge: ClassVar[float] = -180.00
    le: ClassVar[float] = 180.00

    def __init__(self, value: LongitudeType):
        self.validate_long(value)

    @classmethod
    def __get_pydantic_core_schema__(cls, source: Type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.general_after_validator_function(
            cls._validate, core_schema.float_schema(ge=cls.ge, le=cls.le)
        )

    @classmethod
    def _validate(cls, __input_value: Any, _: core_schema.ValidationInfo) -> 'Longitude':
        return cls(__input_value)

    @classmethod
    def validate_long(cls, value: Any) -> None:
        """
        Validate the longitude value.

        Raises:
            PydanticCustomError: If the longitude value is not within the valid range.
        """
        try:
            if float(value) > cls.le or float(value) < cls.ge:
                raise PydanticCustomError('longitude_error', 'Longitude must be between -180 and 180')
        except ValueError:
            raise PydanticCustomError(
                'longitude_error',
                'value is not a valid Longitude: value must be a str, int or float',
            )


CoordinateTuple = Tuple[Latitude, Longitude]
CoordinateType = Union[CoordinateTuple, str, 'Coordinate']


class Coordinate(_repr.Representation):
    __slots__ = '_latitude', '_longitude'

    def __init__(self, value: CoordinateType) -> None:
        self._latitude: Latitude
        self._longitude: Longitude
        if isinstance(value, (tuple, list)):
            self._latitude, self._longitude = parse_tuple(value)
        elif isinstance(value, str):
            self._latitude, self._longitude = parse_str(value)
        elif isinstance(value, Coordinate):
            self._latitude = value.latitude
            self._longitude = value.longitude
        else:
            raise PydanticCustomError(
                'coordinate_error',
                'value is not a valid Coordinate: value must be a tuple, list or string',
            )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        field_schema: dict[str, Any] = {}
        field_schema.update(type='string', format='coordinate')
        return field_schema

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: Type[Any], handler: Callable[[Any], CoreSchema]
    ) -> core_schema.CoreSchema:
        return core_schema.general_plain_validator_function(
            cls._validate, serialization=core_schema.to_string_ser_schema()
        )

    @classmethod
    def _validate(cls, __input_value: Any, _: Any) -> 'Coordinate':
        return cls(__input_value)

    @property
    def latitude(self) -> 'Latitude':
        """
        Get the latitude value of the coordinate.
        """
        return self._latitude

    @property
    def longitude(self) -> 'Longitude':
        """
        Get the longitude value of the coordinate.
        """
        return self._longitude

    def __str__(self) -> str:
        return f'{self.latitude},{self.longitude}'

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Coordinate) and self.latitude == other.latitude and self.longitude == other.longitude

    def __hash__(self) -> int:
        return hash((self.latitude, self.longitude))


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


def parse_tuple(value: Tuple[Any, ...]) -> CoordinateTuple:
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
