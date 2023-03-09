from typing import Any

import pytest
from pydantic_core import PydanticCustomError

from pydantic import BaseModel
from pydantic_extra_types import PasswordStr


def test_password_str_length():
    # Test password length validation
    with pytest.raises(PydanticCustomError):
        PasswordStr('short')
    with pytest.raises(PydanticCustomError):
        PasswordStr('x' * 73)

    # Test valid password
    p = PasswordStr('validpassword')
    assert p == 'validpassword'


def test_password_str_strength():
    # Test password strength calculation
    p = PasswordStr('weakpassword')
    assert p.strength['score'] < 3

    p = PasswordStr('strongpassword123')
    assert p.strength['score'] >= 1


class Data(BaseModel):
    password: PasswordStr

    def __init__(self, **data: Any):
        super().__init__(**data)

    def __repr__(self) -> str:
        return f'Data(password={self.password})'


def test_password_str_model():
    # Test password strength calculation
    d = Data(password='weakpassword')
    assert d.password.strength['score'] < 3
    d = Data(password='strongpassword123')
    assert d.password.strength['score'] >= 1
