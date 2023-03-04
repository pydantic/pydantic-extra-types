"""
Country definitions that are based on the ISO 3166 format
Based on: https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes
"""
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, List

from pydantic_core import PydanticCustomError, core_schema


@dataclass
class CountryInfo:
    alpha2: str
    alpha3: str
    numeric_code: str
    short_name: str
    official_name: str


@lru_cache()
def _countries() -> List[CountryInfo]:
    return [
        CountryInfo(
            'GM',
            'GMB',
            '270',
            'Gambia',
            'The Republic of The Gambia',
        ),
        CountryInfo(
            'GE',
            'GEO',
            '268',
            'Georgia',
            'Georgia',
        ),
        CountryInfo(
            'DE',
            'DEU',
            '276',
            'Germany',
            'The Federal Republic of Germany',
        ),
        CountryInfo(
            'GH',
            'GHA',
            '288',
            'Ghana',
            'The Republic of Ghana',
        ),
        CountryInfo(
            'GI',
            'GIB',
            '292',
            'Gibraltar',
            'Gibraltar',
        ),
        CountryInfo(
            'GR',
            'GRC',
            '300',
            'Greece',
            'The Hellenic Republic',
        ),
        CountryInfo(
            'GL',
            'GRL',
            '304',
            'Greenland',
            'Kalaallit Nunaat',
        ),
        CountryInfo(
            'GD',
            'GRD',
            '308',
            'Grenada',
            'Grenada',
        ),
        CountryInfo(
            'GP',
            'GLP',
            '312',
            'Guadeloupe',
            'Guadeloupe',
        ),
        CountryInfo(
            'GU',
            'GUM',
            '316',
            'Guam',
            'The Territory of Guam',
        ),
        CountryInfo(
            'GT',
            'GTM',
            '320',
            'Guatemala',
            'The Republic of Guatemala',
        ),
        CountryInfo(
            'GG',
            'GGY',
            '831',
            'Guernsey',
            'The Bailiwick of Guernsey',
        ),
        CountryInfo(
            'GN',
            'GIN',
            '324',
            'Guinea',
            'The Republic of Guinea',
        ),
        CountryInfo(
            'GW',
            'GNB',
            '624',
            'Guinea-Bissau',
            'The Republic of Guinea-Bissau',
        ),
        CountryInfo(
            'GY',
            'GUY',
            '328',
            'Guyana',
            'The Co-operative Republic of Guyana',
        ),
        CountryInfo(
            'HT',
            'HTI',
            '332',
            'Haiti',
            'The Republic of Haiti',
        ),
        CountryInfo(
            'HM',
            'HMD',
            '334',
            'Heard Island and McDonald Islands',
            'The Territory of Heard Island and McDonald Islands',
        ),
        CountryInfo(
            'VA',
            'VAT',
            '336',
            'Holy See',
            'The Holy See',
        ),
        CountryInfo(
            'HN',
            'HND',
            '340',
            'Honduras',
            'The Republic of Honduras',
        ),
        CountryInfo(
            'HK',
            'HKG',
            '344',
            'Hong Kong',
            'The Hong Kong Special Administrative Region of China[10]',
        ),
        CountryInfo(
            'HU',
            'HUN',
            '348',
            'Hungary',
            'Hungary',
        ),
        CountryInfo(
            'IS',
            'ISL',
            '352',
            'Iceland',
            'Iceland',
        ),
        CountryInfo(
            'IN',
            'IND',
            '356',
            'India',
            'The Republic of India',
        ),
        CountryInfo(
            'ID',
            'IDN',
            '360',
            'Indonesia',
            'The Republic of Indonesia',
        ),
        CountryInfo(
            'IR',
            'IRN',
            '364',
            'Iran (Islamic Republic of)',
            'The Islamic Republic of Iran',
        ),
        CountryInfo(
            'IQ',
            'IRQ',
            '368',
            'Iraq',
            'The Republic of Iraq',
        ),
        CountryInfo(
            'IE',
            'IRL',
            '372',
            'Ireland',
            'Ireland',
        ),
        CountryInfo(
            'IM',
            'IMN',
            '833',
            'Isle of Man',
            'The Isle of Man',
        ),
        CountryInfo(
            'IL',
            'ISR',
            '376',
            'Israel',
            'The State of Israel',
        ),
        CountryInfo(
            'IT',
            'ITA',
            '380',
            'Italy',
            'The Italian Republic',
        ),
        CountryInfo(
            'JM',
            'JAM',
            '388',
            'Jamaica',
            'Jamaica',
        ),
        CountryInfo(
            'JP',
            'JPN',
            '392',
            'Japan',
            'Japan',
        ),
        CountryInfo(
            'JE',
            'JEY',
            '832',
            'Jersey',
            'The Bailiwick of Jersey',
        ),
        CountryInfo(
            'JO',
            'JOR',
            '400',
            'Jordan',
            'The Hashemite Kingdom of Jordan',
        ),
        CountryInfo(
            'KZ',
            'KAZ',
            '398',
            'Kazakhstan',
            'The Republic of Kazakhstan',
        ),
        CountryInfo(
            'KE',
            'KEN',
            '404',
            'Kenya',
            'The Republic of Kenya',
        ),
        CountryInfo(
            'KI',
            'KIR',
            '296',
            'Kiribati',
            'The Republic of Kiribati',
        ),
        CountryInfo(
            'KP',
            'PRK',
            '408',
            "Korea (the Democratic People's Republic of)",
            "The Democratic People's Republic of Korea",
        ),
        CountryInfo(
            'KR',
            'KOR',
            '410',
            'Korea (the Republic of)',
            'The Republic of Korea',
        ),
        CountryInfo(
            'KW',
            'KWT',
            '414',
            'Kuwait',
            'The State of Kuwait',
        ),
        CountryInfo(
            'KG',
            'KGZ',
            '417',
            'Kyrgyzstan',
            'The Kyrgyz Republic',
        ),
        CountryInfo(
            'LA',
            'LAO',
            '418',
            "Lao People's Democratic Republic",
            "The Lao People's Democratic Republic",
        ),
        CountryInfo(
            'LV',
            'LVA',
            '428',
            'Latvia',
            'The Republic of Latvia',
        ),
        CountryInfo(
            'LB',
            'LBN',
            '422',
            'Lebanon',
            'The Lebanese Republic',
        ),
        CountryInfo(
            'LS',
            'LSO',
            '426',
            'Lesotho',
            'The Kingdom of Lesotho',
        ),
        CountryInfo(
            'LR',
            'LBR',
            '430',
            'Liberia',
            'The Republic of Liberia',
        ),
        CountryInfo(
            'LY',
            'LBY',
            '434',
            'Libya',
            'The State of Libya',
        ),
        CountryInfo(
            'LI',
            'LIE',
            '438',
            'Liechtenstein',
            'The Principality of Liechtenstein',
        ),
        CountryInfo(
            'LT',
            'LTU',
            '440',
            'Lithuania',
            'The Republic of Lithuania',
        ),
        CountryInfo(
            'LU',
            'LUX',
            '442',
            'Luxembourg',
            'The Grand Duchy of Luxembourg',
        ),
        CountryInfo(
            'MO',
            'MAC',
            '446',
            'Macao',
            'The Macao Special Administrative Region of China[11]',
        ),
        CountryInfo(
            'MK',
            'MKD',
            '807',
            'North Macedonia',
            'The Republic of North Macedonia[12]',
        ),
        CountryInfo(
            'MG',
            'MDG',
            '450',
            'Madagascar',
            'The Republic of Madagascar',
        ),
        CountryInfo(
            'MW',
            'MWI',
            '454',
            'Malawi',
            'The Republic of Malawi',
        ),
        CountryInfo(
            'MY',
            'MYS',
            '458',
            'Malaysia',
            'Malaysia',
        ),
        CountryInfo(
            'MV',
            'MDV',
            '462',
            'Maldives',
            'The Republic of Maldives',
        ),
        CountryInfo(
            'ML',
            'MLI',
            '466',
            'Mali',
            'The Republic of Mali',
        ),
        CountryInfo(
            'MT',
            'MLT',
            '470',
            'Malta',
            'The Republic of Malta',
        ),
        CountryInfo(
            'MH',
            'MHL',
            '584',
            'Marshall Islands',
            'The Republic of the Marshall Islands',
        ),
        CountryInfo(
            'MQ',
            'MTQ',
            '474',
            'Martinique',
            'Martinique',
        ),
        CountryInfo(
            'MR',
            'MRT',
            '478',
            'Mauritania',
            'The Islamic Republic of Mauritania',
        ),
        CountryInfo(
            'MU',
            'MUS',
            '480',
            'Mauritius',
            'The Republic of Mauritius',
        ),
        CountryInfo(
            'YT',
            'MYT',
            '175',
            'Mayotte',
            'The Department of Mayotte',
        ),
        CountryInfo(
            'MX',
            'MEX',
            '484',
            'Mexico',
            'The United Mexican States',
        ),
        CountryInfo(
            'FM',
            'FSM',
            '583',
            'Micronesia (Federated States of)',
            'The Federated States of Micronesia',
        ),
        CountryInfo(
            'MD',
            'MDA',
            '498',
            'Moldova (the Republic of)',
            'The Republic of Moldova',
        ),
        CountryInfo(
            'MC',
            'MCO',
            '492',
            'Monaco',
            'The Principality of Monaco',
        ),
        CountryInfo(
            'MN',
            'MNG',
            '496',
            'Mongolia',
            'Mongolia',
        ),
        CountryInfo(
            'ME',
            'MNE',
            '499',
            'Montenegro',
            'Montenegro',
        ),
        CountryInfo(
            'MS',
            'MSR',
            '500',
            'Montserrat',
            'Montserrat',
        ),
        CountryInfo(
            'MA',
            'MAR',
            '504',
            'Morocco',
            'The Kingdom of Morocco',
        ),
        CountryInfo(
            'MZ',
            'MOZ',
            '508',
            'Mozambique',
            'The Republic of Mozambique',
        ),
        CountryInfo(
            'MM',
            'MMR',
            '104',
            'Myanmar',
            'The Republic of the Union of Myanmar',
        ),
        CountryInfo(
            'NA',
            'NAM',
            '516',
            'Namibia',
            'The Republic of Namibia',
        ),
        CountryInfo(
            'NR',
            'NRU',
            '520',
            'Nauru',
            'The Republic of Nauru',
        ),
        CountryInfo(
            'NP',
            'NPL',
            '524',
            'Nepal',
            'The Federal Democratic Republic of Nepal',
        ),
        CountryInfo(
            'NL',
            'NLD',
            '528',
            'Netherlands',
            'The Kingdom of the Netherlands',
        ),
        CountryInfo(
            'NC',
            'NCL',
            '540',
            'New Caledonia',
            'New Caledonia',
        ),
        CountryInfo(
            'NZ',
            'NZL',
            '554',
            'New Zealand',
            'New Zealand',
        ),
        CountryInfo(
            'NI',
            'NIC',
            '558',
            'Nicaragua',
            'The Republic of Nicaragua',
        ),
        CountryInfo(
            'NE',
            'NER',
            '562',
            'Niger',
            'The Republic of the Niger',
        ),
        CountryInfo(
            'NG',
            'NGA',
            '566',
            'Nigeria',
            'The Federal Republic of Nigeria',
        ),
        CountryInfo(
            'NU',
            'NIU',
            '570',
            'Niue',
            'Niue',
        ),
        CountryInfo(
            'NF',
            'NFK',
            '574',
            'Norfolk Island',
            'The Territory of Norfolk Island',
        ),
        CountryInfo(
            'MP',
            'MNP',
            '580',
            'Northern Mariana Islands',
            'The Commonwealth of the Northern Mariana Islands',
        ),
        CountryInfo(
            'NO',
            'NOR',
            '578',
            'Norway',
            'The Kingdom of Norway',
        ),
        CountryInfo(
            'OM',
            'OMN',
            '512',
            'Oman',
            'The Sultanate of Oman',
        ),
        CountryInfo(
            'PK',
            'PAK',
            '586',
            'Pakistan',
            'The Islamic Republic of Pakistan',
        ),
        CountryInfo(
            'PW',
            'PLW',
            '585',
            'Palau',
            'The Republic of Palau',
        ),
        CountryInfo(
            'PA',
            'PAN',
            '591',
            'Panama',
            'The Republic of Panamá',
        ),
        CountryInfo(
            'PG',
            'PNG',
            '598',
            'Papua New Guinea',
            'The Independent State of Papua New Guinea',
        ),
        CountryInfo(
            'PY',
            'PRY',
            '600',
            'Paraguay',
            'The Republic of Paraguay',
        ),
        CountryInfo(
            'PE',
            'PER',
            '604',
            'Peru',
            'The Republic of Perú',
        ),
        CountryInfo(
            'PH',
            'PHL',
            '608',
            'Philippines',
            'The Republic of the Philippines',
        ),
        CountryInfo(
            'PN',
            'PCN',
            '612',
            'Pitcairn',
            'The Pitcairn, Henderson, Ducie and Oeno Islands',
        ),
        CountryInfo(
            'PL',
            'POL',
            '616',
            'Poland',
            'The Republic of Poland',
        ),
        CountryInfo(
            'PT',
            'PRT',
            '620',
            'Portugal',
            'The Portuguese Republic',
        ),
        CountryInfo(
            'PR',
            'PRI',
            '630',
            'Puerto Rico',
            'The Commonwealth of Puerto Rico',
        ),
        CountryInfo(
            'QA',
            'QAT',
            '634',
            'Qatar',
            'The State of Qatar',
        ),
        CountryInfo(
            'RE',
            'REU',
            '638',
            'Réunion',
            'Réunion',
        ),
        CountryInfo(
            'RO',
            'ROU',
            '642',
            'Romania',
            'Romania',
        ),
        CountryInfo(
            'RU',
            'RUS',
            '643',
            'Russian Federation',
            'The Russian Federation',
        ),
        CountryInfo(
            'RW',
            'RWA',
            '646',
            'Rwanda',
            'The Republic of Rwanda',
        ),
        CountryInfo(
            'BL',
            'BLM',
            '652',
            'Saint Barthélemy',
            'The Collectivity of Saint-Barthélemy',
        ),
        CountryInfo(
            'SH',
            'SHN',
            '654',
            'Saint Helena Ascension Island Tristan da Cunha',
            'Saint Helena, Ascension and Tristan da Cunha',
        ),
        CountryInfo(
            'KN',
            'KNA',
            '659',
            'Saint Kitts and Nevis',
            'Saint Kitts and Nevis',
        ),
        CountryInfo(
            'LC',
            'LCA',
            '662',
            'Saint Lucia',
            'Saint Lucia',
        ),
        CountryInfo(
            'MF',
            'MAF',
            '663',
            'Saint Martin (French part)',
            'The Collectivity of Saint-Martin',
        ),
        CountryInfo(
            'PM',
            'SPM',
            '666',
            'Saint Pierre and Miquelon',
            'The Overseas Collectivity of Saint-Pierre and Miquelon',
        ),
        CountryInfo(
            'VC',
            'VCT',
            '670',
            'Saint Vincent and the Grenadines',
            'Saint Vincent and the Grenadines',
        ),
        CountryInfo(
            'WS',
            'WSM',
            '882',
            'Samoa',
            'The Independent State of Samoa',
        ),
        CountryInfo(
            'SM',
            'SMR',
            '674',
            'San Marino',
            'The Republic of San Marino',
        ),
        CountryInfo(
            'ST',
            'STP',
            '678',
            'Sao Tome and Principe',
            'The Democratic Republic of São Tomé and Príncipe',
        ),
        CountryInfo(
            'SA',
            'SAU',
            '682',
            'Saudi Arabia',
            'The Kingdom of Saudi Arabia',
        ),
        CountryInfo(
            'SN',
            'SEN',
            '686',
            'Senegal',
            'The Republic of Senegal',
        ),
        CountryInfo(
            'RS',
            'SRB',
            '688',
            'Serbia',
            'The Republic of Serbia',
        ),
        CountryInfo(
            'SC',
            'SYC',
            '690',
            'Seychelles',
            'The Republic of Seychelles',
        ),
        CountryInfo(
            'SL',
            'SLE',
            '694',
            'Sierra Leone',
            'The Republic of Sierra Leone',
        ),
        CountryInfo(
            'SG',
            'SGP',
            '702',
            'Singapore',
            'The Republic of Singapore',
        ),
        CountryInfo(
            'SX',
            'SXM',
            '534',
            'Sint Maarten (Dutch part)',
            'Sint Maarten',
        ),
        CountryInfo(
            'SK',
            'SVK',
            '703',
            'Slovakia',
            'The Slovak Republic',
        ),
        CountryInfo(
            'SI',
            'SVN',
            '705',
            'Slovenia',
            'The Republic of Slovenia',
        ),
        CountryInfo(
            'SB',
            'SLB',
            '090',
            'Solomon Islands',
            'The Solomon Islands',
        ),
        CountryInfo(
            'SO',
            'SOM',
            '706',
            'Somalia',
            'The Federal Republic of Somalia',
        ),
        CountryInfo(
            'ZA',
            'ZAF',
            '710',
            'South Africa',
            'The Republic of South Africa',
        ),
        CountryInfo(
            'GS',
            'SGS',
            '239',
            'South Georgia and the South Sandwich Islands',
            'South Georgia and the South Sandwich Islands',
        ),
        CountryInfo(
            'SS',
            'SSD',
            '728',
            'South Sudan',
            'The Republic of South Sudan',
        ),
        CountryInfo(
            'ES',
            'ESP',
            '724',
            'Spain',
            'The Kingdom of Spain',
        ),
        CountryInfo(
            'LK',
            'LKA',
            '144',
            'Sri Lanka',
            'The Democratic Socialist Republic of Sri Lanka',
        ),
        CountryInfo(
            'SD',
            'SDN',
            '729',
            'Sudan',
            'The Republic of the Sudan',
        ),
        CountryInfo(
            'SR',
            'SUR',
            '740',
            'Suriname',
            'The Republic of Suriname',
        ),
        CountryInfo(
            'SJ',
            'SJM',
            '744',
            'Svalbard Jan Mayen',
            'Svalbard and Jan Mayen',
        ),
        CountryInfo(
            'SE',
            'SWE',
            '752',
            'Sweden',
            'The Kingdom of Sweden',
        ),
        CountryInfo(
            'CH',
            'CHE',
            '756',
            'Switzerland',
            'The Swiss Confederation',
        ),
        CountryInfo(
            'SY',
            'SYR',
            '760',
            'Syrian Arab Republic',
            'The Syrian Arab Republic',
        ),
        CountryInfo(
            'TW',
            'TWN',
            '158',
            'Taiwan (Province of China)',
            'The Republic of China',
        ),
        CountryInfo(
            'TJ',
            'TJK',
            '762',
            'Tajikistan',
            'The Republic of Tajikistan',
        ),
        CountryInfo(
            'TZ',
            'TZA',
            '834',
            'Tanzania, the United Republic of',
            'The United Republic of Tanzania',
        ),
        CountryInfo(
            'TH',
            'THA',
            '764',
            'Thailand',
            'The Kingdom of Thailand',
        ),
        CountryInfo(
            'TL',
            'TLS',
            '626',
            'Timor-Leste',
            'The Democratic Republic of Timor-Leste',
        ),
        CountryInfo(
            'TG',
            'TGO',
            '768',
            'Togo',
            'The Togolese Republic',
        ),
        CountryInfo(
            'TK',
            'TKL',
            '772',
            'Tokelau',
            'Tokelau',
        ),
        CountryInfo(
            'TO',
            'TON',
            '776',
            'Tonga',
            'The Kingdom of Tonga',
        ),
        CountryInfo(
            'TT',
            'TTO',
            '780',
            'Trinidad and Tobago',
            'The Republic of Trinidad and Tobago',
        ),
        CountryInfo(
            'TN',
            'TUN',
            '788',
            'Tunisia',
            'The Republic of Tunisia',
        ),
        CountryInfo(
            'TR',
            'TUR',
            '792',
            'Türkiye [ab]',
            'The Republic of Türkiye',
        ),
        CountryInfo(
            'TM',
            'TKM',
            '795',
            'Turkmenistan',
            'Turkmenistan',
        ),
        CountryInfo(
            'TC',
            'TCA',
            '796',
            'Turks and Caicos Islands',
            'The Turks and Caicos Islands',
        ),
        CountryInfo(
            'TV',
            'TUV',
            '798',
            'Tuvalu',
            'Tuvalu',
        ),
        CountryInfo(
            'UG',
            'UGA',
            '800',
            'Uganda',
            'The Republic of Uganda',
        ),
        CountryInfo(
            'UA',
            'UKR',
            '804',
            'Ukraine',
            'Ukraine',
        ),
        CountryInfo(
            'AE',
            'ARE',
            '784',
            'United Arab Emirates',
            'The United Arab Emirates',
        ),
        CountryInfo(
            'GB',
            'GBR',
            '826',
            'United Kingdom of Great Britain and Northern Ireland',
            'The United Kingdom of Great Britain and Northern Ireland',
        ),
        CountryInfo(
            'UM',
            'UMI',
            '581',
            'United States Minor Outlying Islands',
            'Baker Island, Howland Island, Jarvis Island, Johnston Atoll, Kingman Reef, Midway Atoll,'
            ' Navassa Island, Palmyra Atoll, and Wake Island',
        ),
        CountryInfo(
            'US',
            'USA',
            '840',
            'United States of America',
            'The United States of America',
        ),
        CountryInfo(
            'UY',
            'URY',
            '858',
            'Uruguay',
            'The Oriental Republic of Uruguay',
        ),
        CountryInfo(
            'UZ',
            'UZB',
            '860',
            'Uzbekistan',
            'The Republic of Uzbekistan',
        ),
        CountryInfo(
            'VU',
            'VUT',
            '548',
            'Vanuatu',
            'The Republic of Vanuatu',
        ),
        CountryInfo(
            'VE',
            'VEN',
            '862',
            'Venezuela (Bolivarian Republic of)',
            'The Bolivarian Republic of Venezuela',
        ),
        CountryInfo(
            'VN',
            'VNM',
            '704',
            'Viet Nam',
            'The Socialist Republic of Viet Nam',
        ),
        CountryInfo(
            'VG',
            'VGB',
            '092',
            'Virgin Islands (British)',
            'The Virgin Islands',
        ),
        CountryInfo(
            'VI',
            'VIR',
            '850',
            'Virgin Islands (U.S.)',
            'The Virgin Islands of the United States',
        ),
        CountryInfo(
            'WF',
            'WLF',
            '876',
            'Wallis and Futuna',
            'The Territory of the Wallis and Futuna Islands',
        ),
        CountryInfo(
            'EH',
            'ESH',
            '732',
            'Western Sahara',
            'The Sahrawi Arab Democratic Republic',
        ),
        CountryInfo(
            'YE',
            'YEM',
            '887',
            'Yemen',
            'The Republic of Yemen',
        ),
        CountryInfo(
            'ZM',
            'ZMB',
            '894',
            'Zambia',
            'The Republic of Zambia',
        ),
        CountryInfo(
            'ZW',
            'ZWE',
            '716',
            'Zimbabwe',
            'The Republic of Zimbabwe',
        ),
    ]


