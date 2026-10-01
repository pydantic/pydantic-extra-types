import pytest
from pydantic import TypeAdapter

from pydantic_extra_types.s3 import S3Path


@pytest.mark.parametrize(
    'key,last_key',
    [
        ('directory/\n', '\n'),
        ('directory\n/file.txt', 'file.txt'),
        ('first\n/second\n/file.txt', 'file.txt'),
        ('directory\n/file.txt/', 'file.txt'),
        ('directory\r\n/file.txt', 'file.txt'),
        ('directory/file\n.txt', 'file\n.txt'),
    ],
)
@pytest.mark.parametrize('use_adapter', [False, True])
def test_s3_preserves_newlines_in_object_keys(key: str, last_key: str, use_adapter: bool) -> None:
    raw = 's3://bucket/' + key
    path = TypeAdapter(S3Path).validate_python(raw) if use_adapter else S3Path(raw)
    assert path.bucket == 'bucket'
    assert path.key == key
    assert path.last_key == last_key
    assert str(path) == raw
