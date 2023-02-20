from typing import Any, ClassVar, Dict, Optional

from pydantic_core import PydanticCustomError, core_schema
from zxcvbn import zxcvbn


class PasswordStr(str):
    min_length: ClassVar[int] = 8
    max_length: ClassVar[int] = 72
    strip_whitespace: ClassVar[bool] = True
    _password_strength: Optional[Dict[str, Any]] = None

    def __new__(cls, password: str) -> 'PasswordStr':
        return super().__new__(cls, password)

    def __init__(self, password: str):
        self.validate_length(password)
        self._password_strength = zxcvbn(password)  # type: ignore

    @classmethod
    def __get_pydantic_core_schema__(cls, **_kwargs: Any) -> core_schema.FunctionSchema:
        return core_schema.function_after_schema(
            core_schema.str_schema(
                min_length=cls.min_length, max_length=cls.max_length, strip_whitespace=cls.strip_whitespace
            ),
            cls.validate,
        )

    @classmethod
    def validate(cls, __input_value: str, **_kwargs: Any) -> 'PasswordStr':
        return cls(__input_value)

    @classmethod
    def validate_length(cls, password: str) -> None:
        if len(password) < cls.min_length:
            raise PydanticCustomError(
                'password_length',
                'Password must be at least {min_length} characters',
                {'min_length': cls.min_length},
            )
        if len(password) > cls.max_length:
            raise PydanticCustomError(
                'password_length',
                'Password must be at most {max_length} characters',
                {'max_length': cls.max_length},
            )

    @property
    def strength(self) -> Dict[str, Any]:
        if self._password_strength is None:
            raise ValueError('Password strength not calculated')
        return self._password_strength
