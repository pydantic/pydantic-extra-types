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
