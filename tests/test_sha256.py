import pytest
from pydantic import BaseModel, ValidationError

from pydantic_extra_types.sha256 import Sha256Str

EMPTY_SHA256 = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'


class Artifact(BaseModel):
    checksum: Sha256Str


@pytest.mark.parametrize('value', [EMPTY_SHA256, EMPTY_SHA256.upper(), f'  {EMPTY_SHA256}\n'])
def test_valid_sha256(value: str) -> None:
    checksum = Artifact(checksum=value).checksum
    assert checksum == EMPTY_SHA256
    assert isinstance(checksum, Sha256Str)


def test_sha256_from_json() -> None:
    artifact = Artifact.model_validate_json(f'{{"checksum": "{EMPTY_SHA256.upper()}"}}')
    assert artifact.checksum == EMPTY_SHA256
    assert artifact.model_dump_json() == f'{{"checksum":"{EMPTY_SHA256}"}}'


@pytest.mark.parametrize(
    'value',
    [
        '',
        EMPTY_SHA256[:-1],
        EMPTY_SHA256 + '0',
        'g' + EMPTY_SHA256[1:],
        '0x' + EMPTY_SHA256[2:],
        EMPTY_SHA256[:30] + ' ' + EMPTY_SHA256[31:],
        EMPTY_SHA256[:-1] + '\u0663',
    ],
)
def test_invalid_sha256(value: str) -> None:
    with pytest.raises(ValidationError, match='string_pattern_mismatch'):
        Artifact(checksum=value)


def test_sha256_not_a_string() -> None:
    with pytest.raises(ValidationError, match='string_type'):
        Artifact(checksum=1234)
