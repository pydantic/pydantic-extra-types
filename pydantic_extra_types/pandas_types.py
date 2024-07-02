from __future__ import annotations

from typing import Any

import pandas as pd
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema


class Series(pd.Series):  # type: ignore
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.BeforeValidatorFunctionSchema:
        return core_schema.general_before_validator_function(
            cls._validate,
            core_schema.any_schema(),
        )

    @classmethod
    def _validate(cls, __input_value: Any, _: core_schema.ValidationInfo) -> Series:
        return cls(__input_value)
