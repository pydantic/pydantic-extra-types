import pytest
from pydantic import BaseModel

from pydantic_extra_types.color import Color
from pydantic_extra_types.country import (
    CountryAlpha2,
    CountryAlpha3,
    CountryNumericCode,
    CountryOfficialName,
    CountryShortName,
)
from pydantic_extra_types.payment import PaymentCardNumber


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
    ],
)
def test_json_schema(cls, expected):
    class Model(BaseModel):
        x: cls

    assert Model.model_json_schema() == expected
