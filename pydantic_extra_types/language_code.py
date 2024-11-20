"""Language definitions that are based on the [ISO 639-3](https://en.wikipedia.org/wiki/ISO_639-3) & [ISO 639-5](https://en.wikipedia.org/wiki/ISO_639-5)."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Union

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import PydanticCustomError, core_schema

try:
    import pycountry
except ModuleNotFoundError as e:  # pragma: no cover
    raise RuntimeError(
        'The `language_code` module requires "pycountry" to be installed.'
        ' You can install it with "pip install pycountry".'
    ) from e


@dataclass
class LanguageInfo:
    """LanguageInfo is a dataclass that contains the language information.

    Args:
        alpha2: The language code in the [ISO 639-1 alpha-2](https://en.wikipedia.org/wiki/ISO_639-1) format.
        alpha3: The language code in the [ISO 639-3 alpha-3](https://en.wikipedia.org/wiki/ISO_639-3) format.
        name: The language name.
    """

    alpha2: Union[str, None]
    alpha3: str
    name: str


@lru_cache
def _languages() -> list[LanguageInfo]:
    """Return a list of LanguageInfo objects containing the language information.

    Returns:
        A list of LanguageInfo objects containing the language information.
    """
    return [
        LanguageInfo(
            alpha2=getattr(language, 'alpha_2', None),
            alpha3=language.alpha_3,
            name=language.name,
        )
        for language in pycountry.languages
    ]


@lru_cache
def _index_by_alpha2() -> dict[str, LanguageInfo]:
    """Return a dictionary with the language code in the [ISO 639-1 alpha-2](https://en.wikipedia.org/wiki/ISO_639-1) format as the key and the LanguageInfo object as the value."""
    return {language.alpha2: language for language in _languages() if language.alpha2 is not None}


@lru_cache
def _index_by_alpha3() -> dict[str, LanguageInfo]:
    """Return a dictionary with the language code in the [ISO 639-3 alpha-3](https://en.wikipedia.org/wiki/ISO_639-3) format as the key and the LanguageInfo object as the value."""
    return {language.alpha3: language for language in _languages()}


@lru_cache
def _index_by_name() -> dict[str, LanguageInfo]:
    """Return a dictionary with the language name as the key and the LanguageInfo object as the value."""
    return {language.name: language for language in _languages()}


class LanguageAlpha2(str):
    """LanguageAlpha2 parses languages codes in the [ISO 639-1 alpha-2](https://en.wikipedia.org/wiki/ISO_639-1)
    format.

    ```py
    from pydantic import BaseModel

    from pydantic_extra_types.language_code import LanguageAlpha2


    class Movie(BaseModel):
        audio_lang: LanguageAlpha2
        subtitles_lang: LanguageAlpha2


    movie = Movie(audio_lang='de', subtitles_lang='fr')
    print(movie)
    # > audio_lang='de' subtitles_lang='fr'
    ```
    """

    @classmethod
    def _validate(cls, __input_value: str, _: core_schema.ValidationInfo) -> LanguageAlpha2:
        """Validate a language code in the ISO 639-1 alpha-2 format from the provided str value.

        Args:
            __input_value: The str value to be validated.
            _: The Pydantic ValidationInfo.

        Returns:
            The validated language code in the ISO 639-1 alpha-2 format.
        """
        if __input_value not in _index_by_alpha2():
            raise PydanticCustomError('language_alpha2', 'Invalid language alpha2 code')
        return cls(__input_value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.AfterValidatorFunctionSchema:
        """Return a Pydantic CoreSchema with the language code in the ISO 639-1 alpha-2 format validation.

        Args:
            source: The source type.
            handler: The handler to get the CoreSchema.

        Returns:
            A Pydantic CoreSchema with the language code in the ISO 639-1 alpha-2 format validation.
        """
        return core_schema.with_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(to_lower=True),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> dict[str, Any]:
        """Return a Pydantic JSON Schema with the language code in the ISO 639-1 alpha-2 format validation.

        Args:
            schema: The Pydantic CoreSchema.
            handler: The handler to get the JSON Schema.

        Returns:
            A Pydantic JSON Schema with the language code in the ISO 639-1 alpha-2 format validation.
        """
        json_schema = handler(schema)
        json_schema.update({'pattern': r'^\w{2}$'})
        return json_schema

    @property
    def alpha3(self) -> str:
        """The language code in the [ISO 639-3 alpha-3](https://en.wikipedia.org/wiki/ISO_639-3) format."""
        return _index_by_alpha2()[self].alpha3

    @property
    def name(self) -> str:
        """The language name."""
        return _index_by_alpha2()[self].name


class LanguageName(str):
    """LanguageName parses languages names listed in the [ISO 639-3 standard](https://en.wikipedia.org/wiki/ISO_639-3)
    format.

    ```py
    from pydantic import BaseModel

    from pydantic_extra_types.language_code import LanguageName


    class Movie(BaseModel):
        audio_lang: LanguageName
        subtitles_lang: LanguageName


    movie = Movie(audio_lang='Dutch', subtitles_lang='Mandarin Chinese')
    print(movie)
    # > audio_lang='Dutch' subtitles_lang='Mandarin Chinese'
    ```
    """

    @classmethod
    def _validate(cls, __input_value: str, _: core_schema.ValidationInfo) -> LanguageName:
        """Validate a language name from the provided str value.

        Args:
            __input_value: The str value to be validated.
            _: The Pydantic ValidationInfo.

        Returns:
            The validated language name.
        """
        if __input_value not in _index_by_name():
            raise PydanticCustomError('language_name', 'Invalid language name')
        return cls(__input_value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.AfterValidatorFunctionSchema:
        """Return a Pydantic CoreSchema with the language name validation.

        Args:
            source: The source type.
            handler: The handler to get the CoreSchema.

        Returns:
            A Pydantic CoreSchema with the language name validation.
        """
        return core_schema.with_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )

    @property
    def alpha2(self) -> Union[str, None]:
        """The language code in the [ISO 639-1 alpha-2](https://en.wikipedia.org/wiki/ISO_639-1) format. Does not exist for all languages."""
        return _index_by_name()[self].alpha2

    @property
    def alpha3(self) -> str:
        """The language code in the [ISO 639-3 alpha-3](https://en.wikipedia.org/wiki/ISO_639-3) format."""
        return _index_by_name()[self].alpha3


class ISO639_3(str):
    """ISO639_3 parses Language in the [ISO 639-3 alpha-3](https://en.wikipedia.org/wiki/ISO_639-3_alpha-3)
    format.

    ```py
    from pydantic import BaseModel

    from pydantic_extra_types.language_code import ISO639_3


    class Language(BaseModel):
        alpha_3: ISO639_3


    lang = Language(alpha_3='ssr')
    print(lang)
    # > alpha_3='ssr'
    ```
    """

    allowed_values_list = [lang.alpha_3 for lang in pycountry.languages]
    allowed_values = set(allowed_values_list)

    @classmethod
    def _validate(cls, __input_value: str, _: core_schema.ValidationInfo) -> ISO639_3:
        """Validate a ISO 639-3 language code from the provided str value.

        Args:
            __input_value: The str value to be validated.
            _: The Pydantic ValidationInfo.

        Returns:
            The validated ISO 639-3 language code.

        Raises:
            PydanticCustomError: If the ISO 639-3 language code is not valid.
        """
        if __input_value not in cls.allowed_values:
            raise PydanticCustomError(
                'ISO649_3', 'Invalid ISO 639-3 language code. See https://en.wikipedia.org/wiki/ISO_639-3'
            )
        return cls(__input_value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, _: type[Any], __: GetCoreSchemaHandler
    ) -> core_schema.AfterValidatorFunctionSchema:
        """Return a Pydantic CoreSchema with the ISO 639-3 language code validation.

        Args:
            _: The source type.
            __: The handler to get the CoreSchema.

        Returns:
            A Pydantic CoreSchema with the ISO 639-3 language code validation.

        """
        return core_schema.with_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(min_length=3, max_length=3),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> dict[str, Any]:
        """Return a Pydantic JSON Schema with the ISO 639-3 language code validation.

        Args:
            schema: The Pydantic CoreSchema.
            handler: The handler to get the JSON Schema.

        Returns:
            A Pydantic JSON Schema with the ISO 639-3 language code validation.

        """
        json_schema = handler(schema)
        json_schema.update({'enum': cls.allowed_values_list})
        return json_schema


class ISO639_5(str):
    """ISO639_5 parses Language in the [ISO 639-5 alpha-3](https://en.wikipedia.org/wiki/ISO_639-5_alpha-3)
    format.

    ```py
    from pydantic import BaseModel

    from pydantic_extra_types.language_code import ISO639_5


    class Language(BaseModel):
        alpha_3: ISO639_5


    lang = Language(alpha_3='gem')
    print(lang)
    # > alpha_3='gem'
    ```
    """

    allowed_values_list = [lang.alpha_3 for lang in pycountry.language_families]
    allowed_values_list.sort()
    allowed_values = set(allowed_values_list)

    @classmethod
    def _validate(cls, __input_value: str, _: core_schema.ValidationInfo) -> ISO639_5:
        """Validate a ISO 639-5 language code from the provided str value.

        Args:
            __input_value: The str value to be validated.
            _: The Pydantic ValidationInfo.

        Returns:
            The validated ISO 639-3 language code.

        Raises:
            PydanticCustomError: If the ISO 639-5 language code is not valid.
        """
        if __input_value not in cls.allowed_values:
            raise PydanticCustomError(
                'ISO649_5', 'Invalid ISO 639-5 language code. See https://en.wikipedia.org/wiki/ISO_639-5'
            )
        return cls(__input_value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, _: type[Any], __: GetCoreSchemaHandler
    ) -> core_schema.AfterValidatorFunctionSchema:
        """Return a Pydantic CoreSchema with the ISO 639-5 language code validation.

        Args:
            _: The source type.
            __: The handler to get the CoreSchema.

        Returns:
            A Pydantic CoreSchema with the ISO 639-5 language code validation.

        """
        return core_schema.with_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(min_length=3, max_length=3),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> dict[str, Any]:
        """Return a Pydantic JSON Schema with the ISO 639-5 language code validation.

        Args:
            schema: The Pydantic CoreSchema.
            handler: The handler to get the JSON Schema.

        Returns:
            A Pydantic JSON Schema with the ISO 639-5 language code validation.

        """
        json_schema = handler(schema)
        json_schema.update({'enum': cls.allowed_values_list})
        return json_schema
