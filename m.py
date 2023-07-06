from pydantic import BaseModel, validator
from pydantic_extra_types.pandas_types import Series
import pandas as pd


"""
from typing import Any, Type, TypeVar

import pandas as pd
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema

T = TypeVar('T', str, bytes, bool, int, float, complex, pd.Timestamp, pd.Timedelta, pd.Period)


class Series(pd.Series):  # type: ignore
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
        return cls(__input_value)
"""


class Model(BaseModel):
    x: Series


m = Model(x=[1, 2, 4])
s = pd.Series([1, 2, 4])
t = Series(data=[1, 2, 4], index=["a", "b", "d"])

print(m)
print(m.x)

print(s)

print(m.x == s)

print(isinstance(m.x, pd.Series))

print(t)
print(t.index)
