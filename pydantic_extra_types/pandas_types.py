from typing import Any, List, Tuple, Type, TypeVar, Union

from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema

try:
    import pandas as pd
except ModuleNotFoundError:  # pragma: no cover
    raise RuntimeError(
        '`Series` requires "pandas" to be installed. You can install it with "pip install pandas"'
    )

T = TypeVar('T', str, bytes, bool, int, float, complex, pd.Timestamp, pd.Timedelta, pd.Period)


class Series:
    def __init__(self, value: Any) -> None:
        self.value = pd.Series(value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: Type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.AfterValidatorFunctionSchema:
        return core_schema.general_after_validator_function(
            cls._validate,
            core_schema.any_schema(),
        )

    @classmethod
    def _validate(cls, __input_value: Any, _: core_schema.ValidationInfo) -> 'Series':
        if isinstance(__input_value, pd.Series):
            return cls(__input_value)
        return cls(pd.Series(__input_value))

    def __repr__(self) -> str:
        return repr(self.value)

    def __getattr__(self, name: str) -> Any:
        return getattr(self.value, name)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, (pd.Series, Series))

    def __add__(self, other: Union['Series', List[Any], Tuple[Any], T]) -> 'Series':
        if isinstance(other, Series):
            result_val = self.value + other.value
        else:
            result_val = self.value + other
        return Series(result_val)
