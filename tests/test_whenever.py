from collections.abc import Callable
from datetime import datetime, timedelta, timezone
from typing import Annotated

import pytest
from pydantic import BaseModel, TypeAdapter, ValidationError
from whenever import (
    DateDelta,
    DateTimeDelta,
    Instant,
    LocalDateTime,
    OffsetDateTime,
    SystemDateTime,
    TimeDelta,
    ZonedDateTime,
)
from zoneinfo import ZoneInfo

from pydantic_extra_types.whenever import (
    DateDeltaAnnotation,
    DateTimeDeltaAnnotation,
    InstantAnnotation,
    LocalDateTimeAnnotation,
    OffsetDateTimeAnnotation,
    SystemDateTimeAnnotation,
    TimeDeltaAnnotation,
    ZonedDateTimeAnnotation,
)

# ==== Tests for Core types ============================================================================================

## ---- Tests for Instant ----------------------------------------------------------------------------------------------


class InstantModel(BaseModel):
    instant: Annotated[Instant, InstantAnnotation]


@pytest.mark.parametrize(
    'instance',
    [
        Instant.now(),
        Instant.from_utc(
            year=2025,
            month=4,
            day=14,
            hour=21,
            minute=11,
            second=0,
            nanosecond=123456789,
        ),
        Instant.parse_common_iso('2025-04-14T21:11:00.123456789Z'),
    ],
)
def test_whenever_instant__existing_instance(instance: Instant):
    """Verifies that constructing a model with an existing whenever.Instant doesn't throw."""
    model = InstantModel(instant=instance)
    assert model.instant.timestamp() == instance.timestamp()


@pytest.mark.parametrize(
    'instance',
    [
        datetime.now(timezone.utc),
        datetime(
            year=2025,
            month=4,
            day=14,
            hour=21,
            minute=11,
            second=0,
            microsecond=123456,
            tzinfo=timezone.utc,
        ),
        datetime.fromtimestamp(1744665060, timezone.utc),
    ],
)
def test_whenever_instant__datetime_instance(instance: datetime):
    """Verifies that constructing a model with a datetime doesn't throw."""
    model = InstantModel(instant=instance)

    assert model.instant.timestamp() == int(instance.timestamp())
    assert isinstance(model.instant, Instant)
    assert model.instant


@pytest.mark.parametrize(
    'str_timestamp, parser',
    [
        (Instant.now().format_common_iso(), Instant.parse_common_iso),
        ('2025-04-14T21:11:00Z', Instant.parse_common_iso),
        ('2025-04-14T21:11:00.123456789Z', Instant.parse_common_iso),
        ('Mon, 14 Apr 2025 21:11:00 GMT', Instant.parse_rfc2822),
        ('Mon, 14 Apr 2025 21:11:00 UTC', Instant.parse_rfc2822),
        ('Mon, 14 Apr 2025 21:11:00 UT', Instant.parse_rfc2822),
        ('Mon, 14 Apr 2025 21:11:00 +0000', Instant.parse_rfc2822),
        ('Mon, 14 Apr 2025 21:11:00 -0000', Instant.parse_rfc2822),
        ('2025-04-14 23:11:00Z', Instant.parse_rfc3339),
        ('2025-04-14 23:11:00z', Instant.parse_rfc3339),
        ('2025-04-14T23:11:00Z', Instant.parse_rfc3339),
        ('2025-04-14t23:11:00Z', Instant.parse_rfc3339),
        ('2025-04-14t23:11:00.123456789Z', Instant.parse_rfc3339),
        ('2025-04-14t23:11:00+00:00', Instant.parse_rfc3339),
    ],
)
def test_whenever_instant_from_serialized(str_timestamp: str, parser: Callable[[str], Instant]):
    """Verifies that building an instance from serialized, well-formed strings decode properly."""
    instant_actual: Instant = parser(str_timestamp)
    model = InstantModel(instant=str_timestamp)
    assert model.instant == instant_actual
    assert type(model.instant) is Instant
    assert isinstance(model.instant, Instant)


@pytest.mark.parametrize(
    'whenever_instant',
    [
        Instant.now(),
        Instant.from_utc(
            year=2025,
            month=4,
            day=14,
            hour=21,
            minute=11,
            second=0,
            nanosecond=123456789,
        ),
        Instant.parse_common_iso('2025-04-14T21:11:00.123456789Z'),
    ],
)
def test_whenever_instant__serialization_roundtrip(whenever_instant: Instant):
    adapter = TypeAdapter(InstantAnnotation)
    json_serialized = adapter.dump_json(whenever_instant)
    deserialized = TypeAdapter.validate_json(adapter, json_serialized)
    assert deserialized == whenever_instant
    assert deserialized.timestamp() == whenever_instant.timestamp()


