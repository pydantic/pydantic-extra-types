import pytest
from httpx import URL as URL_HTTPX
from pydantic import BaseModel, ValidationError

from pydantic_extra_types.httpx_url import URL

from .too_long_url import TOO_LONG_URL


class CheckingModel(BaseModel):
    url: URL


def test_url_ok():
    model = CheckingModel(url='https://www.example.com')
    assert isinstance(model.url, URL_HTTPX)
    assert model.url == 'https://www.example.com'
    assert model.model_dump() == {'url': 'https://www.example.com'}  # test serialization


@pytest.mark.parametrize('invalid_url', ['', '\0', TOO_LONG_URL])
def test_url_fail(invalid_url: str):
    with pytest.raises(ValidationError):
        CheckingModel(url='\0')
