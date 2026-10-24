"""The `pydantic_extra_types.coordinate` module provides the [`Latitude`][pydantic_extra_types.coordinate.Latitude],
[`Longitude`][pydantic_extra_types.coordinate.Longitude], and
[`Coordinate`][pydantic_extra_types.coordinate.Coordinate] data types.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Annotated, Any, ClassVar

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic._internal import _repr
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import ArgsKwargs, PydanticCustomError, core_schema

# Pattern used by pydantic for decimal string validation in JSON schema
_DECIMAL_PATTERN = r'^(?!^[-+.]*$)[+-]?0*\d*\.?\d*$'


class _FloatDecimalAnnotation:
    """Annotation for Union[float, Decimal] that provides proper JSON schema with decimal pattern."""

    @classmethod
    def _validate(cls, value: Any, handler: core_schema.ValidatorFunctionWrapHandler) -> Any:
        """Keep Decimal values as Decimal so the enclosing field can check their bounds exactly.

        Pydantic's smart-union fallback would otherwise convert an out-of-range Decimal to a
        lossy float before ``Latitude``/``Longitude`` sees it.
        """
        if isinstance(value, Decimal):
            return value if value.is_finite() else handler(value)
        if isinstance(value, str):
            try:
                decimal_value = Decimal(value)
            except (InvalidOperation, ValueError):
                return handler(value)
            if decimal_value.is_finite():
                return decimal_value
        return handler(value)

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.no_info_wrap_validator_function(
            cls._validate,
            core_schema.float_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {
            'anyOf': [
                {'type': 'number'},
                {'type': 'string', 'pattern': _DECIMAL_PATTERN},
            ]
        }


# Type for tuple items that properly serializes decimal JSON schema with pattern
_CoordinateValue = Annotated[float | Decimal, _FloatDecimalAnnotation]

LatitudeType = float | Decimal
LongitudeType = float | Decimal
CoordinateType = tuple[_CoordinateValue, _CoordinateValue]


def _check_decimal_range(value: Decimal, minimum: float, maximum: float) -> None:
    """Raise the same bound errors as pydantic's constrained decimal schema."""
    if value < Decimal(str(minimum)):
        raise PydanticCustomError(
            'greater_than_equal',
            'Input should be greater than or equal to {minimum}',
            {'minimum': minimum},
        )
    if value > Decimal(str(maximum)):
        raise PydanticCustomError(
            'less_than_equal',
            'Input should be less than or equal to {maximum}',
            {'maximum': maximum},
        )


def _reject_lossy_decimal(value: Any, minimum: float, maximum: float) -> None:
    """Reject an out-of-range Decimal that the float branch would have rounded into range."""
    if isinstance(value, Decimal):
        decimal_value = value
    elif isinstance(value, str):
        try:
            decimal_value = Decimal(value)
        except (InvalidOperation, ValueError):
            return
    else:
        return
    if not decimal_value.is_finite():
        return
    if Decimal(str(minimum)) <= decimal_value <= Decimal(str(maximum)):
        return
    try:
        float_value = float(value)
    except (ValueError, OverflowError):
        return
    if minimum <= float_value <= maximum:
        _check_decimal_range(decimal_value, minimum, maximum)


