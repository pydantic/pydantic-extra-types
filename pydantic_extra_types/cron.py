"""The `pydantic_extra_types.cron` module provides the [`CronStr`][pydantic_extra_types.cron.CronStr] data type."""

from __future__ import annotations

from datetime import datetime
from typing import Any, ClassVar

try:
    from cron_converter import Cron
    from cron_converter.sub_modules.seeker import Seeker as CronSeeker
except ModuleNotFoundError as e:  # pragma: no cover
    raise RuntimeError(
        'The `cron` module requires "cron-converter" to be installed. You can install it with "pip install cron-converter".'
    ) from e
from pydantic import GetCoreSchemaHandler
from pydantic_core import PydanticCustomError, core_schema


class CronStr(str):
    """A cron expression validated via [`cron-converter`](https://pypi.org/project/cron-converter/).
    ## Examples
    ```python
        from pydantic import BaseModel
        from pydantic_extra_types.cron import CronStr

        class Schedule(BaseModel):
            cron: CronStr

        schedule = Schedule(cron="*/5 * * * *")
        print(schedule.cron)
        >> */5 * * * *
        print(schedule.cron.minute)
        >> */5
        print(schedule.cron.next_run)
        >> 2025-10-07T22:40:00+00:00
    ```
    """

    strip_whitespace: ClassVar[bool] = True
    """Whether to strip surrounding whitespace from the input value."""
    _component_names: ClassVar[tuple[str, ...]] = (
        'minute',
        'hour',
        'day_of_the_month',
        'month',
        'day_of_the_week',
    )
    """Expected cron expression components in the order enforced by `cron-converter`."""

    minute: str
    hour: str
    day_of_the_month: str
    month: str
    day_of_the_week: str
    cron_obj: Cron

    def __new__(cls, cron_expression: str, *, _cron: Cron | None = None) -> CronStr:
        if _cron is None:
            cron_expression, cron_obj = cls._validate(cron_expression)
        else:
            cron_obj = _cron
            cron_expression = cron_obj.to_string()

        obj = super().__new__(cls, cron_expression)
        obj._apply_cron(cron_obj)
        return obj

    def _apply_cron(self, cron_obj: Cron) -> None:
        self.cron_obj = cron_obj
        self.minute, self.hour, self.day_of_the_month, self.month, self.day_of_the_week = str(self).split()

    @classmethod
    def _validate(cls, value: Any) -> tuple[str, Cron]:
        if not isinstance(value, str):
            raise PydanticCustomError('cron_str_type', 'Cron expression must be a string')

        cron_expression = value.strip()
        if not cron_expression:
            raise PydanticCustomError('cron_str_empty', 'Cron expression must not be empty')

        parts = cron_expression.split()
        if len(parts) != len(cls._component_names):
            parts_list = ', '.join(cls._component_names)
            raise PydanticCustomError(
                'cron_str_components',
                f'Cron expression must contain {len(cls._component_names)} space separated components: {parts_list}',
            )

        try:
            cron_obj = Cron(cron_expression)
        except (TypeError, ValueError) as exc:
            raise PydanticCustomError('cron_str_invalid', str(exc)) from exc

        # `cron-converter` may normalise components (e.g. remove duplicate spaces),
        # so we reuse its canonical representation.
        return cron_obj.to_string(), cron_obj

    @classmethod
    def validate(cls, __input_value: Any, _: core_schema.ValidationInfo) -> CronStr:
        cron_expression, cron_obj = cls._validate(__input_value)
        return cls(cron_expression, _cron=cron_obj)

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.with_info_after_validator_function(
            cls.validate,
            core_schema.str_schema(strip_whitespace=cls.strip_whitespace),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetCoreSchemaHandler
    ) -> dict[str, Any]:
        return dict(handler(schema))

    def schedule(self, start_date: datetime | None = None, timezone_str: str | None = None) -> CronSeeker:
        """Return the iterator produced by `cron-converter` for this expression."""
        return self.cron_obj.schedule(start_date=start_date, timezone_str=timezone_str)

    def next_after(self, start_date: datetime | None = None, timezone_str: str | None = None) -> datetime:
        """Return the first run datetime after `start_date` (or now if omitted)."""
        seeker = self.schedule(start_date=start_date, timezone_str=timezone_str)
        return seeker.next()

    @property
    def next_run(self) -> str:
        """Return the next run as an ISO formatted string (shortcut for backwards compatibility)."""
        return self.next_after().isoformat()
