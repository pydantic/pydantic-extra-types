"""Currency definitions that are based on the [ISO4217](https://en.wikipedia.org/wiki/ISO_4217)."""

from __future__ import annotations

from typing import Any

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import PydanticCustomError, core_schema

try:
    import pycountry
except ModuleNotFoundError as e:  # pragma: no cover
    raise RuntimeError(
        'The `currency_code` module requires "pycountry" to be installed. You can install it with "pip install '
        'pycountry".'
    ) from e

# List of codes that should not be usually used within regular transactions
_CODES_FOR_BONDS_METAL_TESTING = {
    'XTS',  # testing
    'XAU',  # gold
    'XAG',  # silver
    'XPD',  # palladium
    'XPT',  # platinum
    'XBA',  # Bond Markets Unit European Composite Unit (EURCO)
    'XBB',  # Bond Markets Unit European Monetary Unit (E.M.U.-6)
    'XBC',  # Bond Markets Unit European Unit of Account 9 (E.U.A.-9)
    'XBD',  # Bond Markets Unit European Unit of Account 17 (E.U.A.-17)
    'XXX',  # no currency
    'XDR',  # SDR (Special Drawing Right)
}


class ISO4217(str):
    """ISO4217 parses Currency in the [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217) format.

    ```py
    from pydantic import BaseModel

    from pydantic_extra_types.currency_code import ISO4217


    class Currency(BaseModel):
        alpha_3: ISO4217


    currency = Currency(alpha_3='AED')
    print(currency)
    # > alpha_3='AED'
    ```
    """

    allowed_countries_list = [country.alpha_3 for country in pycountry.currencies]
    allowed_currencies = set(allowed_countries_list)

    @classmethod
    def _validate(cls, currency_code: str, _: core_schema.ValidationInfo) -> str:
        """Validate a ISO 4217 language code from the provided str value.

        Args:
            currency_code: The str value to be validated.
            _: The Pydantic ValidationInfo.

        Returns:
            The validated ISO 4217 currency code.

        Raises:
            PydanticCustomError: If the ISO 4217 currency code is not valid.
        """
        currency_code = currency_code.upper()
        if currency_code not in cls.allowed_currencies:
            raise PydanticCustomError(
                'ISO4217', 'Invalid ISO 4217 currency code. See https://en.wikipedia.org/wiki/ISO_4217'
            )
        return currency_code

    @classmethod
    def __get_pydantic_core_schema__(cls, _: type[Any], __: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.with_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(min_length=3, max_length=3),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> dict[str, Any]:
        json_schema = handler(schema)
        json_schema.update({'enum': cls.allowed_countries_list})
        return json_schema


class Currency(str):
    """Currency parses currency subset of the [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217) format.
    It excludes bonds testing codes and precious metals.
        ```py
        from pydantic import BaseModel

        from pydantic_extra_types.currency_code import Currency


        class currency(BaseModel):
            alpha_3: Currency


        cur = currency(alpha_3='AED')
        print(cur)
        # > alpha_3='AED'
        ```
    """

    allowed_countries_list = list(
        filter(lambda x: x not in _CODES_FOR_BONDS_METAL_TESTING, ISO4217.allowed_countries_list)
    )
    allowed_currencies = set(allowed_countries_list)

    @classmethod
    def _validate(cls, currency_symbol: str, _: core_schema.ValidationInfo) -> str:
        """Validate a subset of the [ISO4217](https://en.wikipedia.org/wiki/ISO_4217) format.
        It excludes bonds testing codes and precious metals.

        Args:
            currency_symbol: The str value to be validated.
            _: The Pydantic ValidationInfo.

        Returns:
            The validated ISO 4217 currency code.

        Raises:
            PydanticCustomError: If the ISO 4217 currency code is not valid or is bond, precious metal or testing code.
        """
        currency_symbol = currency_symbol.upper()
        if currency_symbol not in cls.allowed_currencies:
            raise PydanticCustomError(
                'InvalidCurrency',
                'Invalid currency code.'
                ' See https://en.wikipedia.org/wiki/ISO_4217 . '
                'Bonds, testing and precious metals codes are not allowed.',
            )
        return currency_symbol

    @classmethod
    def __get_pydantic_core_schema__(cls, _: type[Any], __: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        """Return a Pydantic CoreSchema with the currency subset of the
        [ISO4217](https://en.wikipedia.org/wiki/ISO_4217) format.
        It excludes bonds testing codes and precious metals.

        Args:
             _: The source type.
             __: The handler to get the CoreSchema.

        Returns:
            A Pydantic CoreSchema with the subset of the currency subset of the
            [ISO4217](https://en.wikipedia.org/wiki/ISO_4217) format.
            It excludes bonds testing codes and precious metals.
        """
        return core_schema.with_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(min_length=3, max_length=3),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> dict[str, Any]:
        """Return a Pydantic JSON Schema with subset of the [ISO4217](https://en.wikipedia.org/wiki/ISO_4217) format.
        Excluding bonds testing codes and precious metals.

        Args:
            schema: The Pydantic CoreSchema.
            handler: The handler to get the JSON Schema.

        Returns:
            A Pydantic JSON Schema with the subset of the ISO4217 currency code validation. without bonds testing codes
            and precious metals.

        """
        json_schema = handler(schema)
        json_schema.update({'enum': cls.allowed_countries_list})
        return json_schema