class Latitude(float):
    """Latitude value should be between -90 and 90, inclusive.

    Supports both float and Decimal types.

    ```py
    from decimal import Decimal
    from pydantic import BaseModel
    from pydantic_extra_types.coordinate import Latitude


    class Location(BaseModel):
        latitude: Latitude


    # Using float
    location1 = Location(latitude=41.40338)
    # Using Decimal
    location2 = Location(latitude=Decimal('41.40338'))
    ```
    """

    min: ClassVar[float] = -90.00
    max: ClassVar[float] = 90.00

    @classmethod
    def _validate(cls, value: Any, handler: core_schema.ValidatorFunctionWrapHandler) -> Any:
        """Reject the lossy float fallback before validating the normal float/Decimal union."""
        _reject_lossy_decimal(value, cls.min, cls.max)
        return handler(value)

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.no_info_wrap_validator_function(
            cls._validate,
            core_schema.union_schema(
                [
                    core_schema.float_schema(ge=cls.min, le=cls.max),
                    core_schema.decimal_schema(ge=Decimal(cls.min), le=Decimal(cls.max)),
                ]
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {
            'anyOf': [
                {'type': 'number', 'minimum': cls.min, 'maximum': cls.max},
                {'type': 'string', 'pattern': _DECIMAL_PATTERN},
            ]
        }


class Longitude(float):
    """Longitude value should be between -180 and 180, inclusive.

    Supports both float and Decimal types.

    ```py
    from decimal import Decimal
    from pydantic import BaseModel

    from pydantic_extra_types.coordinate import Longitude


    class Location(BaseModel):
        longitude: Longitude


    # Using float
    location1 = Location(longitude=2.17403)
    # Using Decimal
    location2 = Location(longitude=Decimal('2.17403'))
    ```
    """

    min: ClassVar[float] = -180.00
    max: ClassVar[float] = 180.00

    @classmethod
    def _validate(cls, value: Any, handler: core_schema.ValidatorFunctionWrapHandler) -> Any:
        """Reject the lossy float fallback before validating the normal float/Decimal union."""
        _reject_lossy_decimal(value, cls.min, cls.max)
        return handler(value)

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.no_info_wrap_validator_function(
            cls._validate,
            core_schema.union_schema(
                [
                    core_schema.float_schema(ge=cls.min, le=cls.max),
                    core_schema.decimal_schema(ge=Decimal(cls.min), le=Decimal(cls.max)),
                ]
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {
            'anyOf': [
                {'type': 'number', 'minimum': cls.min, 'maximum': cls.max},
                {'type': 'string', 'pattern': _DECIMAL_PATTERN},
            ]
        }


@dataclass
class Coordinate(_repr.Representation):
    """Coordinate parses Latitude and Longitude.

    You can use the `Coordinate` data type for storing coordinates. Coordinates can be
    defined using one of the following formats:

    1. Tuple: `(Latitude, Longitude)`. For example: `(41.40338, 2.17403)` or `(Decimal('41.40338'), Decimal('2.17403'))`.
    2. `Coordinate` instance: `Coordinate(latitude=Latitude, longitude=Longitude)`.

    ```py
    from decimal import Decimal
    from pydantic import BaseModel

    from pydantic_extra_types.coordinate import Coordinate


    class Location(BaseModel):
        coordinate: Coordinate


    # Using float values
    location1 = Location(coordinate=(41.40338, 2.17403))
    # > coordinate=Coordinate(latitude=41.40338, longitude=2.17403)

    # Using Decimal values
    location2 = Location(coordinate=(Decimal('41.40338'), Decimal('2.17403')))
    # > coordinate=Coordinate(latitude=41.40338, longitude=2.17403)
    ```
    """

    _NULL_ISLAND: ClassVar[tuple[float, float]] = (0.0, 0.0)

    latitude: Latitude
    longitude: Longitude

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        schema_chain = [
            core_schema.no_info_wrap_validator_function(cls._parse_str, core_schema.str_schema()),
            core_schema.no_info_wrap_validator_function(
                cls._parse_tuple,
                handler.generate_schema(CoordinateType),
            ),
            handler(source),
        ]

        chain_length = len(schema_chain)
        chain_schemas = [core_schema.chain_schema(schema_chain[x:]) for x in range(chain_length - 1, -1, -1)]
        return core_schema.no_info_wrap_validator_function(
            cls._parse_args,
            core_schema.union_schema(chain_schemas),  # type: ignore[arg-type]
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
        except ValueError as e:
            raise PydanticCustomError(
                'coordinate_error',
                'value is not a valid coordinate: string is not recognized as a valid coordinate',
            ) from e
        return ArgsKwargs(args=value)

    @classmethod
    def _parse_tuple(cls, value: Any, handler: core_schema.ValidatorFunctionWrapHandler) -> Any:
        return ArgsKwargs(args=handler(value)) if isinstance(value, (tuple, list)) else value

    def __str__(self) -> str:
        return f'{self.latitude},{self.longitude}'

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Coordinate) and self.latitude == other.latitude and self.longitude == other.longitude

    def __hash__(self) -> int:
        return hash((self.latitude, self.longitude))
