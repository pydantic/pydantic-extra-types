import pycountry
import pytest
from pydantic import BaseModel

import pydantic_extra_types
from pydantic_extra_types.color import Color
from pydantic_extra_types.coordinate import Coordinate, Latitude, Longitude
from pydantic_extra_types.country import (
    CountryAlpha2,
    CountryAlpha3,
    CountryNumericCode,
    CountryShortName,
)
from pydantic_extra_types.currency_code import ISO4217, Currency
from pydantic_extra_types.isbn import ISBN
from pydantic_extra_types.language_code import ISO639_3, ISO639_5, LanguageAlpha2, LanguageName
from pydantic_extra_types.mac_address import MacAddress
from pydantic_extra_types.payment import PaymentCardNumber
from pydantic_extra_types.pendulum_dt import DateTime
from pydantic_extra_types.script_code import ISO_15924
from pydantic_extra_types.semantic_version import SemanticVersion
from pydantic_extra_types.timezone_name import TimeZoneName
from pydantic_extra_types.ulid import ULID

languages = [lang.alpha_3 for lang in pycountry.languages]
language_families = [lang.alpha_3 for lang in pycountry.language_families]
languages.sort()
language_families.sort()

currencies = [currency.alpha_3 for currency in pycountry.currencies]
currencies.sort()
everyday_currencies = [
    currency.alpha_3
    for currency in pycountry.currencies
    if currency.alpha_3 not in pydantic_extra_types.currency_code._CODES_FOR_BONDS_METAL_TESTING
]

scripts = [script.alpha_4 for script in pycountry.scripts]

timezone_names = TimeZoneName.allowed_values_list

everyday_currencies.sort()


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
        (
            ISBN,
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
            DateTime,
            {
                'properties': {'x': {'format': 'date-time', 'title': 'X', 'type': 'string'}},
                'required': ['x'],
                'title': 'Model',
                'type': 'object',
            },
        ),
        (
            LanguageAlpha2,
            {
                'properties': {'x': {'pattern': '^\\w{2}$', 'title': 'X', 'type': 'string'}},
                'required': ['x'],
                'title': 'Model',
                'type': 'object',
            },
        ),
        (
            LanguageName,
            {
                'properties': {'x': {'title': 'X', 'type': 'string'}},
                'required': ['x'],
                'title': 'Model',
                'type': 'object',
            },
        ),
        (
            ISO639_3,
            {
                'properties': {
                    'x': {
                        'title': 'X',
                        'type': 'string',
                        'enum': languages,
                        'maxLength': 3,
                        'minLength': 3,
                    }
                },
                'required': ['x'],
                'title': 'Model',
                'type': 'object',
            },
        ),
        (
            ISO639_5,
            {
                'properties': {
                    'x': {
                        'title': 'X',
                        'type': 'string',
                        'enum': language_families,
                        'maxLength': 3,
                        'minLength': 3,
                    }
                },
                'required': ['x'],
                'title': 'Model',
                'type': 'object',
            },
        ),
        (
            ISO4217,
            {
                'properties': {
                    'x': {
                        'title': 'X',
                        'type': 'string',
                        'enum': currencies,
                        'maxLength': 3,
                        'minLength': 3,
                    }
                },
                'required': ['x'],
                'title': 'Model',
                'type': 'object',
            },
        ),
        (
            Currency,
            {
                'properties': {
                    'x': {
                        'title': 'X',
                        'type': 'string',
                        'enum': everyday_currencies,
                        'maxLength': 3,
                        'minLength': 3,
                    }
                },
                'required': ['x'],
                'title': 'Model',
                'type': 'object',
            },
        ),
        (
            ISO_15924,
            {
                'properties': {
                    'x': {
                        'title': 'X',
                        'type': 'string',
                        'enum': scripts,
                        'maxLength': 4,
                        'minLength': 4,
                    }
                },
                'required': ['x'],
                'title': 'Model',
                'type': 'object',
            },
        ),
        (
            SemanticVersion,
            {
                'properties': {'x': {'title': 'X', 'type': 'string'}},
                'required': ['x'],
                'title': 'Model',
                'type': 'object',
            },
        ),
        (
            TimeZoneName,
            {
                'properties': {
                    'x': {
                        'title': 'X',
                        'type': 'string',
                        'enum': timezone_names,
                        'minLength': 1,
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
