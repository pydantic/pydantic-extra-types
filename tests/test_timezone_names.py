import re

import pytest
import pytz
from pydantic import BaseModel, ValidationError

from pydantic_extra_types.timezone_name import TimeZoneName

has_zone_info = True
try:
    from zoneinfo import available_timezones
except ImportError:
    has_zone_info = False

pytz_zones_bad = [(zone.lower(), zone) for zone in pytz.all_timezones]
pytz_zones_bad.extend([(f' {zone}', zone) for zone in pytz.all_timezones_set])


class TZNameCheck(BaseModel):
    timezone_name: TimeZoneName


class TZNonStrict(TimeZoneName, strict=False):
    pass


class NonStrictTzName(BaseModel):
    timezone_name: TZNonStrict


@pytest.mark.parametrize('zone', pytz.all_timezones)
def test_all_timezones_non_strict_pytz(zone):
    assert TZNameCheck(timezone_name=zone).timezone_name == zone
    assert NonStrictTzName(timezone_name=zone).timezone_name == zone


@pytest.mark.parametrize('zone', pytz_zones_bad)
def test_all_timezones_pytz_lower(zone):
    assert NonStrictTzName(timezone_name=zone[0]).timezone_name == zone[1]


def test_fail_non_existing_timezone():
    with pytest.raises(
        ValidationError,
        match=re.escape(
            '1 validation error for TZNameCheck\n'
            'timezone_name\n  '
            'Invalid timezone name. '
            "[type=TimeZoneName, input_value='mars', input_type=str]"
        ),
    ):
        TZNameCheck(timezone_name='mars')

    with pytest.raises(
        ValidationError,
        match=re.escape(
            '1 validation error for NonStrictTzName\n'
            'timezone_name\n  '
            'Invalid timezone name. '
            "[type=TimeZoneName, input_value='mars', input_type=str]"
        ),
    ):
        NonStrictTzName(timezone_name='mars')


if has_zone_info:
    zones = list(available_timezones())
    zones.sort()
    zones_bad = [(zone.lower(), zone) for zone in zones]

    @pytest.mark.parametrize('zone', zones)
    def test_all_timezones_zone_info(zone):
        assert TZNameCheck(timezone_name=zone).timezone_name == zone
        assert NonStrictTzName(timezone_name=zone).timezone_name == zone

    @pytest.mark.parametrize('zone', zones_bad)
    def test_all_timezones_zone_info_NonStrict(zone):
        assert NonStrictTzName(timezone_name=zone[0]).timezone_name == zone[1]
