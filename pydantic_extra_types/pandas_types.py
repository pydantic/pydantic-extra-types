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
