"""convenient URL type compatible with httpx and pydantic mostly useful in settings for base url of httpx client"""
from typing import Any

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import core_schema

try:
    from httpx import URL as URL_HTTPX
    from httpx._exceptions import InvalidURL
    from httpx._urlparse import MAX_URL_LENGTH
except ImportError:
    raise RuntimeError(
        'The `httpx` module requires "httpx" to be installed. You can install it with "pip install ' 'httpx".'
    )


class URL(URL_HTTPX):
    """URL parses URL in the [httpx.URL](https://www.python-httpx.org/api/#url) format.

    ```py
    from pydantic import BaseModel

    from pydantic_extra_types.httpx_url import URL

    class Website(BaseModel):
        url: URL

    website = Website(url='https://www.example.com')
    print(website)
    # > url='https://www.example.com'
    ```
    """

    @classmethod
    def _validate(cls, url: str, _: core_schema.ValidationInfo) -> 'URL':
        """
        Validate a URL from the provided str value.

        Args:
            url: The str value to be validated.
            _: The Pydantic ValidationInfo.

        Returns:
            The validated URL.
        """
        try:
            return cls(url)
        except InvalidURL as e:
            raise ValueError(str(e))

    @classmethod
    def __get_pydantic_core_schema__(cls, type: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        """
        duplicate of the `AnyUrl` schema, but with the `URL` type from httpx.
        """
        return core_schema.with_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(min_length=1, max_length=MAX_URL_LENGTH),
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> dict[str, Any]:
        """
        duplicate of the `AnyUrl` schema, but with the `URL` type from httpx.
        """
        json_schema = handler(schema)
        return json_schema
