import uuid
from datetime import datetime, timezone
from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

from pydantic_extra_types.uuid_types import UUID6, UUID7, UUID8, uuid7, uuid7_to_datetime


# ---- Models ----


class ModelUUID7(BaseModel):
    id: UUID7


class ModelUUID6(BaseModel):
    id: UUID6


class ModelUUID8(BaseModel):
    id: UUID8


# ---- UUID7 validation tests ----

# A known valid UUID v7 string (version nibble = 7, variant = RFC 4122)
VALID_UUID7_STR = '018f0e8c-7a6a-7b1c-a3e4-fdf3e0ef7a4a'
VALID_UUID7_OBJ = uuid.UUID(VALID_UUID7_STR)

# A valid UUID v4 (should be rejected for UUID7 field)
VALID_UUID4_STR = 'a7b3d4e1-1c2d-4f3e-8a5b-6c7d8e9f0a1b'


@pytest.mark.parametrize(
    'value, valid',
    [
        # Valid UUID v7 as string
        (VALID_UUID7_STR, True),
        # Valid UUID v7 as uuid.UUID object
        (VALID_UUID7_OBJ, True),
        # UUID v4 should be rejected
        (VALID_UUID4_STR, False),
        # UUID v1 should be rejected
        ('6ba7b810-9dad-11d1-80b4-00c04fd430c8', False),
        # Not a valid UUID at all
        ('not-a-uuid', False),
        # Empty string
        ('', False),
    ],
)
def test_uuid7_validation(value: Any, valid: bool) -> None:
    if valid:
        m = ModelUUID7(id=value)
        assert m.id.version == 7
        assert isinstance(m.id, uuid.UUID)
    else:
        with pytest.raises(ValidationError):
            ModelUUID7(id=value)


def test_uuid7_serialization() -> None:
    m = ModelUUID7(id=VALID_UUID7_STR)
    dumped = m.model_dump()
    assert dumped['id'] == VALID_UUID7_OBJ

    json_str = m.model_dump_json()
    assert VALID_UUID7_STR in json_str


def test_uuid7_json_schema() -> None:
    schema = ModelUUID7.model_json_schema()
    assert schema['properties']['id']['type'] == 'string'
    assert schema['properties']['id']['format'] == 'uuid'


# ---- UUID6 validation tests ----

VALID_UUID6_STR = '1ef21d2f-6aa3-6d00-a327-541a2bda5190'


@pytest.mark.parametrize(
    'value, valid',
    [
        (VALID_UUID6_STR, True),
        (uuid.UUID(VALID_UUID6_STR), True),
        # UUID v4 should be rejected
        (VALID_UUID4_STR, False),
    ],
)
def test_uuid6_validation(value: Any, valid: bool) -> None:
    if valid:
        m = ModelUUID6(id=value)
        assert m.id.version == 6
    else:
        with pytest.raises(ValidationError):
            ModelUUID6(id=value)


def test_uuid6_json_schema() -> None:
    schema = ModelUUID6.model_json_schema()
    assert schema['properties']['id']['type'] == 'string'
    assert schema['properties']['id']['format'] == 'uuid'


# ---- UUID8 validation tests ----

VALID_UUID8_STR = '00112233-4455-8677-8899-aabbccddeeff'


@pytest.mark.parametrize(
    'value, valid',
    [
        (VALID_UUID8_STR, True),
        (uuid.UUID(VALID_UUID8_STR), True),
        # UUID v4 should be rejected
        (VALID_UUID4_STR, False),
    ],
)
def test_uuid8_validation(value: Any, valid: bool) -> None:
    if valid:
        m = ModelUUID8(id=value)
        assert m.id.version == 8
    else:
        with pytest.raises(ValidationError):
            ModelUUID8(id=value)


def test_uuid8_json_schema() -> None:
    schema = ModelUUID8.model_json_schema()
    assert schema['properties']['id']['type'] == 'string'
    assert schema['properties']['id']['format'] == 'uuid'


# ---- uuid7() generation tests ----


def test_uuid7_generation() -> None:
    generated = uuid7()
    assert isinstance(generated, uuid.UUID)
    assert generated.version == 7


def test_uuid7_generation_is_unique() -> None:
    ids = {uuid7() for _ in range(100)}
    assert len(ids) == 100


def test_uuid7_generation_is_sortable() -> None:
    """UUID v7 should be roughly time-ordered."""
    ids = [uuid7() for _ in range(10)]
    assert ids == sorted(ids)


def test_uuid7_generation_validates() -> None:
    """Generated UUID v7 should pass the UUID7 type validation."""
    generated = uuid7()
    m = ModelUUID7(id=str(generated))
    assert m.id.version == 7


# ---- uuid7_to_datetime tests ----


def test_uuid7_to_datetime() -> None:
    u = uuid.UUID(VALID_UUID7_STR)
    dt = uuid7_to_datetime(u)
    assert isinstance(dt, datetime)
    assert dt.tzinfo == timezone.utc
    # The known UUID 018f0e8c-7a6a corresponds to timestamp_ms = 0x018f0e8c7a6a
    expected_ms = 0x018F0E8C7A6A
    expected_dt = datetime.fromtimestamp(expected_ms / 1000.0, tz=timezone.utc)
    assert dt == expected_dt


def test_uuid7_to_datetime_roundtrip() -> None:
    """Generate a UUID v7, extract the datetime, and verify it is recent."""
    generated = uuid7()
    dt = uuid7_to_datetime(generated)
    now = datetime.now(tz=timezone.utc)
    # The extracted time should be within 2 seconds of now
    assert abs((now - dt).total_seconds()) < 2


def test_uuid7_to_datetime_wrong_version() -> None:
    """Should raise ValueError for non-v7 UUIDs."""
    u4 = uuid.UUID(VALID_UUID4_STR)
    with pytest.raises(ValueError, match='Expected UUID version 7'):
        uuid7_to_datetime(u4)
