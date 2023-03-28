"""all supported currencies, Data about currencies is taken from https://github.com/sebastianbergmann/money"""

from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, List

from pydantic_core import PydanticCustomError, core_schema


@dataclass
class Currency:
    code: str
    display_name: str
    numeric_code: int
    default_fraction_digits: int
    sub_unit: int


@lru_cache()
def _currency() -> List[Currency]:
    """Get currency by code"""
    return [
        Currency(
            'AED',
            'UAE Dirham',
            784,
            2,
            100,
        ),
        Currency(
            'AFN',
            'Afghani',
            971,
            2,
            100,
        ),
        Currency(
            'ALL',
            'Lek',
            8,
            2,
            100,
        ),
        Currency(
            'AMD',
            'Armenian Dram',
            51,
            2,
            100,
        ),
        Currency(
            'ANG',
            'Netherlands Antillean Guilder',
            532,
            2,
            100,
        ),
        Currency(
            'AOA',
            'Kwanza',
            973,
            2,
            100,
        ),
        Currency(
            'ARS',
            'Argentine Peso',
            32,
            2,
            100,
        ),
        Currency(
            'AUD',
            'Australian Dollar',
            36,
            2,
            100,
        ),
        Currency(
            'AWG',
            'Aruban Florin',
            533,
            2,
            100,
        ),
        Currency(
            'AZN',
            'Azerbaijanian Manat',
            944,
            2,
            100,
        ),
        Currency(
            'BAM',
            'Convertible Mark',
            977,
            2,
            100,
        ),
        Currency(
            'BBD',
            'Barbados Dollar',
            52,
            2,
            100,
        ),
        Currency(
            'BDT',
            'Taka',
            50,
            2,
            100,
        ),
        Currency(
            'BGN',
            'Bulgarian Lev',
            975,
            2,
            100,
        ),
        Currency(
            'BHD',
            'Bahraini Dinar',
            48,
            3,
            1000,
        ),
        Currency(
            'BIF',
            'Burundi Franc',
            108,
            0,
            100,
        ),
        Currency(
            'BMD',
            'Bermudian Dollar',
            60,
            2,
            100,
        ),
        Currency(
            'BND',
            'Brunei Dollar',
            96,
            2,
            100,
        ),
        Currency(
            'BOB',
            'Boliviano',
            68,
            2,
            100,
        ),
        Currency(
            'BOV',
            'Mvdol',
            984,
            2,
            100,
        ),
        Currency(
            'BRL',
            'Brazilian Real',
            986,
            2,
            100,
        ),
        Currency(
            'BSD',
            'Bahamian Dollar',
            44,
            2,
            100,
        ),
        Currency(
            'BTN',
            'Ngultrum',
            64,
            2,
            100,
        ),
        Currency(
            'BWP',
            'Pula',
            72,
            2,
            100,
        ),
        Currency(
            'BYR',
            'Belarusian Ruble',
            974,
            0,
            1,
        ),
        Currency(
            'BYN',
            'Belarusian Ruble',
            933,
            2,
            100,
        ),
        Currency(
            'BZD',
            'Belize Dollar',
            84,
            2,
            100,
        ),
        Currency(
            'CAD',
            'Canadian Dollar',
            124,
            2,
            100,
        ),
        Currency(
            'CDF',
            'Congolese Franc',
            976,
            2,
            100,
        ),
        Currency(
            'CHE',
            'WIR Euro',
            947,
            2,
            100,
        ),
        Currency(
            'CHF',
            'Swiss Franc',
            756,
            2,
            100,
        ),
        Currency(
            'CHW',
            'WIR Franc',
            948,
            2,
            100,
        ),
        Currency(
            'CLF',
            'Unidades de fomento',
            990,
            0,
            100,
        ),
        Currency(
            'CLP',
            'Chilean Peso',
            152,
            0,
            100,
        ),
        Currency(
            'CNY',
            'Yuan Renminbi',
            156,
            2,
            100,
        ),
        Currency(
            'COP',
            'Colombian Peso',
            170,
            2,
            100,
        ),
        Currency(
            'COU',
            'Unidad de Valor Real',
            970,
            2,
            100,
        ),
        Currency(
            'CRC',
            'Costa Rican Colon',
            188,
            2,
            100,
        ),
        Currency(
            'CUC',
            'Peso Convertible',
            931,
            2,
            100,
        ),
        Currency(
            'CUP',
            'Cuban Peso',
            192,
            2,
            100,
        ),
        Currency(
            'CVE',
            'Cape Verde Escudo',
            132,
            2,
            100,
        ),
        Currency(
            'CZK',
            'Czech Koruna',
            203,
            2,
            100,
        ),
        Currency(
            'DJF',
            'Djibouti Franc',
            262,
            0,
            100,
        ),
        Currency(
            'DKK',
            'Danish Krone',
            208,
            2,
            100,
        ),
        Currency(
            'DOP',
            'Dominican Peso',
            214,
            2,
            100,
        ),
        Currency(
            'DZD',
            'Algerian Dinar',
            12,
            2,
            100,
        ),
        Currency(
            'EGP',
            'Egyptian Pound',
            818,
            2,
            100,
        ),
        Currency(
            'ERN',
            'Nakfa',
            232,
            2,
            100,
        ),
        Currency(
            'ETB',
            'Ethiopian Birr',
            230,
            2,
            100,
        ),
        Currency(
            'EUR',
            'Euro',
            978,
            2,
            100,
        ),
        Currency(
            'FJD',
            'Fiji Dollar',
            242,
            2,
            100,
        ),
        Currency(
            'FKP',
            'Falkland Islands Pound',
            238,
            2,
            100,
        ),
        Currency(
            'GBP',
            'Pound Sterling',
            826,
            2,
            100,
        ),
        Currency(
            'GEL',
            'Lari',
            981,
            2,
            100,
        ),
        Currency(
            'GHS',
            'Ghana Cedi',
            936,
            2,
            100,
        ),
        Currency(
            'GIP',
            'Gibraltar Pound',
            292,
            2,
            100,
        ),
        Currency(
            'GMD',
            'Dalasi',
            270,
            2,
            100,
        ),
        Currency(
            'GNF',
            'Guinea Franc',
            324,
            0,
            100,
        ),
        Currency(
            'GTQ',
            'Quetzal',
            320,
            2,
            100,
        ),
        Currency(
            'GYD',
            'Guyana Dollar',
            328,
            2,
            100,
        ),
        Currency(
            'HKD',
            'Hong Kong Dollar',
            344,
            2,
            100,
        ),
        Currency(
            'HNL',
            'Lempira',
            340,
            2,
            100,
        ),
        Currency(
            'HRK',
            'Croatian Kuna',
            191,
            2,
            100,
        ),
        Currency(
            'HTG',
            'Gourde',
            332,
            2,
            100,
        ),
        Currency(
            'HUF',
            'Forint',
            348,
            2,
            100,
        ),
        Currency(
            'IDR',
            'Rupiah',
            360,
            2,
            100,
        ),
        Currency(
            'ILS',
            'New Israeli Sheqel',
            376,
            2,
            100,
        ),
        Currency(
            'INR',
            'Indian Rupee',
            356,
            2,
            100,
        ),
        Currency(
            'IQD',
            'Iraqi Dinar',
            368,
            3,
            1000,
        ),
        Currency(
            'IRR',
            'Iranian Rial',
            364,
            2,
            100,
        ),
        Currency(
            'ISK',
            'Iceland Krona',
            352,
            0,
            100,
        ),
        Currency(
            'JMD',
            'Jamaican Dollar',
            388,
            2,
            100,
        ),
        Currency(
            'JOD',
            'Jordanian Dinar',
            400,
            3,
            1000,
        ),
        Currency(
            'JPY',
            'Yen',
            392,
            0,
            1,
        ),
        Currency(
            'KES',
            'Kenyan Shilling',
            404,
            2,
            100,
        ),
        Currency(
            'KGS',
            'Som',
            417,
            2,
            100,
        ),
        Currency(
            'KHR',
            'Riel',
            116,
            2,
            100,
        ),
        Currency(
            'KMF',
            'Comoro Franc',
            174,
            0,
            100,
        ),
        Currency(
            'KPW',
            'North Korean Won',
            408,
            2,
            100,
        ),
        Currency(
            'KRW',
            'Won',
            410,
            0,
            100,
        ),
        Currency(
            'KWD',
            'Kuwaiti Dinar',
            414,
            3,
            1000,
        ),
        Currency(
            'KYD',
            'Cayman Islands Dollar',
            136,
            2,
            100,
        ),
        Currency(
            'KZT',
            'Tenge',
            398,
            2,
            100,
        ),
        Currency(
            'LAK',
            'Kip',
            418,
            2,
            100,
        ),
        Currency(
            'LBP',
            'Lebanese Pound',
            422,
            2,
            100,
        ),
        Currency(
            'LKR',
            'Sri Lanka Rupee',
            144,
            2,
            100,
        ),
        Currency(
            'LRD',
            'Liberian Dollar',
            430,
            2,
            100,
        ),
        Currency(
            'LSL',
            'Loti',
            426,
            2,
            100,
        ),
        Currency(
            'LTL',
            'Lithuanian Litas',
            440,
            2,
            100,
        ),
        Currency(
            'LVL',
            'Latvian Lats',
            428,
            2,
            100,
        ),
        Currency(
            'LYD',
            'Libyan Dinar',
            434,
            3,
            1000,
        ),
        Currency(
            'MAD',
            'Moroccan Dirham',
            504,
            2,
            100,
        ),
        Currency(
            'MDL',
            'Moldovan Leu',
            498,
            2,
            100,
        ),
        Currency(
            'MGA',
            'Malagasy Ariary',
            969,
            2,
            5,
        ),
        Currency(
            'MKD',
            'Denar',
            807,
            2,
            100,
        ),
        Currency(
            'MMK',
            'Kyat',
            104,
            2,
            100,
        ),
        Currency(
            'MNT',
            'Tugrik',
            496,
            2,
            100,
        ),
        Currency(
            'MOP',
            'Pataca',
            446,
            2,
            100,
        ),
        Currency(
            'MRO',
            'Ouguiya',
            478,
            2,
            5,
        ),
        Currency(
            'MUR',
            'Mauritius Rupee',
            480,
            2,
            100,
        ),
        Currency(
            'MVR',
            'Rufiyaa',
            462,
            2,
            100,
        ),
        Currency(
            'MWK',
            'Kwacha',
            454,
            2,
            100,
        ),
        Currency(
            'MXN',
            'Mexican Peso',
            484,
            2,
            100,
        ),
        Currency(
            'MXV',
            'Mexican Unidad de Inversion (UDI)',
            979,
            2,
            100,
        ),
        Currency(
            'MYR',
            'Malaysian Ringgit',
            458,
            2,
            100,
        ),
        Currency(
            'MZN',
            'Mozambique Metical',
            943,
            2,
            100,
        ),
        Currency(
            'NAD',
            'Namibia Dollar',
            516,
            2,
            100,
        ),
        Currency(
            'NGN',
            'Naira',
            566,
            2,
            100,
        ),
        Currency(
            'NIO',
            'Cordoba Oro',
            558,
            2,
            100,
        ),
        Currency(
            'NOK',
            'Norwegian Krone',
            578,
            2,
            100,
        ),
        Currency(
            'NPR',
            'Nepalese Rupee',
            524,
            2,
            100,
        ),
        Currency(
            'NZD',
            'New Zealand Dollar',
            554,
            2,
            100,
        ),
        Currency(
            'OMR',
            'Rial Omani',
            512,
            3,
            1000,
        ),
        Currency(
            'PAB',
            'Balboa',
            590,
            2,
            100,
        ),
        Currency(
            'PEN',
            'Nuevo Sol',
            604,
            2,
            100,
        ),
        Currency(
            'PGK',
            'Kina',
            598,
            2,
            100,
        ),
        Currency(
            'PHP',
            'Philippine Peso',
            608,
            2,
            100,
        ),
        Currency(
            'PKR',
            'Pakistan Rupee',
            586,
            2,
            100,
        ),
        Currency(
            'PLN',
            'Zloty',
            985,
            2,
            100,
        ),
        Currency(
            'PYG',
            'Guarani',
            600,
            0,
            100,
        ),
        Currency(
            'QAR',
            'Qatari Rial',
            634,
            2,
            100,
        ),
        Currency(
            'RON',
            'New Romanian Leu',
            946,
            2,
            100,
        ),
        Currency(
            'RSD',
            'Serbian Dinar',
            941,
            2,
            100,
        ),
        Currency(
            'RUB',
            'Russian Ruble',
            643,
            2,
            100,
        ),
        Currency(
            'RWF',
            'Rwanda Franc',
            646,
            0,
            100,
        ),
        Currency(
            'SAR',
            'Saudi Riyal',
            682,
            2,
            100,
        ),
        Currency(
            'SBD',
            'Solomon Islands Dollar',
            90,
            2,
            100,
        ),
        Currency(
            'SCR',
            'Seychelles Rupee',
            690,
            2,
            100,
        ),
        Currency(
            'SDG',
            'Sudanese Pound',
            938,
            2,
            100,
        ),
        Currency(
            'SEK',
            'Swedish Krona',
            752,
            2,
            100,
        ),
        Currency(
            'SGD',
            'Singapore Dollar',
            702,
            2,
            100,
        ),
        Currency(
            'SHP',
            'Saint Helena Pound',
            654,
            2,
            100,
        ),
        Currency(
            'SLL',
            'Leone',
            694,
            2,
            100,
        ),
        Currency(
            'SOS',
            'Somali Shilling',
            706,
            2,
            100,
        ),
        Currency(
            'SRD',
            'Surinam Dollar',
            968,
            2,
            100,
        ),
        Currency(
            'SSP',
            'South Sudanese Pound',
            728,
            2,
            100,
        ),
        Currency(
            'STD',
            'Dobra',
            678,
            2,
            100,
        ),
        Currency(
            'SVC',
            'El Salvador Colon',
            222,
            2,
            100,
        ),
        Currency(
            'SYP',
            'Syrian Pound',
            760,
            2,
            100,
        ),
        Currency(
            'SZL',
            'Lilangeni',
            748,
            2,
            100,
        ),
        Currency(
            'THB',
            'Baht',
            764,
            2,
            100,
        ),
        Currency(
            'TJS',
            'Somoni',
            972,
            2,
            100,
        ),
        Currency(
            'TMT',
            'Turkmenistan New Manat',
            934,
            2,
            100,
        ),
        Currency(
            'TND',
            'Tunisian Dinar',
            788,
            3,
            1000,
        ),
        Currency(
            'TOP',
            'Pa’anga',
            776,
            2,
            100,
        ),
        Currency(
            'TRY',
            'Turkish Lira',
            949,
            2,
            100,
        ),
        Currency(
            'TTD',
            'Trinidad and Tobago Dollar',
            780,
            2,
            100,
        ),
        Currency(
            'TWD',
            'New Taiwan Dollar',
            901,
            2,
            100,
        ),
        Currency(
            'TZS',
            'Tanzanian Shilling',
            834,
            2,
            100,
        ),
        Currency(
            'UAH',
            'Hryvnia',
            980,
            2,
            100,
        ),
        Currency(
            'UGX',
            'Uganda Shilling',
            800,
            0,
            100,
        ),
        Currency(
            'USD',
            'US Dollar',
            840,
            2,
            100,
        ),
        Currency(
            'USN',
            'US Dollar (Next day)',
            997,
            2,
            100,
        ),
        Currency(
            'USS',
            'US Dollar (Same day)',
            998,
            2,
            100,
        ),
        Currency(
            'UYI',
            'Uruguay Peso en Unidades Indexadas (URUIURUI)',
            940,
            0,
            100,
        ),
        Currency(
            'UYU',
            'Peso Uruguayo',
            858,
            2,
            100,
        ),
        Currency(
            'UZS',
            'Uzbekistan Sum',
            860,
            2,
            100,
        ),
        Currency(
            'VEF',
            'Bolivar',
            937,
            2,
            100,
        ),
        Currency(
            'VND',
            'Dong',
            704,
            0,
            10,
        ),
        Currency(
            'VUV',
            'Vatu',
            548,
            0,
            1,
        ),
        Currency(
            'WST',
            'Tala',
            882,
            2,
            100,
        ),
        Currency(
            'XAF',
            'CFA Franc BEAC',
            950,
            0,
            100,
        ),
        Currency(
            'XAG',
            'Silver',
            961,
            0,
            100,
        ),
        Currency(
            'XAU',
            'Gold',
            959,
            0,
            100,
        ),
        Currency(
            'XBA',
            'Bond Markets Unit European Composite Unit (EURCO)',
            955,
            0,
            100,
        ),
        Currency(
            'XBB',
            'Bond Markets Unit European Monetary Unit (EMU-6)',
            956,
            0,
            100,
        ),
        Currency(
            'XBC',
            'Bond Markets Unit European Unit of Account 9 (EUA-9)',
            957,
            0,
            100,
        ),
        Currency(
            'XBD',
            'Bond Markets Unit European Unit of Account 17 (EUA-17)',
            958,
            0,
            100,
        ),
        Currency(
            'XCD',
            'East Caribbean Dollar',
            951,
            2,
            100,
        ),
        Currency(
            'XDR',
            'SDR (Special Drawing Right)',
            960,
            0,
            100,
        ),
        Currency(
            'XFU',
            'UIC-Franc',
            958,
            0,
            100,
        ),
        Currency(
            'XOF',
            'CFA Franc BCEAO',
            952,
            0,
            100,
        ),
        Currency(
            'XPD',
            'Palladium',
            964,
            0,
            100,
        ),
        Currency(
            'XPF',
            'CFP Franc',
            953,
            0,
            100,
        ),
        Currency(
            'XPT',
            'Platinum',
            962,
            0,
            100,
        ),
        Currency(
            'XSU',
            'Sucre',
            994,
            0,
            100,
        ),
        Currency(
            'XTS',
            'Codes specifically reserved for testing purposes',
            963,
            0,
            100,
        ),
        Currency(
            'XUA',
            'ADB Unit of Account',
            965,
            0,
            100,
        ),
        Currency(
            'YER',
            'Yemeni Rial',
            886,
            2,
            100,
        ),
        Currency(
            'ZAR',
            'Rand',
            710,
            2,
            100,
        ),
        Currency(
            'ZMW',
            'Zambian Kwacha',
            967,
            2,
            100,
        ),
        Currency(
            'ZWL',
            'Zimbabwe Dollar',
            932,
            2,
            100,
        ),
    ]


