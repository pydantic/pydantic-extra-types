import pytest
from pydantic import BaseModel, ValidationError

from pydantic_extra_types.domain import DomainStr


class MyModel(BaseModel):
    domain: DomainStr


very_long_domains_list = [
    'sub1.sub2.sub3.sub4.sub5.sub6.sub7.sub8.sub9.sub10.sub11.sub12.sub13.sub14.sub15.sub16.sub17.sub18.sub19.sub20.sub21.sub22.sub23.sub24.sub25.sub26.sub27.sub28.sub29.sub30.sub31.sub32.sub33.extremely-long-domain-name-example-to-test-the-253-character-limit.com',
    'a-very-very-long-subdomain-name-that-continues-forever-and-ever-testing-the-length-limit-of-domains-to-make-sure-it-reaches-beyond-the-maximum-allowed-for-experimentation-and-testing-purposes.extremely-extended-domain-name-example-for-253-characters-limit.net',
]


@pytest.mark.parametrize('domain', ['a.com', 'x.com'])
def test_single_letter_domain(domain: str):
    MyModel.model_validate({'domain': domain})


@pytest.mark.parametrize('domain', very_long_domains_list)
def test_domains_over_253_characters(domain: str):
    assert len(domain) > 253
    try:
        MyModel.model_validate({'domain': domain})
        raise Exception('Domain did not throw an error for having over 253 characters')
    except ValidationError:
        # An error is expected on this test
        pass


@pytest.mark.parametrize('domain', [''])
def test_domains_having_less_than_one_character(domain: str):
    try:
        MyModel.model_validate({'domain': domain})
        raise Exception('Domain did not throw an error for having less than 1 character')
    except ValidationError:
        # An error is expected on this test
        pass
