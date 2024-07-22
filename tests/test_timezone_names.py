import re

import pytest
import pytz
from pydantic import BaseModel, ValidationError
from pydantic_core import PydanticCustomError

from pydantic_extra_types.timezone_name import TimeZoneName, TimeZoneNameSettings, timezone_name_settings

has_zone_info = True
try:
    from zoneinfo import available_timezones
except ImportError:
    has_zone_info = False

pytz_zones_bad = [(zone.lower(), zone) for zone in pytz.all_timezones]
pytz_zones_bad.extend([(f' {zone}', zone) for zone in pytz.all_timezones_set])


class TZNameCheck(BaseModel):
    timezone_name: TimeZoneName


@timezone_name_settings(strict=False)
class TZNonStrict(TimeZoneName):
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


def test_timezone_name_settings_metaclass():
    class TestStrictTZ(TimeZoneName, strict=True, metaclass=TimeZoneNameSettings):
        pass

    class TestNonStrictTZ(TimeZoneName, strict=False, metaclass=TimeZoneNameSettings):
        pass

    assert TestStrictTZ.strict is True
    assert TestNonStrictTZ.strict is False

    # Test default value
    class TestDefaultStrictTZ(TimeZoneName, metaclass=TimeZoneNameSettings):
        pass

    assert TestDefaultStrictTZ.strict is True


def test_timezone_name_validation():
    valid_tz = 'America/New_York'
    invalid_tz = 'Invalid/Timezone'

    assert TimeZoneName._validate(valid_tz, None) == valid_tz

    with pytest.raises(PydanticCustomError):
        TimeZoneName._validate(invalid_tz, None)

    assert TZNonStrict._validate(valid_tz.lower(), None) == valid_tz
    assert TZNonStrict._validate(f' {valid_tz} ', None) == valid_tz

    with pytest.raises(PydanticCustomError):
        TZNonStrict._validate(invalid_tz, None)


def test_timezone_name_pydantic_core_schema():
    schema = TimeZoneName.__get_pydantic_core_schema__(TimeZoneName, None)
    assert isinstance(schema, dict)
    assert schema['type'] == 'function-after'
    assert 'function' in schema
    assert 'schema' in schema
    assert schema['schema']['type'] == 'str'
    assert schema['schema']['min_length'] == 1


def test_timezone_name_pydantic_json_schema():
    core_schema = TimeZoneName.__get_pydantic_core_schema__(TimeZoneName, None)

    class MockJsonSchemaHandler:
        def __call__(self, schema):
            return {'type': 'string'}

    handler = MockJsonSchemaHandler()
    json_schema = TimeZoneName.__get_pydantic_json_schema__(core_schema, handler)
    assert 'enum' in json_schema
    assert isinstance(json_schema['enum'], list)
    assert len(json_schema['enum']) > 0


def test_timezone_name_repr():
    tz = TimeZoneName('America/New_York')
    assert repr(tz) == "'America/New_York'"
    assert str(tz) == 'America/New_York'


def test_timezone_name_allowed_values():
    assert isinstance(TimeZoneName.allowed_values, set)
    assert len(TimeZoneName.allowed_values) > 0
    assert all(isinstance(tz, str) for tz in TimeZoneName.allowed_values)

    assert isinstance(TimeZoneName.allowed_values_list, list)
    assert len(TimeZoneName.allowed_values_list) > 0
    assert all(isinstance(tz, str) for tz in TimeZoneName.allowed_values_list)

    assert isinstance(TimeZoneName.allowed_values_upper_to_correct, dict)
    assert len(TimeZoneName.allowed_values_upper_to_correct) > 0
    assert all(
        isinstance(k, str) and isinstance(v, str) for k, v in TimeZoneName.allowed_values_upper_to_correct.items()
    )


def test_timezone_name_inheritance():
    class CustomTZ(TimeZoneName, metaclass=TimeZoneNameSettings):
        pass

    assert issubclass(CustomTZ, TimeZoneName)
    assert issubclass(CustomTZ, str)
    assert isinstance(CustomTZ('America/New_York'), (CustomTZ, TimeZoneName, str))


def test_timezone_name_string_operations():
    tz = TimeZoneName('America/New_York')
    assert tz.upper() == 'AMERICA/NEW_YORK'
    assert tz.lower() == 'america/new_york'
    assert tz.strip() == 'America/New_York'
    assert f'{tz} Time' == 'America/New_York Time'
    assert tz.startswith('America')
    assert tz.endswith('York')


def test_timezone_name_comparison():
    tz1 = TimeZoneName('America/New_York')
    tz2 = TimeZoneName('Europe/London')
    tz3 = TimeZoneName('America/New_York')

    assert tz1 == tz3
    assert tz1 != tz2
    assert tz1 < tz2  # Alphabetical comparison
    assert tz2 > tz1
    assert tz1 <= tz3
    assert tz1 >= tz3


def test_timezone_name_hash():
    tz1 = TimeZoneName('America/New_York')
    tz2 = TimeZoneName('America/New_York')
    tz3 = TimeZoneName('Europe/London')

    assert hash(tz1) == hash(tz2)
    assert hash(tz1) != hash(tz3)

    tz_set = {tz1, tz2, tz3}
    assert len(tz_set) == 2


def test_timezone_name_slots():
    tz = TimeZoneName('America/New_York')
    with pytest.raises(AttributeError):
        tz.new_attribute = 'test'
