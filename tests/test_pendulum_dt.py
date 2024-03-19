import pendulum
import pytest
from pydantic import BaseModel, ValidationError

from pydantic_extra_types.pendulum_dt import Date, DateTime


class DtModel(BaseModel):
    dt: DateTime


class DateModel(BaseModel):
    d: Date


def test_pendulum_dt_existing_instance():
    """
    Verifies that constructing a model with an existing pendulum dt doesn't throw.
    """
    now = pendulum.now()
    model = DtModel(dt=now)
    assert model.dt == now


def test_pendulum_date_existing_instance():
    """
    Verifies that constructing a model with an existing pendulum date doesn't throw.
    """
    today = pendulum.today().date()
    model = DateModel(d=today)
    assert model.d == today


@pytest.mark.parametrize(
    'dt', [pendulum.now().to_iso8601_string(), pendulum.now().to_w3c_string(), pendulum.now().to_iso8601_string()]
)
def test_pendulum_dt_from_serialized(dt):
    """
    Verifies that building an instance from serialized, well-formed strings decode properly.
    """
    dt_actual = pendulum.parse(dt)
    model = DtModel(dt=dt)
    assert model.dt == dt_actual


def test_pendulum_date_from_serialized():
    """
    Verifies that building an instance from serialized, well-formed strings decode properly.
    """
    date_actual = pendulum.parse('2024-03-18').date()
    model = DateModel(d='2024-03-18')
    assert model.d == date_actual


@pytest.mark.parametrize('dt', [None, 'malformed', pendulum.now().to_iso8601_string()[:5], 42])
def test_pendulum_dt_malformed(dt):
    """
    Verifies that the instance fails to validate if malformed dt are passed.
    """
    with pytest.raises(ValidationError):
        DtModel(dt=dt)


@pytest.mark.parametrize('date', [None, 'malformed', pendulum.today().to_iso8601_string()[:5], 42])
def test_pendulum_date_malformed(date):
    """
    Verifies that the instance fails to validate if malformed date are passed.
    """
    with pytest.raises(ValidationError):
        DateModel(d=date)
