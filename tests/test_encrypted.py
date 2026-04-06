from __future__ import annotations

from typing import Annotated, Optional

import pytest
from pydantic import BaseModel, Field, ValidationError

from pydantic_extra_types.encrypted import CipherString


def encrypt(value: str) -> str:
    return f'enc::{value}'


def decrypt(value: str) -> str:
    if not value.startswith('enc::'):
        raise ValueError('invalid encrypted value')
    return value[5:]


class EncryptRequestModel(BaseModel):
    value: Annotated[str, CipherString.encrypt(encrypt)]


class DecryptResponseModel(BaseModel):
    value: Annotated[str, CipherString.decrypt(decrypt)]


class ConstrainedDecryptModel(BaseModel):
    value: Annotated[str, Field(min_length=3), CipherString.decrypt(decrypt)]


class OptionalEncryptModel(BaseModel):
    value: Annotated[Optional[str], CipherString.encrypt(encrypt)]


def test_encrypt_after_validation() -> None:
    result = EncryptRequestModel(value='abc')
    assert result.value == 'enc::abc'


def test_decrypt_before_validation() -> None:
    result = DecryptResponseModel(value='enc::abc')
    assert result.value == 'abc'


def test_before_mode_runs_prior_to_constraints() -> None:
    with pytest.raises(ValidationError, match='at least 3 characters'):
        ConstrainedDecryptModel(value='enc::ab')


def test_optional_value_none_is_untouched() -> None:
    assert OptionalEncryptModel(value=None).value is None


def test_invalid_mode() -> None:
    with pytest.raises(ValueError, match='`mode` must be either "before" or "after"'):
        CipherString(transform=encrypt, mode='invalid')  # type: ignore[arg-type]


def test_non_callable_transform() -> None:
    with pytest.raises(ValueError, match='`transform` must be callable'):
        CipherString(transform='not-callable')  # type: ignore[arg-type]


def test_transform_exception_bubbles_as_validation_error() -> None:
    with pytest.raises(ValidationError, match='Failed to transform value'):
        DecryptResponseModel(value='plain-value')


def test_transform_must_return_string() -> None:
    def bad_transform(value: str) -> str:
        return 1  # type: ignore[return-value]

    class BadModel(BaseModel):
        value: Annotated[str, CipherString.encrypt(bad_transform)]

    with pytest.raises(ValidationError, match='Transform function must return a string'):
        BadModel(value='abc')


def test_non_string_input() -> None:
    with pytest.raises(ValidationError, match='Input should be a valid string'):
        DecryptResponseModel(value=123)  # type: ignore[arg-type]


def test_json_schema_remains_string() -> None:
    assert EncryptRequestModel.model_json_schema() == {
        'properties': {'value': {'title': 'Value', 'type': 'string'}},
        'required': ['value'],
        'title': 'EncryptRequestModel',
        'type': 'object',
    }


def test_classmethod_constructors() -> None:
    encrypt_transformer = CipherString.encrypt(encrypt)
    decrypt_transformer = CipherString.decrypt(decrypt)

    assert encrypt_transformer.mode == 'after'
    assert decrypt_transformer.mode == 'before'
