from datetime import datetime, timezone
from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

from pydantic_extra_types.ulid import ULID

try:
    from ulid import ULID as _ULID
except ModuleNotFoundError:  # pragma: no cover
    raise RuntimeError(
        'The `ulid` module requires "python-ulid" to be installed. You can install it with "pip install python-ulid".'
    )


class Something(BaseModel):
    ulid: ULID


@pytest.mark.parametrize(
    'ulid, result, valid',
    [
        # Valid ULID for str format
        ('01BTGNYV6HRNK8K8VKZASZCFPE', '01BTGNYV6HRNK8K8VKZASZCFPE', True),
        ('01BTGNYV6HRNK8K8VKZASZCFPF', '01BTGNYV6HRNK8K8VKZASZCFPF', True),
        # Invalid ULID for str format
        ('01BTGNYV6HRNK8K8VKZASZCFP', None, False),  # Invalid ULID (short length)
        ('01BTGNYV6HRNK8K8VKZASZCFPEA', None, False),  # Invalid ULID (long length)
        # Valid ULID for _ULID format
        (_ULID.from_str('01BTGNYV6HRNK8K8VKZASZCFPE'), '01BTGNYV6HRNK8K8VKZASZCFPE', True),
        (_ULID.from_str('01BTGNYV6HRNK8K8VKZASZCFPF'), '01BTGNYV6HRNK8K8VKZASZCFPF', True),
        # Invalid _ULID for bytes format
        (b'\x01\xba\x1e\xb2\x8a\x9f\xfay\x10\xd5\xa5k\xc8', None, False),  # Invalid ULID (short length)
        (b'\x01\xba\x1e\xb2\x8a\x9f\xfay\x10\xd5\xa5k\xc8\xb6\x00', None, False),  # Invalid ULID (long length)
        # Valid ULID for int format
        (109667145845879622871206540411193812282, '2JG4FVY7N8XS4GFVHPXGJZ8S9T', True),
        (109667145845879622871206540411193812283, '2JG4FVY7N8XS4GFVHPXGJZ8S9V', True),
        (109667145845879622871206540411193812284, '2JG4FVY7N8XS4GFVHPXGJZ8S9W', True),
    ],
)
def test_format_for_ulid(ulid: Any, result: Any, valid: bool):
    if valid:
        assert str(Something(ulid=ulid).ulid) == result
    else:
        with pytest.raises(ValidationError, match='format'):
            Something(ulid=ulid)


def test_property_for_ulid():
    ulid = Something(ulid='01BTGNYV6HRNK8K8VKZASZCFPE').ulid
    assert ulid.hex == '015ea15f6cd1c56689a373fab3f63ece'
    assert ulid == '01BTGNYV6HRNK8K8VKZASZCFPE'
    assert ulid.datetime == datetime(2017, 9, 20, 22, 18, 59, 153000, tzinfo=timezone.utc)
    assert ulid.timestamp == 1505945939.153


def test_json_schema():
    assert Something.model_json_schema(mode='validation') == {
        'properties': {
            'ulid': {
                'anyOf': [{'type': 'integer'}, {'format': 'binary', 'type': 'string'}, {'type': 'string'}],
                'title': 'Ulid',
            }
        },
        'required': ['ulid'],
        'title': 'Something',
        'type': 'object',
    }
    assert Something.model_json_schema(mode='serialization') == {
        'properties': {
            'ulid': {
                'anyOf': [{'type': 'integer'}, {'format': 'binary', 'type': 'string'}, {'type': 'string'}],
                'title': 'Ulid',
            }
        },
        'required': ['ulid'],
        'title': 'Something',
        'type': 'object',
    }
