from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

from pydantic_extra_types.routing_number import ABARoutingNumber


class Model(BaseModel):
    routing_number: ABARoutingNumber


@pytest.mark.parametrize('routing_number', [12, None, object(), 123456789])
def test_invalid_routing_number_string(routing_number: Any) -> None:
    with pytest.raises(ValidationError) as validation_error:
        Model(routing_number=routing_number)
    assert validation_error.match('Input should be a valid string')


@pytest.mark.parametrize('routing_number', ['', '123', '1234567890'])
def test_invalid_routing_number_length(routing_number: Any) -> None:
    with pytest.raises(ValidationError) as validation_error:
        Model(routing_number=routing_number)
    assert validation_error.match(r'String should have at (most|least) 9 characters')


@pytest.mark.parametrize('routing_number', ['122105154', '122235822', '123103723', '074900781'])
def test_invalid_routing_number(routing_number: Any) -> None:
    with pytest.raises(ValidationError) as validation_error:
        Model(routing_number=routing_number)
    assert validation_error.match('Incorrect ABA routing transit number')


@pytest.mark.parametrize('routing_number', ['122105155', '122235821', '123103729', '074900783'])
def test_valid_routing_number(routing_number: str) -> None:
    Model(routing_number=routing_number)


def test_raises_error_when_not_a_string() -> None:
    with pytest.raises(ValidationError, match='routing number is not all digits'):
        Model(routing_number='A12210515')
