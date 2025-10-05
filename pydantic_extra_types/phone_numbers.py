"""The `pydantic_extra_types.phone_numbers` module provides the
[`PhoneNumber`][pydantic_extra_types.phone_numbers.PhoneNumber] data type.

This class depends on the [phonenumbers](https://pypi.orgt/phonenumbers/) package,
which is a Python port of Google's [libphonenumber](https://github.com/google/libphonenumber/).
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from functools import partial
from typing import Any, ClassVar

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import PydanticCustomError, core_schema

try:
    import phonenumbers
    from phonenumbers import PhoneNumber as BasePhoneNumber
    from phonenumbers.phonenumberutil import NumberParseException
except ModuleNotFoundError as e:  # pragma: no cover
    raise RuntimeError(
        '`PhoneNumber` requires "phonenumbers" to be installed. You can install it with "pip install phonenumbers"'
    ) from e


class PhoneNumber(str):
    """A wrapper around the `phonenumbers.PhoneNumber` object.

    It provides class-level configuration points you can change by subclassing:

    ## Examples

    ### Normal usage:

    ```python
        from pydantic import BaseModel
        from pydantic_extra_types.phone_numbers import PhoneNumber

        class Contact(BaseModel):
            name: str
            phone: PhoneNumber

        c = Contact(name='Alice', phone='+1 650-253-0000')
        print(c.phone)
        >> tel:+1-650-253-0000 (formatted using RFC3966 by default)
    ```

    ### Changing defaults by subclassing:

    ```python
        from pydantic_extra_types.phone_numbers import PhoneNumber

        class USPhone(PhoneNumber):
            default_region_code = 'US'
            supported_regions = ['US']
            phone_format = 'NATIONAL'

        # Now parsing will accept national numbers for the US
        p = USPhone('650-253-0000')
        print(p)
        >> 650-253-0000
    ```

    ### Changing defaults by using the provided validator annotation:

    ```python
        from typing import Annotated, Union
        import phonenumbers
        from pydantic import BaseModel
        from pydantic_extra_types.phone_numbers import PhoneNumberValidator

        E164NumberType = Annotated[
            Union[str, phonenumbers.PhoneNumber], PhoneNumberValidator(number_format="E164")
        ]


        class Model(BaseModel):
            phone: E164NumberType


        m = Model(phone="+1 650-253-0000")
        print(m.phone)
        >> +16502530000
    ```

    """

    default_region_code: ClassVar[str | None] = None
    """The default region code to use when parsing phone numbers without an international prefix."""

    supported_regions: list[str] = []
    """The supported regions. If empty, all regions are supported."""

    phone_format: str = 'RFC3966'
    """The format of the phone number."""

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> dict[str, Any]:
        json_schema = handler(schema)
        json_schema.update({'format': 'phone'})
        return json_schema

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.with_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(),
        )

    @classmethod
    def _validate(cls, phone_number: str, _: core_schema.ValidationInfo) -> str:
        try:
            parsed_number = phonenumbers.parse(phone_number, cls.default_region_code)
        except phonenumbers.phonenumberutil.NumberParseException as exc:
            raise PydanticCustomError('value_error', 'value is not a valid phone number') from exc
        if not phonenumbers.is_valid_number(parsed_number):
            raise PydanticCustomError('value_error', 'value is not a valid phone number')

        if cls.supported_regions and not any(
            phonenumbers.is_valid_number_for_region(parsed_number, region_code=region)
            for region in cls.supported_regions
        ):
            raise PydanticCustomError('value_error', 'value is not from a supported region')

        return phonenumbers.format_number(parsed_number, getattr(phonenumbers.PhoneNumberFormat, cls.phone_format))

    def __eq__(self, other: Any) -> bool:
        return super().__eq__(other)

    def __hash__(self) -> int:
        return super().__hash__()


@dataclass(frozen=True)
class PhoneNumberValidator:
    """An annotation to validate `phonenumbers.PhoneNumber` objects.

    Example:
        ```python
        from typing import Annotated, Union

        import phonenumbers
        from pydantic import BaseModel
        from pydantic_extra_types.phone_numbers import PhoneNumberValidator

        MyNumberType = Annotated[Union[str, phonenumbers.PhoneNumber], PhoneNumberValidator()]

        USNumberType = Annotated[
            Union[str, phonenumbers.PhoneNumber], PhoneNumberValidator(supported_regions=['US'], default_region='US')
        ]


        class SomeModel(BaseModel):
            phone_number: MyNumberType
            us_number: USNumberType
        ```
    """

    default_region: str | None = None
    """The default region code to use when parsing phone numbers without an international prefix.

    If `None` (the default), the region must be supplied in the phone number as an international prefix.
    """

    number_format: str = 'RFC3966'
    """The format of the phone number to return. See `phonenumbers.PhoneNumberFormat` for valid values."""

    supported_regions: Sequence[str] | None = None
    """The supported regions. If empty (the default), all regions are supported."""

    def __post_init__(self) -> None:
        if self.default_region and self.default_region not in phonenumbers.SUPPORTED_REGIONS:
            raise ValueError(f'Invalid default region code: {self.default_region}')

        if self.number_format not in (
            number_format
            for number_format in dir(phonenumbers.PhoneNumberFormat)
            if not number_format.startswith('_') and number_format.isupper()
        ):
            raise ValueError(f'Invalid number format: {self.number_format}')

        if self.supported_regions:
            for supported_region in self.supported_regions:
                if supported_region not in phonenumbers.SUPPORTED_REGIONS:
                    raise ValueError(f'Invalid supported region code: {supported_region}')

    @staticmethod
    def _parse(
        region: str | None,
        number_format: str,
        supported_regions: Sequence[str] | None,
        phone_number: Any,
    ) -> str:
        if not phone_number:
            raise PydanticCustomError('value_error', 'value is not a valid phone number')

        if not isinstance(phone_number, (str, BasePhoneNumber)):
            raise PydanticCustomError('value_error', 'value is not a valid phone number')

        parsed_number = None
        if isinstance(phone_number, BasePhoneNumber):
            parsed_number = phone_number
        else:
            try:
                parsed_number = phonenumbers.parse(phone_number, region=region)
            except NumberParseException as exc:
                raise PydanticCustomError('value_error', 'value is not a valid phone number') from exc

        if not phonenumbers.is_valid_number(parsed_number):
            raise PydanticCustomError('value_error', 'value is not a valid phone number')

        if supported_regions and not any(
            phonenumbers.is_valid_number_for_region(parsed_number, region_code=region) for region in supported_regions
        ):
            raise PydanticCustomError('value_error', 'value is not from a supported region')

        return phonenumbers.format_number(parsed_number, getattr(phonenumbers.PhoneNumberFormat, number_format))

    def __get_pydantic_core_schema__(self, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.no_info_before_validator_function(
            partial(
                self._parse,
                self.default_region,
                self.number_format,
                self.supported_regions,
            ),
            core_schema.str_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> dict[str, Any]:
        json_schema = handler(schema)
        json_schema.update({'format': 'phone'})
        return json_schema

    def __hash__(self) -> int:
        return super().__hash__()
