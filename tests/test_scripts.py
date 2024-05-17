import re

import pycountry
import pytest
from pydantic import BaseModel, ValidationError

from pydantic_extra_types.script_code import ISO_15924


class ScriptCheck(BaseModel):
    script: ISO_15924


@pytest.mark.parametrize('script', map(lambda lang: lang.alpha_4, pycountry.scripts))
def test_ISO_15924_code_ok(script: str):
    model = ScriptCheck(script=script)
    assert model.script == script
    assert str(model.script) == script
    assert model.model_dump() == {'script': script}  # test serialization


def test_ISO_15924_code_fail_not_enought_letters():
    with pytest.raises(
        ValidationError,
        match=re.escape(
            '1 validation error for ScriptCheck\nscript\n  '
            "String should have at least 4 characters [type=string_too_short, input_value='X', input_type=str]\n"
        ),
    ):
        ScriptCheck(script='X')


def test_ISO_15924_code_fail_too_much_letters():
    with pytest.raises(
        ValidationError,
        match=re.escape(
            '1 validation error for ScriptCheck\nscript\n  '
            "String should have at most 4 characters [type=string_too_long, input_value='Klingon', input_type=str]"
        ),
    ):
        ScriptCheck(script='Klingon')


def test_ISO_15924_code_fail_not_existing():
    with pytest.raises(
        ValidationError,
        match=re.escape(
            '1 validation error for ScriptCheck\nscript\n  '
            'Invalid ISO 15924 script code. See https://en.wikipedia.org/wiki/ISO_15924 '
            "[type=ISO_15924, input_value='Klin', input_type=str]"
        ),
    ):
        ScriptCheck(script='Klin')
