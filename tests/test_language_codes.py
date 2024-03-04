import re
from string import printable

import pycountry
import pytest
from pydantic import BaseModel, ValidationError

from pydantic_extra_types import language_code
from pydantic_extra_types.language_code import (
    LanguageAlpha2,
    LanguageInfo,
    LanguageName,
    _index_by_alpha2,
    _index_by_alpha3,
    _index_by_name,
)

PARAMS_AMOUNT = 20


@pytest.fixture(scope='module', name='MovieAlpha2')
def movie_alpha2_fixture():
    class Movie(BaseModel):
        audio_lang: LanguageAlpha2

    return Movie


@pytest.fixture(scope='module', name='MovieName')
def movie_name_fixture():
    class Movie(BaseModel):
        audio_lang: LanguageName

    return Movie


class ISO3CheckingModel(BaseModel):
    lang: language_code.ISO639_3


class ISO5CheckingModel(BaseModel):
    lang: language_code.ISO639_5


@pytest.mark.parametrize('alpha2, language_data', list(_index_by_alpha2().items()))
def test_valid_alpha2(alpha2: str, language_data: LanguageInfo, MovieAlpha2):
    the_godfather = MovieAlpha2(audio_lang=alpha2)
    assert the_godfather.audio_lang == language_data.alpha2
    assert the_godfather.audio_lang.alpha3 == language_data.alpha3
    assert the_godfather.audio_lang.name == language_data.name


@pytest.mark.parametrize('alpha2', list(printable) + list(_index_by_alpha3().keys())[:PARAMS_AMOUNT])
def test_invalid_alpha2(alpha2: str, MovieAlpha2):
    with pytest.raises(ValidationError, match='Invalid language alpha2 code'):
        MovieAlpha2(audio_lang=alpha2)


@pytest.mark.parametrize('name, language_data', list(_index_by_name().items())[:PARAMS_AMOUNT])
def test_valid_name(name: str, language_data: LanguageInfo, MovieName):
    the_godfather = MovieName(audio_lang=name)
    assert the_godfather.audio_lang == language_data.name
    assert the_godfather.audio_lang.alpha2 == language_data.alpha2
    assert the_godfather.audio_lang.alpha3 == language_data.alpha3


@pytest.mark.parametrize('name', set(printable) - {'E', 'U'})  # E and U are valid language codes
def test_invalid_name(name: str, MovieName):
    with pytest.raises(ValidationError, match='Invalid language name'):
        MovieName(audio_lang=name)


@pytest.mark.parametrize('lang', map(lambda lang: lang.alpha_3, pycountry.languages))
def test_iso_ISO639_3_code_ok(lang: str):
    model = ISO3CheckingModel(lang=lang)
    assert model.lang == lang
    assert model.model_dump() == {'lang': lang}  # test serialization


@pytest.mark.parametrize('lang', map(lambda lang: lang.alpha_3, pycountry.language_families))
def test_iso_639_5_code_ok(lang: str):
    model = ISO5CheckingModel(lang=lang)
    assert model.lang == lang
    assert model.model_dump() == {'lang': lang}  # test serialization


def test_iso3_language_fail():
    with pytest.raises(
        ValidationError,
        match=re.escape(
            '1 validation error for ISO3CheckingModel\nlang\n  '
            'Invalid ISO 639-3 language code. '
            "See https://en.wikipedia.org/wiki/ISO_639-3 [type=ISO649_3, input_value='LOL', input_type=str]"
        ),
    ):
        ISO3CheckingModel(lang='LOL')


def test_iso5_language_fail():
    with pytest.raises(
        ValidationError,
        match=re.escape(
            '1 validation error for ISO5CheckingModel\nlang\n  '
            'Invalid ISO 639-5 language code. '
            "See https://en.wikipedia.org/wiki/ISO_639-5 [type=ISO649_5, input_value='LOL', input_type=str]"
        ),
    ):
        ISO5CheckingModel(lang='LOL')
