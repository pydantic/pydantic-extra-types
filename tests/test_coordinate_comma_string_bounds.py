import json

import pytest
from pydantic import TypeAdapter, ValidationError

from pydantic_extra_types.coordinate import Coordinate


@pytest.mark.parametrize('json_input', [False, True])
@pytest.mark.parametrize(
    'value',
    [
        '90.000000000000000000001,0',
        '-90.000000000000000000001,0',
        '0,180.000000000000000000001',
        '0,-180.000000000000000000001',
    ],
)
def test_comma_string_rejects_values_rounded_inside_bounds(value: str, json_input: bool) -> None:
    adapter = TypeAdapter(Coordinate)

    with pytest.raises(ValidationError):
        if json_input:
            adapter.validate_json(json.dumps(value))
        else:
            adapter.validate_python(value)


@pytest.mark.parametrize('json_input', [False, True])
@pytest.mark.parametrize(
    'value, expected',
    [
        ('89.999999999999999999999,0', (90.0, 0.0)),
        ('-89.999999999999999999999,0', (-90.0, 0.0)),
        ('0,179.999999999999999999999', (0.0, 180.0)),
        ('0,-179.999999999999999999999', (0.0, -180.0)),
        ('90,-180', (90.0, -180.0)),
        ('-90,180', (-90.0, 180.0)),
        (' 45.678, -123.456 ', (45.678, -123.456)),
        ('+4.5e1,-1.2e2', (45.0, -120.0)),
        ('2_0,1_0', (20.0, 10.0)),
    ],
)
def test_comma_string_preserves_float_results(value: str, expected: tuple[float, float], json_input: bool) -> None:
    adapter = TypeAdapter(Coordinate)
    coordinate = adapter.validate_json(json.dumps(value)) if json_input else adapter.validate_python(value)

    assert (coordinate.latitude, coordinate.longitude) == expected
    assert type(coordinate.latitude) is float
    assert type(coordinate.longitude) is float