@lru_cache()
def _index_by_code() -> Dict[str, Currency]:
    return {currency.code: currency for currency in _currency()}


@lru_cache()
def _index_by_display_name() -> Dict[str, Currency]:
    return {currency.display_name: currency for currency in _currency()}


@lru_cache()
def _index_by_numeric_code() -> Dict[int, Currency]:
    return {currency.numeric_code: currency for currency in _currency()}


@lru_cache()
def _index_by_default_fraction_digits() -> Dict[int, Currency]:
    return {currency.default_fraction_digits: currency for currency in _currency()}


@lru_cache()
def _index_by_sub_unit() -> Dict[int, Currency]:
    return {currency.sub_unit: currency for currency in _currency()}


class CurrencyCode(str):
    @classmethod
    def _validate(cls, __input_value: str, _: core_schema.ValidationInfo) -> 'CurrencyCode':
        if __input_value not in _index_by_code():
            raise PydanticCustomError('code', 'invalid currency code')
        return cls(__input_value)

    @classmethod
    def __get_pydantic_core_schema__(cls, **_kwargs: Any) -> core_schema.AfterValidatorFunctionSchema:
        return core_schema.general_after_validator_function(cls._validate, core_schema.str_schema(to_upper=True))

    @property
    def display_name(self) -> str:
        return _index_by_code()[self].display_name

    @property
    def numeric_code(self) -> int:
        return _index_by_code()[self].numeric_code

    @property
    def default_fraction_digits(self) -> int:
        return _index_by_code()[self].default_fraction_digits

    @property
    def sub_unit(self) -> int:
        return _index_by_code()[self].sub_unit


