import pytest
from pydantic import BaseModel

from pydantic_extra_types.color import Color
from pydantic_extra_types.coordinate import Coordinate, Latitude, Longitude
from pydantic_extra_types.country import (
    CountryAlpha2,
    CountryAlpha3,
    CountryNumericCode,
    CountryOfficialName,
    CountryShortName,
)
from pydantic_extra_types.mac_address import MacAddress
from pydantic_extra_types.payment import PaymentCardNumber
from pydantic_extra_types.ulid import ULID


@pytest.mark.parametrize(
    'cls,expected',
    [
        (
            Color,
            {
                'properties': {'x': {'format': 'color', 'title': 'X', 'type': 'string'}},
                'required': ['x'],
                'title': 'Model',
                'type': 'object',
            },
        ),
        (
            PaymentCardNumber,
            {
                'properties': {
                    'x': {
                        'maxLength': 19,
                        'minLength': 12,
                        'title': 'X',
                        'type': 'string',
                    }
                },
                'required': ['x'],
                'title': 'Model',
                'type': 'object',
            },
        ),
        (
            CountryAlpha2,
            {
                'properties': {'x': {'pattern': '^\\w{2}$', 'title': 'X', 'type': 'string'}},
                'required': ['x'],
                'title': 'Model',
                'type': 'object',
            },
        ),
        (
            CountryAlpha3,
            {
                'properties': {'x': {'pattern': '^\\w{3}$', 'title': 'X', 'type': 'string'}},
                'required': ['x'],
                'title': 'Model',
                'type': 'object',
            },
        ),
        (
            CountryNumericCode,
            {
                'properties': {'x': {'pattern': '^[0-9]{3}$', 'title': 'X', 'type': 'string'}},
                'required': ['x'],
                'title': 'Model',
                'type': 'object',
            },
        ),
        (
            CountryOfficialName,
            {
                'properties': {'x': {'title': 'X', 'type': 'string'}},
                'required': ['x'],
                'title': 'Model',
                'type': 'object',
            },
        ),
        (
            CountryShortName,
            {
                'properties': {'x': {'title': 'X', 'type': 'string'}},
                'required': ['x'],
                'title': 'Model',
                'type': 'object',
            },
        ),
        (
            MacAddress,
            {
                'properties': {
                    'x': {
                        'title': 'X',
                        'type': 'string',
                    }
                },
                'required': ['x'],
                'title': 'Model',
                'type': 'object',
            },
        ),
        (
            Latitude,
            {
                'properties': {
                    'x': {
                        'maximum': 90.0,
                        'minimum': -90.0,
                        'title': 'X',
                        'type': 'number',
                    }
                },
                'required': ['x'],
                'title': 'Model',
                'type': 'object',
            },
        ),
        (
            Longitude,
            {
                'properties': {
                    'x': {
                        'maximum': 180.0,
                        'minimum': -180.0,
                        'title': 'X',
                        'type': 'number',
                    }
                },
                'required': ['x'],
                'title': 'Model',
                'type': 'object',
            },
        ),
        (
            Coordinate,
            {
                '$defs': {
                    'Coordinate': {
                        'properties': {
                            'latitude': {'maximum': 90.0, 'minimum': -90.0, 'title': 'Latitude', 'type': 'number'},
                            'longitude': {'maximum': 180.0, 'minimum': -180.0, 'title': 'Longitude', 'type': 'number'},
                        },
                        'required': ['latitude', 'longitude'],
                        'title': 'Coordinate',
                        'type': 'object',
                    }
                },
                'properties': {
                    'x': {
                        'anyOf': [
                            {'$ref': '#/$defs/Coordinate'},
                            {
                                'maxItems': 2,
                                'minItems': 2,
                                'prefixItems': [
                                    {'type': 'number'},
                                    {'type': 'number'},
                                ],
                                'type': 'array',
                            },
                            {'type': 'string'},
                        ],
                        'title': 'X',
                    },
                },
                'required': ['x'],
                'title': 'Model',
                'type': 'object',
            },
        ),
        (
            ULID,
            {
                'properties': {
                    'x': {
                        'anyOf': [{'type': 'integer'}, {'format': 'binary', 'type': 'string'}, {'type': 'string'}],
                        'title': 'X',
                    }
                },
                'required': ['x'],
                'title': 'Model',
                'type': 'object',
            },
        ),
    ],
)
def test_json_schema(cls, expected):
    class Model(BaseModel):
        x: cls

    assert Model.model_json_schema() == expected