@pytest.mark.parametrize(
    'garbage',
    [
        None,
        'malformed',
        42,
        '12m',
        '2021-01-01T12:00:00',
        '2021-01-01T12:00:00+00:01',
        'PT1H',
        'P1DT1H',
        1744665060,
    ],
)
def test_whenever_instant__malformed(garbage):
    """Verifies that the instance fails to validate if values cannot be converted to Instant."""
    with pytest.raises(ValidationError):
        InstantModel(instant=garbage)


## ---- Tests for LocalDateTime ----------------------------------------------------------------------------------------


class LocalDateTimeModel(BaseModel):
    local_dt: Annotated[LocalDateTime, LocalDateTimeAnnotation]


@pytest.mark.parametrize(
    'instance',
    [
        LocalDateTime.from_py_datetime(datetime.now()),
        LocalDateTime(
            year=2025,
            month=4,
            day=14,
            hour=21,
            minute=11,
            second=0,
            nanosecond=123456789,
        ),
        LocalDateTime.parse_common_iso('2025-04-14T21:11:00.123456789'),
    ],
)
def test_whenever_local_date_time__existing_instance(instance: LocalDateTime):
    """Verifies that constructing a model with an existing whenever.LocalDateTime doesn't throw."""
    model = LocalDateTimeModel(local_dt=instance)
    assert model.local_dt.py_datetime() == instance.py_datetime()


@pytest.mark.parametrize(
    'instance',
    [
        datetime.now(),
        datetime(
            year=2025,
            month=4,
            day=14,
            hour=21,
            minute=11,
            second=0,
            microsecond=123456,
        ),
        datetime.fromtimestamp(1744665060),
    ],
)
def test_whenever_local_date_time__datetime_instance(instance: datetime):
    """Verifies that constructing a model with a datetime doesn't throw."""
    model = LocalDateTimeModel(local_dt=instance)

    assert model.local_dt.py_datetime() == instance
    assert isinstance(model.local_dt, LocalDateTime)
    assert model.local_dt


@pytest.mark.parametrize(
    'str_timestamp',
    [
        datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f'),
        '2025-04-14T21:11:00',
        '2025-04-14T21:11:00.123456789',
    ],
)
def test_whenever_local_date_time__from_serialized(str_timestamp: str):
    """Verifies that building an instance from serialized, well-formed strings decode properly."""
    local_dt_actual: LocalDateTime = LocalDateTime.parse_common_iso(str_timestamp)
    model = LocalDateTimeModel(local_dt=str_timestamp)
    assert model.local_dt == local_dt_actual
    assert type(model.local_dt) is LocalDateTime
    assert isinstance(model.local_dt, LocalDateTime)


@pytest.mark.parametrize(
    'whenever_local_date_time',
    [
        LocalDateTime.from_py_datetime(datetime.now()),
        LocalDateTime(
            year=2025,
            month=4,
            day=14,
            hour=21,
            minute=11,
            second=0,
            nanosecond=123456789,
        ),
        LocalDateTime.parse_common_iso('2025-04-14T21:11:00.123456789'),
    ],
)
def test_whenever_local_date_time__serialization_roundtrip(whenever_local_date_time: LocalDateTime):
    adapter = TypeAdapter(LocalDateTimeAnnotation)
    json_serialized = adapter.dump_json(whenever_local_date_time)
    deserialized = TypeAdapter.validate_json(adapter, json_serialized)
    assert deserialized == whenever_local_date_time
    assert deserialized.py_datetime() == whenever_local_date_time.py_datetime()


@pytest.mark.parametrize(
    'garbage',
    [
        None,
        'malformed',
        42,
        '12m',
        '2021-01-01T12:00:00Z',
        '2021-01-01T12:00:00+00:01',
        'PT1H',
        'P1DT1H',
    ],
)
def test_whenever_local_date_time__malformed(garbage):
    """Verifies that the instance fails to validate if values cannot be converted to LocalDateTime."""
    with pytest.raises(ValidationError):
        LocalDateTimeModel(local_dt=garbage)


