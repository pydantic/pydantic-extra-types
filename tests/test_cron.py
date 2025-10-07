from datetime import datetime, timezone

import pytest
from cron_converter import Cron
from pydantic import BaseModel, ValidationError

from pydantic_extra_types.cron import CronStr


class CronModel(BaseModel):
    cron: CronStr


def test_cron_str_is_validated_via_model() -> None:
    model = CronModel(cron='*/5 0 * * 1-5')
    cron_value = model.cron

    assert isinstance(cron_value, CronStr)
    assert cron_value.minute == '*/5'
    assert cron_value.hour == '0'
    assert cron_value.day_of_the_month == '*'
    assert cron_value.month == '*'
    assert cron_value.day_of_the_week == '1-5'
    assert isinstance(cron_value.cron_obj, Cron)


def test_cron_str_rejects_invalid_components() -> None:
    with pytest.raises(ValidationError) as exc:
        CronModel(cron='* * * *')
    assert 'Cron expression must contain 5 space separated components' in str(exc.value)


def test_cron_str_rejects_invalid_expression() -> None:
    with pytest.raises(ValidationError) as exc:
        CronModel(cron='60 0 * * *')
    assert "Value 60 out of range for 'minute'" in str(exc.value)


def test_cron_str_next_after() -> None:
    cron_value = CronStr('15 8 * * 1-5')
    next_run = cron_value.next_after(datetime(2024, 1, 1, 7, 0))
    assert next_run == datetime(2024, 1, 1, 8, 15)
    current_year = datetime.now(timezone.utc).year
    assert cron_value.next_run.startswith(str(current_year))  # sanity check for property access


def test_cron_str_strips_whitespace() -> None:
    cron_value = CronStr(' 0 12 * * * ')
    assert str(cron_value) == '0 12 * * *'