@lru_cache()
def _index_by_alpha2() -> Dict[str, CountryInfo]:
    return {country.alpha2: country for country in _countries()}


@lru_cache()
def _index_by_alpha3() -> Dict[str, CountryInfo]:
    return {country.alpha3: country for country in _countries()}


@lru_cache()
def _index_by_numeric_code() -> Dict[str, CountryInfo]:
    return {country.numeric_code: country for country in _countries()}


@lru_cache()
def _index_by_short_name() -> Dict[str, CountryInfo]:
    return {country.short_name: country for country in _countries()}


@lru_cache()
def _index_by_official_name() -> Dict[str, CountryInfo]:
    return {country.official_name: country for country in _countries()}


class CountryAlpha2(str):
    @classmethod
    def _validate(cls, __input_value: str, **kwargs: Any) -> 'CountryAlpha2':
        if __input_value not in _index_by_alpha2():
            raise PydanticCustomError('country_alpha2', 'Invalid country alpha2 code')
        return cls(__input_value)

    @classmethod
    def __get_pydantic_core_schema__(cls, **_kwargs: Any) -> core_schema.FunctionSchema:
        return core_schema.function_after_schema(
            core_schema.str_schema(to_upper=True), cls._validate, serialization=core_schema.to_string_ser_schema()
        )

    @property
    def alpha3(self) -> str:
        return _index_by_alpha2()[self].alpha3

    @property
    def numeric_code(self) -> str:
        return _index_by_alpha2()[self].numeric_code

    @property
    def short_name(self) -> str:
        return _index_by_alpha2()[self].short_name

    @property
    def official_name(self) -> str:
        return _index_by_alpha2()[self].official_name