## ---- Tests for ZonedDateTime ----------------------------------------------------------------------------------------


class ZonedDateTimeModel(BaseModel):
    zoned_dt: Annotated[ZonedDateTime, ZonedDateTimeAnnotation]


@pytest.mark.parametrize(
    'instance',
    [
        ZonedDateTime.from_py_datetime(datetime.now(ZoneInfo('America/Los_Angeles'))),
        ZonedDateTime(
            year=2025,
            month=4,
            day=14,
            hour=21,
            minute=11,
            second=0,
            tz='America/Los_Angeles',
        ),
        ZonedDateTime.parse_common_iso('2025-04-14T21:11:00-07:00[America/Los_Angeles]'),
    ],
)
def test_whenever_zoned_date_time__existing_instance(instance: ZonedDateTime):
    """Verifies that constructing a model with an existing whenever.ZonedDateTime doesn't throw."""
    model = ZonedDateTimeModel(zoned_dt=instance)
    assert model.zoned_dt.py_datetime() == instance.py_datetime()


@pytest.mark.parametrize(
    'instance',
    [
        datetime.now(ZoneInfo('America/Los_Angeles')),
        datetime(
            year=2025,
            month=4,
            day=14,
            hour=21,
            minute=11,
            second=0,
            microsecond=123456,
            tzinfo=ZoneInfo('America/Los_Angeles'),
        ),
    ],
)
def test_whenever_zoned_date_time__datetime_instance(instance: datetime):
    """Verifies that constructing a model with a datetime doesn't throw."""
    model = ZonedDateTimeModel(zoned_dt=instance)

    assert model.zoned_dt.py_datetime() == instance
    assert isinstance(model.zoned_dt, ZonedDateTime)
    assert model.zoned_dt


@pytest.mark.parametrize(
    'str_timestamp',
    [
        '2025-04-14T21:11:00-07:00[America/Los_Angeles]',
        '2025-04-14T21:11:00.123456789-07:00[America/Los_Angeles]',
    ],
)
def test_whenever_zoned_date_time__from_serialized(str_timestamp: str):
    """Verifies that building an instance from serialized, well-formed strings decode properly."""
    zoned_dt_actual: ZonedDateTime = ZonedDateTime.parse_common_iso(str_timestamp)
    model = ZonedDateTimeModel(zoned_dt=str_timestamp)
    assert model.zoned_dt == zoned_dt_actual
    assert type(model.zoned_dt) is ZonedDateTime
    assert isinstance(model.zoned_dt, ZonedDateTime)


@pytest.mark.parametrize(
    'whenever_zoned_date_time',
    [
        ZonedDateTime.from_py_datetime(datetime.now(ZoneInfo('America/Los_Angeles'))),
        ZonedDateTime(
            year=2025,
            month=4,
            day=14,
            hour=21,
            minute=11,
            second=0,
            tz='America/Los_Angeles',
        ),
        ZonedDateTime.parse_common_iso('2025-04-14T21:11:00-07:00[America/Los_Angeles]'),
    ],
)
def test_whenever_zoned_date_time__serialization_roundtrip(whenever_zoned_date_time: ZonedDateTime):
    adapter = TypeAdapter(ZonedDateTimeAnnotation)
    json_serialized = adapter.dump_json(whenever_zoned_date_time)
    deserialized = TypeAdapter.validate_json(adapter, json_serialized)
    assert deserialized == whenever_zoned_date_time
    assert deserialized.py_datetime() == whenever_zoned_date_time.py_datetime()


@pytest.mark.parametrize(
    'garbage',
    [
        None,
        'malformed',
        42,
        '12m',
        '2021-01-01T12:00:00Z',
        '2021-01-01T12:00:00+00:01',
        '2021-01-01T12:00:00',
        'PT1H',
        'P1DT1H',
    ],
)
def test_whenever_zoned_date_time__malformed(garbage):
    """Verifies that the instance fails to validate if values cannot be converted to ZonedDateTime."""
    with pytest.raises(ValidationError):
        ZonedDateTimeModel(zoned_dt=garbage)


# ==== Tests for Advanced types ========================================================================================

## ---- Tests for OffsetDateTime ---------------------------------------------------------------------------------------


class OffsetDateTimeModel(BaseModel):
    offset_dt: Annotated[OffsetDateTime, OffsetDateTimeAnnotation]