class CurrencyDisplayName(str):
    @classmethod
    def _validate(cls, __input_value: str, _: core_schema.ValidationInfo) -> 'CurrencyDisplayName':
        if __input_value not in _index_by_display_name():
            raise PydanticCustomError('currency_display_name', 'invalid currency display name')
        return cls(__input_value)

    @classmethod
    def __get_pydantic_core_schema__(cls, **_kwargs: Any) -> core_schema.AfterValidatorFunctionSchema:
        return core_schema.general_after_validator_function(
            cls._validate,
            core_schema.str_schema(),
        )

    @property
    def code(self) -> str:
        return _index_by_display_name()[self].code

    @property
    def numeric_code(self) -> int:
        return _index_by_display_name()[self].numeric_code

    @property
    def default_fraction_digits(self) -> int:
        return _index_by_display_name()[self].default_fraction_digits

    @property
    def sub_unit(self) -> int:
        return _index_by_display_name()[self].sub_unit


class CurrencyNumericCode(int):
    @classmethod
    def _validate(cls, __input_value: int, _: core_schema.ValidationInfo) -> 'CurrencyNumericCode':
        if __input_value not in _index_by_numeric_code():
            raise PydanticCustomError('currency_numeric_code', 'invalid currency numeric code')
        return cls(__input_value)

    @classmethod
    def __get_pydantic_core_schema__(cls, **_kwargs: Any) -> core_schema.AfterValidatorFunctionSchema:
        return core_schema.general_after_validator_function(cls._validate, core_schema.int_schema())

    @property
    def code(self) -> str:
        return _index_by_numeric_code()[self].code

    @property
    def display_name(self) -> str:
        return _index_by_numeric_code()[self].display_name

    @property
    def default_fraction_digits(self) -> int:
        return _index_by_numeric_code()[self].default_fraction_digits

    @property
    def sub_unit(self) -> int:
        return _index_by_numeric_code()[self].sub_unit


