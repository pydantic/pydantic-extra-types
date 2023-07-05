from typing import Any

import pytest
from pydantic import BaseModel, ValidationError
from pydantic_core import PydanticCustomError

from pydantic_extra_types.coordinate import Coordinate, Latitude, Longitude


class Coord(BaseModel):
    coord: Coordinate


class Lat(BaseModel):
    lat: Latitude


class Lng(BaseModel):
    lng: Longitude


@pytest.mark.parametrize(
    'coord, result, valid',
    [
        # Valid coordinates
        ((20.0, 10.0), (20.0, 10.0), True),
        ((-90.0, 0.0), (-90.0, 0.0), True),
        (('20.0', 10.0), (20.0, 10.0), True),
        ((20.0, '10.0'), (20.0, 10.0), True),
        (('45.678, -123.456'), (45.678, -123.456), True),
        ((45.678, -123.456), (45.678, -123.456), True),
        (Coordinate((20.0, 10.0)), (20.0, 10.0), True),
        # Invalid coordinates
        ((), None, False),  # Empty tuple
        ((10.0,), None, False),  # Tuple with only one value
        (('ten, '), None, False),
        ((20.0, 10.0, 30.0), None, False),  # Tuple with more than 2 values
        ('20.0, 10.0, 30.0', None, False),  # Str with more than 2 values
        (2, None, False),  # Tuple with more than 2 values
    ],
)
def test_format_for_coordinate(coord: (Any, Any), result: (float, float), valid: bool):
    if valid:
        _coord: Coordinate = Coord(coord=coord).coord
        assert _coord.latitude == result[0]
        assert _coord.longitude == result[1]
    else:
        with pytest.raises(PydanticCustomError, match='value is not a valid'):
            Coordinate(coord)


@pytest.mark.parametrize(
    'coord, valid',
    [
        # Valid coordinates
        ((-90.0, 0.0), True),
        ((50.0, 180.0), True),
        # Invalid coordinates
        ((-91.0, 0.0), False),
        ((50.0, 181.0), False),
    ],
)
def test_limit_for_coordinate(coord: (Any, Any), valid: bool):
    if valid:
        _coord: Coordinate = Coord(coord=coord).coord
        assert _coord.latitude == coord[0]
        assert _coord.longitude == coord[1]
    else:
        with pytest.raises(PydanticCustomError, match='value is not a valid'):
            Coordinate(coord)


@pytest.mark.parametrize(
    'latitude, valid',
    [
        # Valid latitude
        (20.0, True),
        (3.0000000000000000000000, True),
        (90.0, True),
        ('90.0', True),
        (-90.0, True),
        ('-90.0', True),
        # Unvalid latitude
        (91.0, False),
        (-91.0, False),
    ],
)
def test_format_latitude(latitude: float, valid: bool):
    if valid:
        _lat = Lat(lat=latitude).lat
        assert _lat == float(latitude)
    else:
        with pytest.raises(ValidationError, match='1 validation error for Lat'):
            Lat(lat=latitude)


@pytest.mark.parametrize(
    'longitude, valid',
    [
        # Valid latitude
        (20.0, True),
        (3.0000000000000000000000, True),
        (90.0, True),
        ('90.0', True),
        (-90.0, True),
        ('-90.0', True),
        (91.0, True),
        (-91.0, True),
        (180.0, True),
        (-180.0, True),
        # Unvalid latitude
        (181.0, False),
        (-181.0, False),
    ],
)
def test_format_longitude(longitude: float, valid: bool):
    if valid:
        _lng = Lng(lng=longitude).lng
        assert _lng == float(longitude)
    else:
        with pytest.raises(ValidationError, match='1 validation error for Lng'):
            Lng(lng=longitude)


def test_str_repr():
    assert str(Coordinate('20.0,10.0')) == '20.0,10.0'
    assert str(Coordinate((20.0, 10.0))) == '20.0,10.0'
    assert repr(Coordinate((20.0, 10.0))) == 'Coordinate(_latitude=20.0, _longitude=10.0)'


def test_eq():
    assert Coordinate('20.0,10.0') == Coordinate((20.0, 10.0))
    assert Coordinate('20.0,10.0') != Coordinate('20.0,11.0')


def test_color_hashable():
    assert hash(Coordinate((20.0, 10.0))) == hash(Coordinate((20.0, 10.0)))
    assert hash(Coordinate((20.0, 11.0))) != hash(Coordinate((20.0, 10.0)))
