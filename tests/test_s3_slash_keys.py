import pytest
from pydantic import TypeAdapter, ValidationError

from pydantic_extra_types.s3 import S3Path


@pytest.mark.parametrize(
    'key,last_key',
    [('folder//', 'folder'), ('parent/child///', 'child'), ('/', ''), ('///', ''), ('line\n//', 'line\n')],
)
@pytest.mark.parametrize('via_adapter', [False, True])
def test_s3_preserves_slash_suffixed_keys(key: str, last_key: str, via_adapter: bool) -> None:
    value = 's3://bucket/' + key
    path = TypeAdapter(S3Path).validate_python(value) if via_adapter else S3Path(value)
    assert path.bucket == 'bucket'
    assert path.key == key
    assert path.last_key == last_key
    assert str(path) == value
    adapter = TypeAdapter(S3Path)
    assert adapter.validate_json(adapter.dump_json(path)).key == key


def test_s3_empty_key_is_still_invalid() -> None:
    with pytest.raises(ValueError, match='Invalid S3 path'):
        S3Path('s3://bucket/')
    with pytest.raises(ValidationError):
        TypeAdapter(S3Path).validate_python('s3://bucket/')