@pytest.mark.parametrize(
    'instance',
    [
        OffsetDateTime.from_py_datetime(datetime.now(timezone(timedelta(hours=-7)))),
        OffsetDateTime(
            year=2025,
            month=4,
            day=14,
            hour=21,
            minute=11,
            second=0,
            offset=-7,
        ),
        OffsetDateTime.parse_common_iso('2025-04-14T21:11:00-07:00'),
    ],
)
def test_whenever_offset_date_time__existing_instance(instance: OffsetDateTime):
    """Verifies that constructing a model with an existing whenever.OffsetDateTime doesn't throw."""
    model = OffsetDateTimeModel(offset_dt=instance)
    assert model.offset_dt.py_datetime() == instance.py_datetime()


@pytest.mark.parametrize(
    'instance',
    [
        datetime.now(timezone(timedelta(hours=-7))),
        datetime(
            year=2025,
            month=4,
            day=14,
            hour=21,
            minute=11,
            second=0,
            microsecond=123456,
            tzinfo=timezone(timedelta(hours=-7)),
        ),
    ],
)
def test_whenever_offset_date_time__datetime_instance(instance: datetime):
    """Verifies that constructing a model with a datetime doesn't throw."""
    model = OffsetDateTimeModel(offset_dt=instance)

    assert model.offset_dt.py_datetime() == instance
    assert isinstance(model.offset_dt, OffsetDateTime)
    assert model.offset_dt


@pytest.mark.parametrize(
    'str_timestamp,parser',
    [
        ('2025-04-14T21:11:00-07:00', OffsetDateTime.parse_common_iso),
        ('2025-04-14T21:11:00.123456789-07:00', OffsetDateTime.parse_common_iso),
        ('2025-04-14T21:11:00.123456789Z', OffsetDateTime.parse_common_iso),
        ('Mon, 14 Apr 2025 21:11:00 -0700', OffsetDateTime.parse_rfc2822),
        ('Mon, 14 Apr 2025 21:11:00 UT', OffsetDateTime.parse_rfc2822),
        ('Mon, 14 Apr 2025 21:11:00 UTC', OffsetDateTime.parse_rfc2822),
        ('Mon, 14 Apr 2025 21:11:00 GMT', OffsetDateTime.parse_rfc2822),
        ('Mon, 14 Apr 2025 21:11:00 MST', OffsetDateTime.parse_rfc2822),
        ('2025-04-14 23:11:00-07:00', OffsetDateTime.parse_rfc3339),
        ('2025-04-14T23:11:00-07:00', OffsetDateTime.parse_rfc3339),
        ('2025-04-14t23:11:00-07:00', OffsetDateTime.parse_rfc3339),
        ('2025-04-14_23:11:00-07:00', OffsetDateTime.parse_rfc3339),
        ('2025-04-14T23:11:00Z', OffsetDateTime.parse_rfc3339),
        ('2025-04-14T23:11:00z', OffsetDateTime.parse_rfc3339),
        ('2025-04-14T23:11:00.123456789-07:00', OffsetDateTime.parse_rfc3339),
    ],
)
def test_whenever_offset_date_time__from_serialized(str_timestamp: str, parser: Callable[[str], OffsetDateTime]):
    """Verifies that building an instance from serialized, well-formed strings decode properly."""
    offset_dt_actual: OffsetDateTime = parser(str_timestamp)
    model = OffsetDateTimeModel(offset_dt=str_timestamp)
    assert model.offset_dt == offset_dt_actual
    assert type(model.offset_dt) is OffsetDateTime
    assert isinstance(model.offset_dt, OffsetDateTime)


@pytest.mark.parametrize(
    'whenever_offset_date_time',
    [
        OffsetDateTime.from_py_datetime(datetime.now(timezone(timedelta(hours=-7)))),
        OffsetDateTime(
            year=2025,
            month=4,
            day=14,
            hour=21,
            minute=11,
            second=0,
            offset=-7,
        ),
        OffsetDateTime.parse_common_iso('2025-04-14T21:11:00-07:00'),
    ],
)
def test_whenever_offset_date_time__serialization_roundtrip(whenever_offset_date_time: OffsetDateTime):
    adapter = TypeAdapter(OffsetDateTimeAnnotation)
    json_serialized = adapter.dump_json(whenever_offset_date_time)
    deserialized = TypeAdapter.validate_json(adapter, json_serialized)
    assert deserialized == whenever_offset_date_time
    assert deserialized.py_datetime() == whenever_offset_date_time.py_datetime()


