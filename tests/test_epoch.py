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

    c = A.model_validate(dict(epoch=ts))
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
