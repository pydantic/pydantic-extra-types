import datetime

import pytest

from pydantic_extra_types import epoch


@pytest.mark.parametrize('type_,cls_', [(int, epoch.Integer), (float, epoch.Number)], ids=['integer', 'number'])
def test_type(type_, cls_):
    from pydantic import BaseModel

    class A(BaseModel):
        epoch: cls_

    now = datetime.datetime.now(tz=datetime.timezone.utc)
    ts = type_(now.timestamp())
    a = A.model_validate({'epoch': ts})
    v = a.model_dump()
    assert v['epoch'] == ts

    b = A.model_construct(epoch=now)

    v = b.model_dump()
    assert v['epoch'] == ts

    c = A.model_validate({'epoch': ts})
    v = c.model_dump()
    assert v['epoch'] == ts


@pytest.mark.parametrize('cls_', [(epoch.Integer), (epoch.Number)], ids=['integer', 'number'])
def test_schema(cls_):
    from pydantic import BaseModel

    class A(BaseModel):
        dt: cls_

    v = A.model_json_schema()
    assert (dt := v['properties']['dt'])['type'] == cls_.TYPE and dt['format'] == 'date-time'


@pytest.mark.parametrize('cls_', [epoch.Integer, epoch.Number], ids=['integer', 'number'])
def test_out_of_range_raises_validation_error(cls_):
    # A too-large timestamp (e.g. a JS millisecond epoch accidentally fed to a seconds
    # field) overflows past datetime.max. It must surface as a ValidationError, not a raw
    # OverflowError that escapes validate_python.
    from pydantic import TypeAdapter, ValidationError

    ta = TypeAdapter(cls_)
    with pytest.raises(ValidationError):
        ta.validate_python(1_721_000_000_000)


@pytest.mark.parametrize(
    'value', [10**400, -(10**400), '1' + '0' * 400], ids=['positive', 'negative', 'numeric-string']
)
def test_integer_too_large_for_float_raises_validation_error(value):
    # math.isfinite() cannot convert an int this large to a float and raises
    # OverflowError, which must not escape validate_python.
    from pydantic import TypeAdapter, ValidationError

    ta = TypeAdapter(epoch.Integer)
    with pytest.raises(ValidationError, match='timestamp is out of the supported datetime range'):
        ta.validate_python(value)


@pytest.mark.parametrize('value', [float('nan'), float('inf'), float('-inf')])
def test_non_finite_raises_validation_error(value):
    from pydantic import TypeAdapter, ValidationError

    ta = TypeAdapter(epoch.Number)
    with pytest.raises(ValidationError, match='timestamp must be a finite number'):
        ta.validate_python(value)


@pytest.mark.parametrize('cls_', [epoch.Integer, epoch.Number], ids=['integer', 'number'])
@pytest.mark.parametrize(
    'value',
    [
        datetime.datetime(2024, 1, 1, 12, 30, 15, tzinfo=datetime.timezone.utc),
        datetime.datetime(2024, 1, 1, 12, 30, 15, tzinfo=datetime.timezone(datetime.timedelta(hours=2))),
    ],
    ids=['utc', 'offset'],
)
def test_aware_datetime_input_is_returned_unchanged(cls_, value):
    from pydantic import TypeAdapter

    result = TypeAdapter(cls_).validate_python(value)
    assert result == value
    assert result.tzinfo is value.tzinfo


@pytest.mark.parametrize(
    'cls_,error_type', [(epoch.Integer, 'int_type'), (epoch.Number, 'float_type')], ids=['integer', 'number']
)
def test_naive_datetime_input_is_still_rejected(cls_, error_type):
    # A naive datetime would be serialized with .timestamp(), which reads it as local time,
    # so the number written would depend on the host timezone.
    from pydantic import TypeAdapter, ValidationError

    with pytest.raises(ValidationError) as exc_info:
        TypeAdapter(cls_).validate_python(datetime.datetime(2024, 1, 1, 12, 30, 15))
    assert exc_info.value.errors()[0]['type'] == error_type


@pytest.mark.parametrize('cls_,number', [(epoch.Integer, 1), (epoch.Number, 1.5)], ids=['integer', 'number'])
def test_validated_value_validates_again_on_assignment(cls_, number):
    # The value of the field is a datetime, so assignment validation must accept it back.
    from pydantic import BaseModel, ConfigDict

    class LogEntry(BaseModel):
        model_config = ConfigDict(validate_assignment=True)
        ts: cls_

    entry = LogEntry(ts=number)
    value = entry.ts
    entry.ts = entry.ts
    assert entry.ts == value
    assert LogEntry(ts=value) == entry
    assert entry.model_dump() == {'ts': number}


@pytest.mark.parametrize('cls_,number', [(epoch.Integer, 1), (epoch.Number, 1.5)], ids=['integer', 'number'])
def test_validated_value_validates_again_on_revalidation(cls_, number):
    from pydantic import BaseModel, ConfigDict

    class LogEntry(BaseModel):
        ts: cls_

    class Outer(BaseModel):
        model_config = ConfigDict(revalidate_instances='always')
        inner: LogEntry

    entry = LogEntry(ts=number)
    assert Outer(inner=entry).inner == entry
    assert Outer.model_validate({'inner': {'ts': entry.ts}}).inner == entry


def test_integer_serialization_truncates_a_datetime_with_microseconds():
    # A datetime passed in directly is held as is and serialized with int(timestamp), as in test_type.
    from pydantic import TypeAdapter

    ta = TypeAdapter(epoch.Integer)
    after = ta.validate_python(datetime.datetime(1970, 1, 1, 0, 0, 1, 500000, tzinfo=datetime.timezone.utc))
    before = ta.validate_python(datetime.datetime(1969, 12, 31, 23, 59, 59, 500000, tzinfo=datetime.timezone.utc))
    assert ta.dump_python(after) == 1
    assert ta.dump_python(before) == 0


@pytest.mark.parametrize('cls_', [epoch.Integer, epoch.Number], ids=['integer', 'number'])
def test_json_mode_accepts_numbers_only(cls_):
    from pydantic import TypeAdapter, ValidationError

    ta = TypeAdapter(cls_)
    assert ta.validate_json('1') == datetime.datetime(1970, 1, 1, 0, 0, 1, tzinfo=datetime.timezone.utc)
    with pytest.raises(ValidationError):
        ta.validate_json('"2024-01-01T00:00:00Z"')


@pytest.mark.parametrize('cls_', [epoch.Integer, epoch.Number], ids=['integer', 'number'])
def test_python_mode_non_number_keeps_the_number_error(cls_):
    # Not a datetime and not a number: still the number error
    from pydantic import TypeAdapter, ValidationError

    with pytest.raises(ValidationError, match='valid (integer|number)'):
        TypeAdapter(cls_).validate_python('not a number')
