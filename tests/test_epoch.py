import datetime

import pytest

from pydantic_extra_types.epoch import Epoch

@pytest.mark.parametrize('type_',[(int,),(float,)], ids=["integer", "float"])
def test_type(type_):
    from pydantic import BaseModel

    class A(BaseModel):
        epoch: Epoch

    now = datetime.datetime.now(tz=datetime.timezone.utc)
    ts = type_(now.timestamp())
    a = A.model_validate({"epoch":ts})
    v = a.model_dump()
    assert v["epoch"] == ts

    b = A.model_construct(epoch=now)

    v = b.model_dump()
    assert v["epoch"] == ts

    c = A.model_validate(dict(epoch=ts))
    v = c.model_dump()
    assert v["epoch"] == ts


def test_schema():
    from pydantic import BaseModel
    class A(BaseModel):
        dt: Epoch

    v = A.model_json_schema()
    assert (dt:=v["properties"]["dt"])["type"] == "number" and dt["format"] == "date-time"