@pytest.mark.parametrize(
    'garbage',
    [
        None,
        'malformed',
        42,
        '12m',
        '2021-01-01T12:00:00',
        'PT1H',
        'P1DT1H',
    ],
)
def test_whenever_offset_date_time__malformed(garbage):
    """Verifies that the instance fails to validate if values cannot be converted to OffsetDateTime."""
    with pytest.raises(ValidationError):
        OffsetDateTimeModel(offset_dt=garbage)


## ---- Tests for SystemDateTime ---------------------------------------------------------------------------------------


class SystemDateTimeModel(BaseModel):
    system_dt: Annotated[SystemDateTime, SystemDateTimeAnnotation]


@pytest.mark.parametrize(
    'instance',
    [
        SystemDateTime.from_py_datetime(datetime.now(timezone(timedelta(hours=-7)))),
        SystemDateTime(
            year=2025,
            month=4,
            day=14,
            hour=21,
            minute=11,
            second=0,
        ),
        SystemDateTime.parse_common_iso('2025-04-14T21:11:00-07:00'),
    ],
)
def test_whenever_system_date_time__existing_instance(instance: SystemDateTime):
    """Verifies that constructing a model with an existing whenever.SystemDateTime doesn't throw."""
    model = SystemDateTimeModel(system_dt=instance)
    assert model.system_dt.py_datetime() == instance.py_datetime()


@pytest.mark.parametrize(
    'instance',
    [
        datetime.now(timezone(timedelta(hours=-7))),
        datetime(
            year=2025,
            month=4,
            day=14,
            hour=21,
            minute=11,
            second=0,
            microsecond=123456,
            tzinfo=timezone(timedelta(hours=-7)),
        ),
    ],
)
def test_whenever_system_date_time__datetime_instance(instance: datetime):
    """Verifies that constructing a model with a datetime doesn't throw."""
    model = SystemDateTimeModel(system_dt=instance)

    assert model.system_dt.py_datetime() == instance
    assert isinstance(model.system_dt, SystemDateTime)
    assert model.system_dt


@pytest.mark.parametrize(
    'str_timestamp',
    [
        '2025-04-14T21:11:00-07:00',
        '2025-04-14T21:11:00.123456789-07:00',
        '2025-04-14T21:11:00.123456789Z',
    ],
)
def test_whenever_system_date_time__from_serialized(str_timestamp: str):
    """Verifies that building an instance from serialized, well-formed strings decode properly."""
    system_dt_actual: SystemDateTime = SystemDateTime.parse_common_iso(str_timestamp)
    model = SystemDateTimeModel(system_dt=str_timestamp)
    assert model.system_dt == system_dt_actual
    assert type(model.system_dt) is SystemDateTime
    assert isinstance(model.system_dt, SystemDateTime)


@pytest.mark.parametrize(
    'whenever_system_date_time',
    [
        SystemDateTime.from_py_datetime(datetime.now(timezone(timedelta(hours=-7)))),
        SystemDateTime(
            year=2025,
            month=4,
            day=14,
            hour=21,
            minute=11,
            second=0,
        ),
        SystemDateTime.parse_common_iso('2025-04-14T21:11:00-07:00'),
    ],
)
def test_whenever_system_date_time__serialization_roundtrip(whenever_system_date_time: SystemDateTime):
    adapter = TypeAdapter(SystemDateTimeAnnotation)
    json_serialized = adapter.dump_json(whenever_system_date_time)
    deserialized = TypeAdapter.validate_json(adapter, json_serialized)
    assert deserialized == whenever_system_date_time
    assert deserialized.py_datetime() == whenever_system_date_time.py_datetime()


@pytest.mark.parametrize(
    'garbage',
    [
        None,
        'malformed',
        42,
        '12m',
        '2021-01-01T12:00:00',
        'PT1H',
        'P1DT1H',
    ],
)
def test_whenever_system_date_time__malformed(garbage):
    """Verifies that the instance fails to validate if values cannot be converted to SystemDateTime."""
    with pytest.raises(ValidationError):
        SystemDateTimeModel(system_dt=garbage)


# ==== Tests for Deltas ================================================================================================

## ---- Tests for TimeDelta --------------------------------------------------------------------------------------------


class TimeDeltaModel(BaseModel):
    delta_t: Annotated[TimeDelta, TimeDeltaAnnotation]


