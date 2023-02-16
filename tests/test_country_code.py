import pytest
from pydantic import BaseModel
from pydantic_core import PydanticCustomError

from pydantic_extra_types import Country


@pytest.mark.parametrize(
    'code, country_data',
    [
        ('AF', ('Afghanistan', 'The Islamic Republic of Afghanistan', 'AF', 'AFG', '004')),
        ('AX', ('Åland Islands', 'Åland', 'AX', 'ALA', '248')),
        ('AL', ('Albania', 'The Republic of Albania', 'AL', 'ALB', '008')),
        ('DZ', ('Algeria', "The People's Democratic Republic of Algeria", 'DZ', 'DZA', '012')),
        ('EH', ('Western Sahara', 'The Sahrawi Arab Democratic Republic', 'EH', 'ESH', '732')),
        ('YE', ('Yemen', 'The Republic of Yemen', 'YE', 'YEM', '887')),
        ('ZM', ('Zambia', 'The Republic of Zambia', 'ZM', 'ZMB', '894')),
        ('IL', ('Israel', 'The State of Israel', 'IL', 'ISR', '376')),
        ('ZW', ('Zimbabwe', 'The Republic of Zimbabwe', 'ZW',  'ZWE', '716')),
        ('CY', ('Cyprus', 'The Republic of Cyprus', 'CY',  'CYP', '196')),

        ('AFG', ('Afghanistan', 'The Islamic Republic of Afghanistan', 'AF', 'AFG', '004')),
        ('ALA', ('Åland Islands', 'Åland', 'AX', 'ALA', '248')),
        ('ALB', ('Albania', 'The Republic of Albania', 'AL', 'ALB', '008')),
        ('DZA', ('Algeria', "The People's Democratic Republic of Algeria", 'DZ', 'DZA', '012')),
        ('ESH', ('Western Sahara', 'The Sahrawi Arab Democratic Republic', 'EH', 'ESH', '732')),
        ('YEM', ('Yemen', 'The Republic of Yemen', 'YE', 'YEM', '887')),
        ('ZMB', ('Zambia', 'The Republic of Zambia', 'ZM', 'ZMB', '894')),
        ('ISR', ('Israel', 'The State of Israel', 'IL', 'ISR', '376')),
        ('ZWE', ('Zimbabwe', 'The Republic of Zimbabwe', 'ZW', 'ZWE', '716')),
        ('CYP', ('Cyprus', 'The Republic of Cyprus', 'CY', 'CYP', '196')),

        ('004', ('Afghanistan', 'The Islamic Republic of Afghanistan', 'AF', 'AFG', '004')),
        ('248', ('Åland Islands', 'Åland', 'AX', 'ALA', '248')),
        ('008', ('Albania', 'The Republic of Albania', 'AL', 'ALB', '008')),
        ('012', ('Algeria', "The People's Democratic Republic of Algeria", 'DZ', 'DZA', '012')),
        ('732', ('Western Sahara', 'The Sahrawi Arab Democratic Republic', 'EH', 'ESH', '732')),
        ('887', ('Yemen', 'The Republic of Yemen', 'YE', 'YEM', '887')),
        ('894', ('Zambia', 'The Republic of Zambia', 'ZM', 'ZMB', '894')),
        ('376', ('Israel', 'The State of Israel', 'IL', 'ISR', '376')),
        ('716', ('Zimbabwe', 'The Republic of Zimbabwe', 'ZW', 'ZWE', '716')),
        ('196', ('Cyprus', 'The Republic of Cyprus', 'CY', 'CYP', '196')),

        ('Afghanistan', ('Afghanistan', 'The Islamic Republic of Afghanistan', 'AF', 'AFG', '004')),
        ('Åland Islands', ('Åland Islands', 'Åland', 'AX', 'ALA', '248')),
        ('Albania', ('Albania', 'The Republic of Albania', 'AL', 'ALB', '008')),
        ('Algeria', ('Algeria', "The People's Democratic Republic of Algeria", 'DZ', 'DZA', '012')),
        ('Western Sahara', ('Western Sahara', 'The Sahrawi Arab Democratic Republic', 'EH', 'ESH', '732')),
        ('Yemen', ('Yemen', 'The Republic of Yemen', 'YE', 'YEM', '887')),
        ('Zambia', ('Zambia', 'The Republic of Zambia', 'ZM', 'ZMB', '894')),
        ('Israel', ('Israel', 'The State of Israel', 'IL', 'ISR', '376')),
        ('Zimbabwe', ('Zimbabwe', 'The Republic of Zimbabwe', 'ZW', 'ZWE', '716')),
        ('Cyprus', ('Cyprus', 'The Republic of Cyprus', 'CY', 'CYP', '196')),
    ],
)
def test_code_success(code, country_data):
    country = Country(code)
    assert country.country_name == country_data[0]
    assert country.official_name == country_data[1]
    assert country.alpha2_code == country_data[2]
    assert country.alpha3_code == country_data[3]
    assert country.numeric_code == country_data[4]


@pytest.mark.parametrize(
    'code',
    [
        "lala lend",
        "IamHungry",
        "PO",
        "ZN",
        "AES",
        "RSA",
        "0",
        "00",
        "000",
        "111",
        1,
        2,
        [1, 1, 1],
        int,
        str,
    ],
)
def test_code_fail(code):
    with pytest.raises(PydanticCustomError) as error:
        Country(code)
    assert error.value.type == 'country_code_error'


def test_model_validation():
    class Model(BaseModel):
        country: Country

    assert Model(country="US").country.alpha3_code == "USA"
    assert Model(country="USA").country.alpha2_code == "US"
    assert Model(country="united states of america").country.alpha2_code == "US"
    assert Model(country="840").country.alpha2_code == "US"


def test_str_repr():
    assert str(Country("US")) == str(Country("us")) == "country_name='United States of America' official_name='The United States of America' alpha2_code='US' alpha3_code='USA' numeric_code='840'"
    assert repr(Country("US")) == repr(Country("us")) == "Country('US', country_name='United States of America', official_name='The United States of America', alpha3_code='USA', numeric_code='840')"


def test_eq():
    assert Country('us') == Country('us')
    assert Country('us') != Country('france')
    assert Country('us') != 'us'

    assert Country('US') == Country("USA") == Country("840") == Country("United States of America")


def test_hash():
    assert hash(Country('US')) == hash(Country("USA")) == hash(Country("840")) == hash(Country("United States of America"))
    assert hash("US") != hash("FR")