class CurrencyDefaultFractionDigits(int):
    @classmethod
    def _validate(cls, __input_value: int, _: core_schema.ValidationInfo) -> 'CurrencyDefaultFractionDigits':
        if __input_value not in _index_by_default_fraction_digits():
            raise PydanticCustomError('currency_default_fraction_digits', 'invalid currency default fraction digits')
        return cls(__input_value)

    @classmethod
    def __get_pydantic_core_schema__(cls, **_kwargs: Any) -> core_schema.AfterValidatorFunctionSchema:
        return core_schema.general_after_validator_function(cls._validate, core_schema.int_schema())

    @property
    def code(self) -> str:
        return _index_by_default_fraction_digits()[self].code

    @property
    def display_name(self) -> str:
        return _index_by_default_fraction_digits()[self].display_name

    @property
    def numeric_code(self) -> int:
        return _index_by_default_fraction_digits()[self].numeric_code

    @property
    def sub_unit(self) -> int:
        return _index_by_default_fraction_digits()[self].sub_unit


class CurrencySubUnit(int):
    @classmethod
    def _validate(cls, __input_value: int, _: core_schema.ValidationInfo) -> 'CurrencySubUnit':
        if __input_value not in _index_by_sub_unit():
            raise PydanticCustomError('currency_sub_unit', 'invalid currency sub unit')
        return cls(__input_value)

    @classmethod
    def __get_pydantic_core_schema__(cls, **_kwargs: Any) -> core_schema.AfterValidatorFunctionSchema:
        return core_schema.general_after_validator_function(
            cls._validate,
            core_schema.int_schema(),
        )

    @property
    def code(self) -> str:
        return _index_by_sub_unit()[self].code

    @property
    def display_name(self) -> str:
        return _index_by_sub_unit()[self].display_name

    @property
    def numeric_code(self) -> int:
        return _index_by_sub_unit()[self].numeric_code

    @property
    def default_fraction_digits(self) -> int:
        return _index_by_sub_unit()[self].default_fraction_digits
