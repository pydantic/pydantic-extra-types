import pytest
from pydantic import BaseModel, ValidationError

from pydantic_extra_types.iban import IBAN, _validate_iban_check_digits


class BankAccount(BaseModel):
    iban: IBAN


# Valid IBANs from various countries
@pytest.mark.parametrize(
    'iban',
    [
        'GB29NWBK60161331926819',
        'DE89370400440532013000',
        'FR7630006000011234567890189',
        'ES9121000418450200051332',
        'IT60X0542811101000000123456',
        'NL91ABNA0417164300',
        'BE68539007547034',
        'CH9300762011623852957',
        'AT611904300234573201',
        'SE4550000000058398257466',
        'NO9386011117947',
        'DK5000400440116243',
        'PL61109010140000071219812874',
        # With spaces (should be normalized)
        'GB29 NWBK 6016 1331 9268 19',
        # Lowercase (should be normalized)
        'gb29nwbk60161331926819',
    ],
)
def test_valid_iban(iban: str) -> None:
    account = BankAccount(iban=iban)
    assert isinstance(account.iban, str)
    # Should be stored uppercase without spaces
    assert ' ' not in account.iban
    assert account.iban == account.iban.upper()


@pytest.mark.parametrize(
    'iban',
    [
        '',  # empty
        'GB',  # too short
        'XX29NWBK60161331926819',  # unknown country code
        'GB00NWBK60161331926819',  # invalid check digits (wrong checksum)
        'GB29NWBK6016133192681',  # wrong length for GB
        'GB29NWBK601613319268199',  # wrong length for GB
        '1234567890123456',  # no country code
        'GB29NWBK6016133192681!',  # invalid character
    ],
)
def test_invalid_iban(iban: str) -> None:
    with pytest.raises(ValidationError):
        BankAccount(iban=iban)


@pytest.mark.parametrize(
    ('iban', 'error_type'),
    [
        ('GB12', 'iban_invalid_length'),  # shorter than the 5-char minimum
        ('12345678901234', 'iban_invalid_country_code'),  # country code not letters
        ('XX29NWBK60161331926819', 'iban_invalid_country_code'),  # unknown country code
        ('GB29NWBK6016133192681', 'iban_invalid_length'),  # wrong length for GB
        ('GB29NWBK6016133192681!', 'iban_invalid_characters'),  # non-alphanumeric body
        ('GBABNWBK60161331926819', 'iban_invalid_check_digits'),  # check digits not numeric
        ('GB00NWBK60161331926819', 'iban_invalid_checksum'),  # MOD-97 checksum fails
    ],
)
def test_invalid_iban_raises_specific_error(iban: str, error_type: str) -> None:
    with pytest.raises(ValidationError) as exc_info:
        BankAccount(iban=iban)
    assert exc_info.value.errors()[0]['type'] == error_type


@pytest.mark.parametrize(
    'iban',
    [
        'GB29NWBK60161331926819',
        'DE89370400440532013000',
        'FR7630006000011234567890189',
        'ES9121000418450200051332',
    ],
)
def test_validate_iban_check_digits_accepts_valid(iban: str) -> None:
    assert _validate_iban_check_digits(iban) is True


@pytest.mark.parametrize(
    'iban',
    [
        'GB00NWBK60161331926819',
        'DE00370400440532013000',
        'FR0030006000011234567890189',
    ],
)
def test_validate_iban_check_digits_rejects_invalid(iban: str) -> None:
    assert _validate_iban_check_digits(iban) is False


def test_iban_normalizes_spaces_and_case() -> None:
    account = BankAccount(iban='gb29 nwbk 6016 1331 9268 19')
    assert account.iban == 'GB29NWBK60161331926819'
    assert isinstance(account.iban, str)
