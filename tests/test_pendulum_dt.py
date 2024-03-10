import pendulum
import pytest
from pydantic import BaseModel, ValidationError

from pydantic_extra_types.pendulum_dt import Date
from pydantic_extra_types.pendulum_dt import DateTime


class Model(BaseModel):
    dt: DateTime
    d: Date


def test_pendulum_dt_existing_instance():
    """
    Verifies that constructing a model with an existing pendulum dt doesn't throw.
    """
    now = pendulum.now()
    today = pendulum.today()
    model = Model(dt=now, d=today)
    assert model.dt == now
    assert model.d == today


@pytest.mark.parametrize(
    'dt', [pendulum.now().to_iso8601_string(), pendulum.now().to_w3c_string(), pendulum.now().to_iso8601_string()]
)
def test_pendulum_dt_from_serialized(dt):
    """
    Verifies that building an instance from serialized, well-formed strings decode properly.
    """
    dt_actual = pendulum.parse(dt)
    today = pendulum.today()
    model = Model(dt=dt, d=today)
    assert model.dt == dt_actual
    assert model.d == today


@pytest.mark.parametrize(
    "date", [pendulum.today().to_iso8601_string(), pendulum.today().to_w3c_string(), pendulum.today().to_iso8601_string()]
)
def test_pendulum_date_from_serialized(date):
    """
    Verifies that building an instance from serialized, well-formed strings decode properly.
    """
    now = pendulum.now()
    date_actual = pendulum.parse(date)
    model = Model(dt=now, d=date_actual)
    assert model.dt == now
    assert model.d == date_actual


@pytest.mark.parametrize('dt', [None, 'malformed', pendulum.now().to_iso8601_string()[:5], 42])
def test_pendulum_dt_malformed(dt):
    """
    Verifies that the instance fails to validate if malformed dt are passed.
    """
    with pytest.raises(ValidationError):
        Model(dt=dt, d=pendulum.today())


@pytest.mark.parametrize("date", [None, "malformed", pendulum.today().to_iso8601_string()[:5], 42])
def test_pendulum_date_malformed(date):
    """
    Verifies that the instance fails to validate if malformed date are passed.
    """
    with pytest.raises(ValidationError):
        Model(dt=pendulum.now(), d=date)
