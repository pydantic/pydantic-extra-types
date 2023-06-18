from pydantic import BaseModel

from pydantic_extra_types.iban import Iban


class Anything(BaseModel):
    iban: Iban


def test_valid_iban() -> None:
    Anything(iban='DE89370400440532013000')
