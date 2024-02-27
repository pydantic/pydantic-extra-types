import pendulum
import pytest
from pydantic import BaseModel, ValidationError

from pydantic_extra_types.pendulum_dt import DateTime


class Model(BaseModel):
    dt: DateTime


def test_pendulum_dt_existing_instance():
    """
    Verifies that constructing a model with an existing pendulum dt doesn't throw.
    """
    now = pendulum.now()
    model = Model(dt=now)
    assert model.dt == now


@pytest.mark.parametrize(
    'dt', [pendulum.now().to_iso8601_string(), pendulum.now().to_w3c_string(), pendulum.now().to_iso8601_string()]
)
def test_pendulum_dt_from_serialized(dt):
    """
    Verifies that building an instance from serialized, well-formed strings decode properly.
    """
    dt_actual = pendulum.parse(dt)
    model = Model(dt=dt)
    assert model.dt == dt_actual


@pytest.mark.parametrize('dt', [None, 'malformed', pendulum.now().to_iso8601_string()[:5], 42])
def test_pendulum_dt_malformed(dt):
    """
    Verifies that the instance fails to validate if malformed dt are passed.
    """
    with pytest.raises(ValidationError):
        Model(dt=dt)