@pytest.mark.parametrize(
    'instance',
    [
        TimeDelta(milliseconds=90122),
        TimeDelta(microseconds=90122),
        TimeDelta(
            hours=25,
            seconds=732,
            milliseconds=123,
            microseconds=1324,
        ),
    ],
)
def test_whenever_timedelta__existing_instance(instance: TimeDelta):
    """Verifies that constructing a model with an existing whenever.TimeDelta doesn't throw."""
    model = TimeDeltaModel(delta_t=instance)

    assert model.delta_t.in_seconds() == instance.in_seconds()
    assert isinstance(model.delta_t, TimeDelta)
    assert model.delta_t


@pytest.mark.parametrize(
    'instance',
    [
        timedelta(days=42, hours=13, minutes=37),
        timedelta(days=-42, hours=13, minutes=37),
        timedelta(
            weeks=19,
            days=1,
            hours=25,
            seconds=732,
            milliseconds=123,
            microseconds=1324,
        ),
    ],
)
def test_whenever_timedelta__datetime_timedelta_instance(instance: timedelta):
    """Verifies that constructing a model with a datetime.timedelta doesn't throw."""
    model = TimeDeltaModel(delta_t=instance)

    assert model.delta_t.in_seconds() == instance.total_seconds()
    assert isinstance(model.delta_t, TimeDelta)
    assert model.delta_t


@pytest.mark.parametrize(
    'delta_t_str',
    [
        'PT404H',
        'PT25H',
        '-PT2M',
    ],
)
def test_whenever_timedelta__from_serialized(delta_t_str: str):
    """Verifies that building an instance from serialized, well-formed strings decode properly."""
    true_delta_t = TimeDelta.parse_common_iso(delta_t_str)
    model = TimeDeltaModel(delta_t=delta_t_str)
    assert model.delta_t == true_delta_t
    assert type(model.delta_t) is TimeDelta
    assert isinstance(model.delta_t, TimeDelta)


@pytest.mark.parametrize(
    'whenever_timedelta',
    [
        TimeDelta(milliseconds=1),
        TimeDelta(microseconds=1),
        TimeDelta(hours=1),
        TimeDelta(minutes=1),
        TimeDelta(seconds=1),
        TimeDelta(seconds=30, milliseconds=500),
    ],
)
def test_whenever_timedelta__serialization_roundtrip(whenever_timedelta: TimeDelta):
    adapter = TypeAdapter(TimeDeltaAnnotation)
    json_serialized = adapter.dump_json(whenever_timedelta)
    deserialized = TypeAdapter.validate_json(adapter, json_serialized)
    assert deserialized == whenever_timedelta
    assert deserialized.in_seconds() == whenever_timedelta.in_seconds()


@pytest.mark.parametrize(
    'garbage',
    [
        None,
        'malformed',
        42,
        '12m',
        '2021-01-01T12:00:00',
        'P1D',
        'P1DT1H',
    ],
)
def test_whenever_timedelta__malformed(garbage):
    """Verifies that the instance fails to validate if values cannot be converted to TimeDelta."""
    with pytest.raises(ValidationError):
        TimeDeltaModel(delta_t=garbage)


## ---- Tests for DateDelta --------------------------------------------------------------------------------------------


class DateDeltaModel(BaseModel):
    delta_d: Annotated[DateDelta, DateDeltaAnnotation]


@pytest.mark.parametrize(
    'instance',
    [
        DateDelta(weeks=9000),
        DateDelta(days=9000),
        DateDelta(years=25, weeks=732, days=123),
    ],
)
def test_whenever_datedelta__existing_instance(instance: DateDelta):
    """Verifies that constructing a model with an existing whenever.DateDelta doesn't throw."""
    model = DateDeltaModel(delta_d=instance)

    assert model.delta_d.in_years_months_days() == instance.in_years_months_days()
    assert isinstance(model.delta_d, DateDelta)
    assert model.delta_d


@pytest.mark.parametrize(
    'delta_d_str',
    [
        'P25Y7M1W5D',
        'P25D',
        '-P2M',
    ],
)
def test_whenever_datedelta__from_serialized(delta_d_str: str):
    """Verifies that building an instance from serialized, well-formed strings decode properly."""
    true_delta_d = DateDelta.parse_common_iso(delta_d_str)
    model = DateDeltaModel(delta_d=delta_d_str)
    assert model.delta_d == true_delta_d
    assert type(model.delta_d) is DateDelta
    assert isinstance(model.delta_d, DateDelta)