class CountryAlpha3(str):
    @classmethod
    def _validate(cls, __input_value: str, **kwargs: Any) -> 'CountryAlpha3':
        if __input_value not in _index_by_alpha3():
            raise PydanticCustomError('country_alpha3', 'Invalid country alpha3 code')
        return cls(__input_value)

    @classmethod
    def __get_pydantic_core_schema__(cls, **_kwargs: Any) -> core_schema.FunctionSchema:
        return core_schema.function_after_schema(
            core_schema.str_schema(to_upper=True), cls._validate, serialization=core_schema.to_string_ser_schema()
        )

    @property
    def alpha2(self) -> str:
        return _index_by_alpha3()[self].alpha2

    @property
    def numeric_code(self) -> str:
        return _index_by_alpha3()[self].numeric_code

    @property
    def short_name(self) -> str:
        return _index_by_alpha3()[self].short_name

    @property
    def official_name(self) -> str:
        return _index_by_alpha3()[self].official_name


class CountryNumericCode(str):
    @classmethod
    def _validate(cls, __input_value: str, **kwargs: Any) -> 'CountryNumericCode':
        if __input_value not in _index_by_numeric_code():
            raise PydanticCustomError('country_numeric_code', 'Invalid country numeric code')
        return cls(__input_value)

    @classmethod
    def __get_pydantic_core_schema__(cls, **_kwargs: Any) -> core_schema.FunctionSchema:
        return core_schema.function_after_schema(
            core_schema.str_schema(to_upper=True), cls._validate, serialization=core_schema.to_string_ser_schema()
        )

    @property
    def alpha2(self) -> str:
        return _index_by_numeric_code()[self].alpha2

    @property
    def alpha3(self) -> str:
        return _index_by_numeric_code()[self].alpha3

    @property
    def short_name(self) -> str:
        return _index_by_numeric_code()[self].short_name

    @property
    def official_name(self) -> str:
        return _index_by_numeric_code()[self].official_name


