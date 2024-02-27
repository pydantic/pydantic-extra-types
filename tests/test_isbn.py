from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

from pydantic_extra_types.isbn import ISBN


class Book(BaseModel):
    isbn: ISBN


isbn_length_test_cases = [
    # Valid ISBNs
    ('8537809667', '9788537809662', True),  # ISBN-10 as input
    ('9788537809662', '9788537809662', True),  # ISBN-13 as input
    ('080442957X', '9780804429573', True),  # ISBN-10 ending in "X" as input
    ('9788584390670', '9788584390670', True),  # ISBN-13 Starting with 978
    ('9790306406156', '9790306406156', True),  # ISBN-13 starting with 979
    # Invalid ISBNs
    ('97885843906701', None, False),  # Length: 14 (Higher)
    ('978858439067', None, False),  # Length: 12 (In Between)
    ('97885843906', None, False),  # Length: 11 (In Between)
    ('978858439', None, False),  # Length: 9 (Lower)
    ('', None, False),  # Length: 0 (Lower)
]


@pytest.mark.parametrize('input_isbn, output_isbn, valid', isbn_length_test_cases)
def test_isbn_length(input_isbn: Any, output_isbn: str, valid: bool) -> None:
    if valid:
        assert Book(isbn=ISBN(input_isbn)).isbn == output_isbn
    else:
        with pytest.raises(ValidationError, match='isbn_length'):
            Book(isbn=ISBN(input_isbn))


isbn10_digits_test_cases = [
    # Valid ISBNs
    ('8537809667', '9788537809662', True),  # ISBN-10 as input
    ('080442957X', '9780804429573', True),  # ISBN-10 ending in "X" as input
    # Invalid ISBNs
    ('@80442957X', None, False),  # Non Integer in [0] position
    ('8@37809667', None, False),  # Non Integer in [1] position
    ('85@7809667', None, False),  # Non Integer in [2] position
    ('853@809667', None, False),  # Non Integer in [3] position
    ('8537@09667', None, False),  # Non Integer in [4] position
    ('85378@9667', None, False),  # Non Integer in [5] position
    ('853780@667', None, False),  # Non Integer in [6] position
    ('8537809@67', None, False),  # Non Integer in [7] position
    ('85378096@7', None, False),  # Non Integer in [8] position
    ('853780966@', None, False),  # Non Integer or X in [9] position
]


@pytest.mark.parametrize('input_isbn, output_isbn, valid', isbn10_digits_test_cases)
def test_isbn10_digits(input_isbn: Any, output_isbn: str, valid: bool) -> None:
    if valid:
        assert Book(isbn=ISBN(input_isbn)).isbn == output_isbn
    else:
        with pytest.raises(ValidationError, match='isbn10_invalid_characters'):
            Book(isbn=ISBN(input_isbn))


isbn13_digits_test_cases = [
    # Valid ISBNs
    ('9788537809662', '9788537809662', True),  # ISBN-13 as input
    ('9780306406157', '9780306406157', True),  # ISBN-13 as input
    ('9788584390670', '9788584390670', True),  # ISBN-13 Starting with 978
    ('9790306406156', '9790306406156', True),  # ISBN-13 starting with 979
    # Invalid ISBNs
    ('@788537809662', None, False),  # Non Integer in [0] position
    ('9@88537809662', None, False),  # Non Integer in [1] position
    ('97@8537809662', None, False),  # Non Integer in [2] position
    ('978@537809662', None, False),  # Non Integer in [3] position
    ('9788@37809662', None, False),  # Non Integer in [4] position
    ('97885@7809662', None, False),  # Non Integer in [5] position
    ('978853@809662', None, False),  # Non Integer in [6] position
    ('9788537@09662', None, False),  # Non Integer in [7] position
    ('97885378@9662', None, False),  # Non Integer in [8] position
    ('978853780@662', None, False),  # Non Integer in [9] position
    ('9788537809@62', None, False),  # Non Integer in [10] position
    ('97885378096@2', None, False),  # Non Integer in [11] position
    ('978853780966@', None, False),  # Non Integer in [12] position
]


@pytest.mark.parametrize('input_isbn, output_isbn, valid', isbn13_digits_test_cases)
def test_isbn13_digits(input_isbn: Any, output_isbn: str, valid: bool) -> None:
    if valid:
        assert Book(isbn=ISBN(input_isbn)).isbn == output_isbn
    else:
        with pytest.raises(ValidationError, match='isbn13_invalid_characters'):
            Book(isbn=ISBN(input_isbn))


isbn13_early_digits_test_cases = [
    # Valid ISBNs
    ('9780306406157', '9780306406157', True),  # ISBN-13 as input
    ('9788584390670', '9788584390670', True),  # ISBN-13 Starting with 978
    ('9790306406156', '9790306406156', True),  # ISBN-13 starting with 979
    # Invalid ISBNs
    ('1788584390670', None, False),  # Does not start with 978 or 979
    ('9288584390670', None, False),  # Does not start with 978 or 979
    ('9738584390670', None, False),  # Does not start with 978 or 979
]


@pytest.mark.parametrize('input_isbn, output_isbn, valid', isbn13_early_digits_test_cases)
def test_isbn13_early_digits(input_isbn: Any, output_isbn: str, valid: bool) -> None:
    if valid:
        assert Book(isbn=ISBN(input_isbn)).isbn == output_isbn
    else:
        with pytest.raises(ValidationError, match='isbn_invalid_early_characters'):
            Book(isbn=ISBN(input_isbn))


isbn_last_digit_test_cases = [
    # Valid ISBNs
    ('8537809667', '9788537809662', True),  # ISBN-10 as input
    ('9788537809662', '9788537809662', True),  # ISBN-13 as input
    ('080442957X', '9780804429573', True),  # ISBN-10 ending in "X" as input
    ('9788584390670', '9788584390670', True),  # ISBN-13 Starting with 978
    ('9790306406156', '9790306406156', True),  # ISBN-13 starting with 979
    # Invalid ISBNs
    ('8537809663', None, False),  # ISBN-10 as input with wrong last digit
    ('9788537809661', None, False),  # ISBN-13 as input with wrong last digit
    ('080442953X', None, False),  # ISBN-10 ending in "X" as input with wrong last digit
    ('9788584390671', None, False),  # ISBN-13 Starting with 978 with wrong last digit
    ('9790306406155', None, False),  # ISBN-13 starting with 979 with wrong last digit
]


@pytest.mark.parametrize('input_isbn, output_isbn, valid', isbn_last_digit_test_cases)
def test_isbn_last_digit(input_isbn: Any, output_isbn: str, valid: bool) -> None:
    if valid:
        assert Book(isbn=ISBN(input_isbn)).isbn == output_isbn
    else:
        with pytest.raises(ValidationError, match='isbn_invalid_digit_check_isbn'):
            Book(isbn=ISBN(input_isbn))


isbn_conversion_test_cases = [
    # Valid ISBNs
    ('8537809667', '9788537809662'),
    ('080442957X', '9780804429573'),
    ('9788584390670', '9788584390670'),
    ('9790306406156', '9790306406156'),
]


@pytest.mark.parametrize('input_isbn, output_isbn', isbn_conversion_test_cases)
def test_isbn_conversion(input_isbn: Any, output_isbn: str) -> None:
    assert Book(isbn=ISBN(input_isbn)).isbn == output_isbn
