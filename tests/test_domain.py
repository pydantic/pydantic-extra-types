from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

from pydantic_extra_types.domain import DomainStr


class MyModel(BaseModel):
    domain: DomainStr


valid_domains = [
    'example.com',
    'sub.example.com',
    'sub-domain.example-site.co.uk',
    'a.com',
    'x.com',
    '1.2.3.4.5.6.7.8.9.10.11.12.13.14.15.com',  # Multiple subdomains
]

invalid_domains = [
    '',  # Empty string
    'example',  # Missing TLD
    '.com',  # Missing domain name
    'example.',  # Trailing dot
    'exam ple.com',  # Space in domain
    'exa_mple.com',  # Underscore in domain
    'example.com.',  # Trailing dot
]

very_long_domains = [
    'a' * 249 + '.com',  # Just under the limit
    'a' * 250 + '.com',  # At the limit
    'a' * 251 + '.com',  # Just over the limit
    'sub1.sub2.sub3.sub4.sub5.sub6.sub7.sub8.sub9.sub10.sub11.sub12.sub13.sub14.sub15.sub16.sub17.sub18.sub19.sub20.sub21.sub22.sub23.sub24.sub25.sub26.sub27.sub28.sub29.sub30.sub31.sub32.sub33.extremely-long-domain-name-example-to-test-the-253-character-limit.com',
]

invalid_domain_types = [1, 2, 1.1, 2.1, False, [], {}, None]


@pytest.mark.parametrize('domain', valid_domains)
def test_valid_domains(domain: str):
    try:
        MyModel.model_validate({'domain': domain})
        assert len(domain) < 254 and len(domain) > 0
    except ValidationError:
        assert len(domain) > 254 or len(domain) == 0


@pytest.mark.parametrize('domain', invalid_domains)
def test_invalid_domains(domain: str):
    try:
        MyModel.model_validate({'domain': domain})
        raise Exception(
            f"This test case has only samples that should raise a ValidationError. This domain '{domain}' did not raise such an exception."
        )
    except ValidationError:
        # An error is expected on this test
        pass


@pytest.mark.parametrize('domain', very_long_domains)
def test_very_long_domains(domain: str):
    try:
        MyModel.model_validate({'domain': domain})
        assert len(domain) < 254 and len(domain) > 0
    except ValidationError:
        # An error is expected on this test
        pass


@pytest.mark.parametrize('domain', invalid_domain_types)
def test_invalid_domain_types(domain: Any):
    with pytest.raises(ValidationError, match='Value must be a string'):
        MyModel(domain=domain)
