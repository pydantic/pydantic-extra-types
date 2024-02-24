import re

import pycountry
import pytest
from pydantic import BaseModel, ValidationError

from pydantic_extra_types import language_code


class ISO3CheckingModel(BaseModel):
    lang: language_code.ISO639_3


class ISO5CheckingModel(BaseModel):
    lang: language_code.ISO639_5


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