@pytest.mark.parametrize(
    'whenever_datedelta',
    [
        DateDelta(weeks=9000),
        DateDelta(days=9000),
        DateDelta(years=25, weeks=732, days=123),
    ],
)
def test_whenever_datedelta__serialization_roundtrip(whenever_datedelta: DateDelta):
    adapter = TypeAdapter(DateDeltaAnnotation)
    json_serialized = adapter.dump_json(whenever_datedelta)
    deserialized = TypeAdapter.validate_json(adapter, json_serialized)
    assert deserialized == whenever_datedelta
    assert deserialized.in_years_months_days() == whenever_datedelta.in_years_months_days()


@pytest.mark.parametrize(
    'garbage',
    [
        None,
        'malformed',
        42,
        '12m',
        '2021-01-01T12:00:00',
        'PT1H',
        'P1DT1H',
    ],
)
def test_whenever_datedelta__malformed(garbage):
    """Verifies that the instance fails to validate if values cannot be converted to DateDelta."""
    with pytest.raises(ValidationError):
        DateDeltaModel(delta_d=garbage)


## ---- Tests for DateTimeDelta ----------------------------------------------------------------------------------------


class DateTimeDeltaModel(BaseModel):
    delta_dt: Annotated[DateTimeDelta, DateTimeDeltaAnnotation]


@pytest.mark.parametrize(
    'instance',
    [
        DateTimeDelta(milliseconds=1),
        DateTimeDelta(microseconds=1),
        DateTimeDelta(hours=1),
        DateTimeDelta(minutes=1),
        DateTimeDelta(seconds=1),
        DateTimeDelta(seconds=30, milliseconds=500),
        DateTimeDelta(weeks=9000),
        DateTimeDelta(days=9000),
        DateTimeDelta(years=25, weeks=732, days=123),
        DateTimeDelta(days=13, hours=21),
        DateTimeDelta(
            years=25,
            weeks=732,
            days=123,
            hours=1,
            minutes=1,
            seconds=30,
            milliseconds=500,
        ),
    ],
)
def test_whenever_datetimedelta__existing_instance(instance: DateTimeDelta):
    """Verifies that constructing a model with an existing whenever.DateTimeDelta doesn't throw."""
    model = DateTimeDeltaModel(delta_dt=instance)

    assert model.delta_dt.in_months_days_secs_nanos() == instance.in_months_days_secs_nanos()
    assert isinstance(model.delta_dt, DateTimeDelta)
    assert model.delta_dt


@pytest.mark.parametrize(
    'delta_dt_str',
    [
        'P25Y732W123DT1H1M30.500S',
        'P25D',
        'PT23H',
        '-P2M',
        '-PT2M',
        '-P2MT2M',
    ],
)
def test_whenever_datetimedelta__from_serialized(delta_dt_str: str):
    """Verifies that building an instance from serialized, well-formed strings decode properly."""
    true_delta_dt = DateTimeDelta.parse_common_iso(delta_dt_str)
    model = DateTimeDeltaModel(delta_dt=delta_dt_str)
    assert model.delta_dt == true_delta_dt
    assert type(model.delta_dt) is DateTimeDelta
    assert isinstance(model.delta_dt, DateTimeDelta)


@pytest.mark.parametrize(
    'whenever_datetimedelta',
    [
        DateTimeDelta(weeks=9000),
        DateTimeDelta(hours=9000),
        DateTimeDelta(days=123, hours=321),
    ],
)
def test_whenever_datetimedelta__serialization_roundtrip(whenever_datetimedelta: DateTimeDelta):
    adapter = TypeAdapter(DateTimeDeltaAnnotation)
    json_serialized = adapter.dump_json(whenever_datetimedelta)
    deserialized = TypeAdapter.validate_json(adapter, json_serialized)
    assert deserialized == whenever_datetimedelta
    assert deserialized.in_months_days_secs_nanos() == whenever_datetimedelta.in_months_days_secs_nanos()


@pytest.mark.parametrize(
    'garbage',
    [
        None,
        'malformed',
        42,
        '12m',
        '2021-01-01T12:00:00',
    ],
)
def test_whenever_datetimedelta__malformed(garbage):
    """Verifies that the instance fails to validate if values cannot be converted to DateTimeDelta."""
    with pytest.raises(ValidationError):
        DateTimeDeltaModel(delta_dt=garbage)