class CountryShortName(str):
    @classmethod
    def _validate(cls, __input_value: str, **kwargs: Any) -> 'CountryShortName':
        if __input_value not in _index_by_short_name():
            raise PydanticCustomError('country_short_name', 'Invalid country short name')
        return cls(__input_value)

    @classmethod
    def __get_pydantic_core_schema__(cls, **_kwargs: Any) -> core_schema.FunctionSchema:
        return core_schema.function_after_schema(
            core_schema.str_schema(), cls._validate, serialization=core_schema.to_string_ser_schema()
        )

    @property
    def alpha2(self) -> str:
        return _index_by_short_name()[self].alpha2

    @property
    def alpha3(self) -> str:
        return _index_by_short_name()[self].alpha3

    @property
    def numeric_code(self) -> str:
        return _index_by_short_name()[self].numeric_code

    @property
    def official_name(self) -> str:
        return _index_by_short_name()[self].official_name


class CountryOfficialName(str):
    @classmethod
    def _validate(cls, __input_value: str, **kwargs: Any) -> 'CountryOfficialName':
        if __input_value not in _index_by_official_name():
            raise PydanticCustomError('country_numeric_code', 'Invalid country official name')
        return cls(__input_value)

    @classmethod
    def __get_pydantic_core_schema__(cls, **_kwargs: Any) -> core_schema.FunctionSchema:
        return core_schema.function_after_schema(
            core_schema.str_schema(), cls._validate, serialization=core_schema.to_string_ser_schema()
        )

    @property
    def alpha2(self) -> str:
        return _index_by_official_name()[self].alpha2

    @property
    def alpha3(self) -> str:
        return _index_by_official_name()[self].alpha3

    @property
    def numeric_code(self) -> str:
        return _index_by_official_name()[self].numeric_code

    @property
    def short_name(self) -> str:
        return _index_by_official_name()[self].short_name
