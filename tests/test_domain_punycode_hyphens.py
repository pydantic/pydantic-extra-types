import pytest
from pydantic import TypeAdapter, ValidationError

from pydantic_extra_types.domain import DomainStr


@pytest.mark.parametrize(
    'domain',
    [
        'example.xn--vermgensberater-ctb',
        'example.xn--vermgensberatung-pwb',
        'EXAMPLE.XN--VERMGENSBERATER-CTB',
        'example.xn--p1ai',
        'example.com',
    ],
)
def test_domain_accepts_punycode_tlds_with_internal_hyphens(domain: str) -> None:
    assert TypeAdapter(DomainStr).validate_python(domain) == domain.lower()


@pytest.mark.parametrize(
    'tld',
    ['xn--abc-', 'xn--a_b', 'xn--' + 'a' * 57 + '-bc', 'ordinary-tld'],
)
def test_domain_punycode_hyphens_preserve_label_restrictions(tld: str) -> None:
    with pytest.raises(ValidationError, match='Invalid domain format'):
        TypeAdapter(DomainStr).validate_python('example.' + tld)
