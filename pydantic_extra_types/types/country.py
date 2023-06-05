"""
Country definitions that are based on the ISO 3166 format
Based on: https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes
"""
from dataclasses import dataclass
from functools import lru_cache
from typing import Dict, List, Type, TypeVar

from pydantic_core import PydanticCustomError, core_schema

from pydantic import GetCoreSchemaHandler

T = TypeVar("T")


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
            "BB",
            "BRB",
            "052",
            "Barbados",
            "Barbados",
        ),
        CountryInfo(
            "RE",
            "REU",
            "638",
            "Réunion",
            "Réunion Island",
        ),
        CountryInfo(
            "SR",
            "SUR",
            "740",
            "Suriname",
            "Republic of Suriname",
        ),
        CountryInfo(
            "NA",
            "NAM",
            "516",
            "Namibia",
            "Republic of Namibia",
        ),
        CountryInfo(
            "GN",
            "GIN",
            "324",
            "Guinea",
            "Republic of Guinea",
        ),
        CountryInfo(
            "VU",
            "VUT",
            "548",
            "Vanuatu",
            "Republic of Vanuatu",
        ),
        CountryInfo(
            "WS",
            "WSM",
            "882",
            "Samoa",
            "Independent State of Samoa",
        ),
        CountryInfo(
            "FR",
            "FRA",
            "250",
            "France",
            "French Republic",
        ),
        CountryInfo(
            "AD",
            "AND",
            "020",
            "Andorra",
            "Principality of Andorra",
        ),
        CountryInfo(
            "AZ",
            "AZE",
            "031",
            "Azerbaijan",
            "Republic of Azerbaijan",
        ),
        CountryInfo(
            "MV",
            "MDV",
            "462",
            "Maldives",
            "Republic of the Maldives",
        ),
        CountryInfo(
            "PF",
            "PYF",
            "258",
            "French Polynesia",
            "French Polynesia",
        ),
        CountryInfo(
            "LC",
            "LCA",
            "662",
            "Saint Lucia",
            "Saint Lucia",
        ),
        CountryInfo(
            "PA",
            "PAN",
            "591",
            "Panama",
            "Republic of Panama",
        ),
        CountryInfo(
            "TL",
            "TLS",
            "626",
            "Timor-Leste",
            "Democratic Republic of Timor-Leste",
        ),
        CountryInfo(
            "MK",
            "MKD",
            "807",
            "North Macedonia",
            "Republic of North Macedonia",
        ),
        CountryInfo(
            "DK",
            "DNK",
            "208",
            "Denmark",
            "Kingdom of Denmark",
        ),
        CountryInfo(
            "EG",
            "EGY",
            "818",
            "Egypt",
            "Arab Republic of Egypt",
        ),
        CountryInfo(
            "EE",
            "EST",
            "233",
            "Estonia",
            "Republic of Estonia",
        ),
        CountryInfo(
            "CZ",
            "CZE",
            "203",
            "Czechia",
            "Czech Republic",
        ),
        CountryInfo(
            "BS",
            "BHS",
            "044",
            "Bahamas",
            "Commonwealth of the Bahamas",
        ),
        CountryInfo(
            "UY",
            "URY",
            "858",
            "Uruguay",
            "Oriental Republic of Uruguay",
        ),
        CountryInfo(
            "AX",
            "ALA",
            "248",
            "Åland Islands",
            "Åland Islands",
        ),
        CountryInfo(
            "KM",
            "COM",
            "174",
            "Comoros",
            "Union of the Comoros",
        ),
        CountryInfo(
            "CK",
            "COK",
            "184",
            "Cook Islands",
            "Cook Islands",
        ),
        CountryInfo(
            "CR",
            "CRI",
            "188",
            "Costa Rica",
            "Republic of Costa Rica",
        ),
        CountryInfo(
            "TG",
            "TGO",
            "768",
            "Togo",
            "Togolese Republic",
        ),
        CountryInfo(
            "ST",
            "STP",
            "678",
            "São Tomé and Príncipe",
            "Democratic Republic of São Tomé and Príncipe",
        ),
        CountryInfo(
            "NL",
            "NLD",
            "528",
            "Netherlands",
            "Kingdom of the Netherlands",
        ),
        CountryInfo(
            "HK",
            "HKG",
            "344",
            "Hong Kong",
            "Hong Kong Special Administrative Region of the People's Republic of China",
        ),
        CountryInfo(
            "AU",
            "AUS",
            "036",
            "Australia",
            "Commonwealth of Australia",
        ),
        CountryInfo(
            "MY",
            "MYS",
            "458",
            "Malaysia",
            "Malaysia",
        ),
        CountryInfo(
            "NP",
            "NPL",
            "524",
            "Nepal",
            "Federal Democratic Republic of Nepal",
        ),
        CountryInfo(
            "CU",
            "CUB",
            "192",
            "Cuba",
            "Republic of Cuba",
        ),
        CountryInfo(
            "KP",
            "PRK",
            "408",
            "North Korea",
            "Democratic People's Republic of Korea",
        ),
        CountryInfo(
            "GF",
            "GUF",
            "254",
            "French Guiana",
            "Guiana",
        ),
        CountryInfo(
            "MD",
            "MDA",
            "498",
            "Moldova",
            "Republic of Moldova",
        ),
        CountryInfo(
            "ZM",
            "ZMB",
            "894",
            "Zambia",
            "Republic of Zambia",
        ),
        CountryInfo(
            "DM",
            "DMA",
            "212",
            "Dominica",
            "Commonwealth of Dominica",
        ),
        CountryInfo(
            "MH",
            "MHL",
            "584",
            "Marshall Islands",
            "Republic of the Marshall Islands",
        ),
        CountryInfo(
            "TO",
            "TON",
            "776",
            "Tonga",
            "Kingdom of Tonga",
        ),
        CountryInfo(
            "PE",
            "PER",
            "604",
            "Peru",
            "Republic of Peru",
        ),
        CountryInfo(
            "CV",
            "CPV",
            "132",
            "Cape Verde",
            "Republic of Cabo Verde",
        ),
        CountryInfo(
            "KI",
            "KIR",
            "296",
            "Kiribati",
            "Independent and Sovereign Republic of Kiribati",
        ),
        CountryInfo(
            "FI",
            "FIN",
            "246",
            "Finland",
            "Republic of Finland",
        ),
        CountryInfo(
            "CI",
            "CIV",
            "384",
            "Ivory Coast",
            "Republic of Côte d'Ivoire",
        ),
        CountryInfo(
            "MQ",
            "MTQ",
            "474",
            "Martinique",
            "Martinique",
        ),
        CountryInfo(
            "PK",
            "PAK",
            "586",
            "Pakistan",
            "Islamic Republic of Pakistan",
        ),
        CountryInfo(
            "DJ",
            "DJI",
            "262",
            "Djibouti",
            "Republic of Djibouti",
        ),
        CountryInfo(
            "TC",
            "TCA",
            "796",
            "Turks and Caicos Islands",
            "Turks and Caicos Islands",
        ),
        CountryInfo(
            "FM",
            "FSM",
            "583",
            "Micronesia",
            "Federated States of Micronesia",
        ),
        CountryInfo(
            "SI",
            "SVN",
            "705",
            "Slovenia",
            "Republic of Slovenia",
        ),
        CountryInfo(
            "KG",
            "KGZ",
            "417",
            "Kyrgyzstan",
            "Kyrgyz Republic",
        ),
        CountryInfo(
            "BQ",
            "BES",
            "535",
            "Caribbean Netherlands",
            "Bonaire, Sint Eustatius and Saba",
        ),
        CountryInfo(
            "TF",
            "ATF",
            "260",
            "French Southern and Antarctic Lands",
            "Territory of the French Southern and Antarctic Lands",
        ),
        CountryInfo(
            "BL",
            "BLM",
            "652",
            "Saint Barthélemy",
            "Collectivity of Saint Barthélemy",
        ),
        CountryInfo(
            "CH",
            "CHE",
            "756",
            "Switzerland",
            "Swiss Confederation",
        ),
        CountryInfo(
            "KW",
            "KWT",
            "414",
            "Kuwait",
            "State of Kuwait",
        ),
        CountryInfo(
            "SC",
            "SYC",
            "690",
            "Seychelles",
            "Republic of Seychelles",
        ),
        CountryInfo(
            "GB",
            "GBR",
            "826",
            "United Kingdom",
            "United Kingdom of Great Britain and Northern Ireland",
        ),
        CountryInfo(
            "VI",
            "VIR",
            "850",
            "United States Virgin Islands",
            "Virgin Islands of the United States",
        ),
        CountryInfo(
            "FJ",
            "FJI",
            "242",
            "Fiji",
            "Republic of Fiji",
        ),
        CountryInfo(
            "YE",
            "YEM",
            "887",
            "Yemen",
            "Republic of Yemen",
        ),
        CountryInfo(
            "VG",
            "VGB",
            "092",
            "British Virgin Islands",
            "Virgin Islands",
        ),
        CountryInfo(
            "BV",
            "BVT",
            "074",
            "Bouvet Island",
            "Bouvet Island",
        ),
        CountryInfo(
            "CF",
            "CAF",
            "140",
            "Central African Republic",
            "Central African Republic",
        ),
        CountryInfo(
            "BE",
            "BEL",
            "056",
            "Belgium",
            "Kingdom of Belgium",
        ),
        CountryInfo(
            "CW",
            "CUW",
            "531",
            "Curaçao",
            "Country of Curaçao",
        ),
        CountryInfo(
            "AR",
            "ARG",
            "032",
            "Argentina",
            "Argentine Republic",
        ),
        CountryInfo(
            "MG",
            "MDG",
            "450",
            "Madagascar",
            "Republic of Madagascar",
        ),
        CountryInfo(
            "ZA",
            "ZAF",
            "710",
            "South Africa",
            "Republic of South Africa",
        ),
        CountryInfo(
            "LV",
            "LVA",
            "428",
            "Latvia",
            "Republic of Latvia",
        ),
        CountryInfo(
            "ZW",
            "ZWE",
            "716",
            "Zimbabwe",
            "Republic of Zimbabwe",
        ),
        CountryInfo(
            "AQ",
            "ATA",
            "010",
            "Antarctica",
            "Antarctica",
        ),
        CountryInfo(
            "GG",
            "GGY",
            "831",
            "Guernsey",
            "Bailiwick of Guernsey",
        ),
        CountryInfo(
            "GA",
            "GAB",
            "266",
            "Gabon",
            "Gabonese Republic",
        ),
        CountryInfo(
            "RO",
            "ROU",
            "642",
            "Romania",
            "Romania",
        ),
        CountryInfo(
            "DE",
            "DEU",
            "276",
            "Germany",
            "Federal Republic of Germany",
        ),
        CountryInfo(
            "BD",
            "BGD",
            "050",
            "Bangladesh",
            "People's Republic of Bangladesh",
        ),
        CountryInfo(
            "MS",
            "MSR",
            "500",
            "Montserrat",
            "Montserrat",
        ),
        CountryInfo(
            "JO",
            "JOR",
            "400",
            "Jordan",
            "Hashemite Kingdom of Jordan",
        ),
        CountryInfo(
            "MZ",
            "MOZ",
            "508",
            "Mozambique",
            "Republic of Mozambique",
        ),
        CountryInfo(
            "IL",
            "ISR",
            "376",
            "Israel",
            "State of Israel",
        ),
        CountryInfo(
            "ER",
            "ERI",
            "232",
            "Eritrea",
            "State of Eritrea",
        ),
        CountryInfo(
            "ID",
            "IDN",
            "360",
            "Indonesia",
            "Republic of Indonesia",
        ),
        CountryInfo(
            "IM",
            "IMN",
            "833",
            "Isle of Man",
            "Isle of Man",
        ),
        CountryInfo(
            "JP",
            "JPN",
            "392",
            "Japan",
            "Japan",
        ),
        CountryInfo(
            "ES",
            "ESP",
            "724",
            "Spain",
            "Kingdom of Spain",
        ),
        CountryInfo(
            "AF",
            "AFG",
            "004",
            "Afghanistan",
            "Islamic Republic of Afghanistan",
        ),
        CountryInfo(
            "AE",
            "ARE",
            "784",
            "United Arab Emirates",
            "United Arab Emirates",
        ),
        CountryInfo(
            "MW",
            "MWI",
            "454",
            "Malawi",
            "Republic of Malawi",
        ),
        CountryInfo(
            "TR",
            "TUR",
            "792",
            "Turkey",
            "Republic of Turkey",
        ),
        CountryInfo(
            "BY",
            "BLR",
            "112",
            "Belarus",
            "Republic of Belarus",
        ),
        CountryInfo(
            "ME",
            "MNE",
            "499",
            "Montenegro",
            "Montenegro",
        ),
        CountryInfo(
            "BA",
            "BIH",
            "070",
            "Bosnia and Herzegovina",
            "Bosnia and Herzegovina",
        ),
        CountryInfo(
            "SZ",
            "SWZ",
            "748",
            "Eswatini",
            "Kingdom of Eswatini",
        ),
        CountryInfo(
            "LT",
            "LTU",
            "440",
            "Lithuania",
            "Republic of Lithuania",
        ),
        CountryInfo(
            "TM",
            "TKM",
            "795",
            "Turkmenistan",
            "Turkmenistan",
        ),
        CountryInfo(
            "ET",
            "ETH",
            "231",
            "Ethiopia",
            "Federal Democratic Republic of Ethiopia",
        ),
        CountryInfo(
            "AI",
            "AIA",
            "660",
            "Anguilla",
            "Anguilla",
        ),
        CountryInfo(
            "HU",
            "HUN",
            "348",
            "Hungary",
            "Hungary",
        ),
        CountryInfo(
            "AS",
            "ASM",
            "016",
            "American Samoa",
            "American Samoa",
        ),
        CountryInfo(
            "TD",
            "TCD",
            "148",
            "Chad",
            "Republic of Chad",
        ),
        CountryInfo(
            "GP",
            "GLP",
            "312",
            "Guadeloupe",
            "Guadeloupe",
        ),
        CountryInfo(
            "NG",
            "NGA",
            "566",
            "Nigeria",
            "Federal Republic of Nigeria",
        ),
        CountryInfo(
            "SM",
            "SMR",
            "674",
            "San Marino",
            "Republic of San Marino",
        ),
        CountryInfo(
            "UA",
            "UKR",
            "804",
            "Ukraine",
            "Ukraine",
        ),
        CountryInfo(
            "HT",
            "HTI",
            "332",
            "Haiti",
            "Republic of Haiti",
        ),
        CountryInfo(
            "BW",
            "BWA",
            "072",
            "Botswana",
            "Republic of Botswana",
        ),
        CountryInfo(
            "PT",
            "PRT",
            "620",
            "Portugal",
            "Portuguese Republic",
        ),
        CountryInfo(
            "GY",
            "GUY",
            "328",
            "Guyana",
            "Co-operative Republic of Guyana",
        ),
        CountryInfo(
            "IE",
            "IRL",
            "372",
            "Ireland",
            "Republic of Ireland",
        ),
        CountryInfo(
            "NC",
            "NCL",
            "540",
            "New Caledonia",
            "New Caledonia",
        ),
        CountryInfo(
            "MF",
            "MAF",
            "663",
            "Saint Martin",
            "Saint Martin",
        ),
        CountryInfo(
            "MU",
            "MUS",
            "480",
            "Mauritius",
            "Republic of Mauritius",
        ),
        CountryInfo(
            "GI",
            "GIB",
            "292",
            "Gibraltar",
            "Gibraltar",
        ),
        CountryInfo(
            "KN",
            "KNA",
            "659",
            "Saint Kitts and Nevis",
            "Federation of Saint Christopher and Nevis",
        ),
        CountryInfo(
            "IS",
            "ISL",
            "352",
            "Iceland",
            "Iceland",
        ),
        CountryInfo(
            "SJ",
            "SJM",
            "744",
            "Svalbard and Jan Mayen",
            "Svalbard og Jan Mayen",
        ),
        CountryInfo(
            "CL",
            "CHL",
            "152",
            "Chile",
            "Republic of Chile",
        ),
        CountryInfo(
            "UM",
            "UMI",
            "581",
            "United States Minor Outlying Islands",
            "United States Minor Outlying Islands",
        ),
        CountryInfo(
            "KZ",
            "KAZ",
            "398",
            "Kazakhstan",
            "Republic of Kazakhstan",
        ),
        CountryInfo(
            "CN",
            "CHN",
            "156",
            "China",
            "People's Republic of China",
        ),
        CountryInfo(
            "MO",
            "MAC",
            "446",
            "Macau",
            "Macao Special Administrative Region of the People's Republic of China",
        ),
        CountryInfo(
            "AM",
            "ARM",
            "051",
            "Armenia",
            "Republic of Armenia",
        ),
        CountryInfo(
            "BO",
            "BOL",
            "068",
            "Bolivia",
            "Plurinational State of Bolivia",
        ),
        CountryInfo(
            "SD",
            "SDN",
            "729",
            "Sudan",
            "Republic of the Sudan",
        ),
        CountryInfo(
            "VN",
            "VNM",
            "704",
            "Vietnam",
            "Socialist Republic of Vietnam",
        ),
        CountryInfo(
            "WF",
            "WLF",
            "876",
            "Wallis and Futuna",
            "Territory of the Wallis and Futuna Islands",
        ),
        CountryInfo(
            "BI",
            "BDI",
            "108",
            "Burundi",
            "Republic of Burundi",
        ),
        CountryInfo(
            "CA",
            "CAN",
            "124",
            "Canada",
            "Canada",
        ),
        CountryInfo(
            "CO",
            "COL",
            "170",
            "Colombia",
            "Republic of Colombia",
        ),
        CountryInfo(
            "LS",
            "LSO",
            "426",
            "Lesotho",
            "Kingdom of Lesotho",
        ),
        CountryInfo(
            "BM",
            "BMU",
            "060",
            "Bermuda",
            "Bermuda",
        ),
        CountryInfo(
            "GT",
            "GTM",
            "320",
            "Guatemala",
            "Republic of Guatemala",
        ),
        CountryInfo(
            "UZ",
            "UZB",
            "860",
            "Uzbekistan",
            "Republic of Uzbekistan",
        ),
        CountryInfo(
            "KY",
            "CYM",
            "136",
            "Cayman Islands",
            "Cayman Islands",
        ),
        CountryInfo(
            "SN",
            "SEN",
            "686",
            "Senegal",
            "Republic of Senegal",
        ),
        CountryInfo(
            "GM",
            "GMB",
            "270",
            "Gambia",
            "Republic of the Gambia",
        ),
        CountryInfo(
            "LI",
            "LIE",
            "438",
            "Liechtenstein",
            "Principality of Liechtenstein",
        ),
        CountryInfo(
            "PN",
            "PCN",
            "612",
            "Pitcairn Islands",
            "Pitcairn Group of Islands",
        ),
        CountryInfo(
            "TV",
            "TUV",
            "798",
            "Tuvalu",
            "Tuvalu",
        ),
        CountryInfo(
            "GQ",
            "GNQ",
            "226",
            "Equatorial Guinea",
            "Republic of Equatorial Guinea",
        ),
        CountryInfo(
            "BT",
            "BTN",
            "064",
            "Bhutan",
            "Kingdom of Bhutan",
        ),
        CountryInfo(
            "AW",
            "ABW",
            "533",
            "Aruba",
            "Aruba",
        ),
        CountryInfo(
            "PY",
            "PRY",
            "600",
            "Paraguay",
            "Republic of Paraguay",
        ),
        CountryInfo(
            "GD",
            "GRD",
            "308",
            "Grenada",
            "Grenada",
        ),
        CountryInfo(
            "PG",
            "PNG",
            "598",
            "Papua New Guinea",
            "Independent State of Papua New Guinea",
        ),
        CountryInfo(
            "JM",
            "JAM",
            "388",
            "Jamaica",
            "Jamaica",
        ),
        CountryInfo(
            "CG",
            "COG",
            "178",
            "Republic of the Congo",
            "Republic of the Congo",
        ),
        CountryInfo(
            "PL",
            "POL",
            "616",
            "Poland",
            "Republic of Poland",
        ),
        CountryInfo(
            "RU",
            "RUS",
            "643",
            "Russia",
            "Russian Federation",
        ),
        CountryInfo(
            "MR",
            "MRT",
            "478",
            "Mauritania",
            "Islamic Republic of Mauritania",
        ),
        CountryInfo(
            "EH",
            "ESH",
            "732",
            "Western Sahara",
            "Sahrawi Arab Democratic Republic",
        ),
        CountryInfo(
            "BF",
            "BFA",
            "854",
            "Burkina Faso",
            "Burkina Faso",
        ),
        CountryInfo(
            "CD",
            "COD",
            "180",
            "DR Congo",
            "Democratic Republic of the Congo",
        ),
        CountryInfo(
            "BJ",
            "BEN",
            "204",
            "Benin",
            "Republic of Benin",
        ),
        CountryInfo(
            "UG",
            "UGA",
            "800",
            "Uganda",
            "Republic of Uganda",
        ),
        CountryInfo(
            "MN",
            "MNG",
            "496",
            "Mongolia",
            "Mongolia",
        ),
        CountryInfo(
            "LA",
            "LAO",
            "418",
            "Laos",
            "Lao People's Democratic Republic",
        ),
        CountryInfo(
            "DZ",
            "DZA",
            "012",
            "Algeria",
            "People's Democratic Republic of Algeria",
        ),
        CountryInfo(
            "BN",
            "BRN",
            "096",
            "Brunei",
            "Nation of Brunei, Abode of Peace",
        ),
        CountryInfo(
            "KE",
            "KEN",
            "404",
            "Kenya",
            "Republic of Kenya",
        ),
        CountryInfo(
            "LK",
            "LKA",
            "144",
            "Sri Lanka",
            "Democratic Socialist Republic of Sri Lanka",
        ),
        CountryInfo(
            "DO",
            "DOM",
            "214",
            "Dominican Republic",
            "Dominican Republic",
        ),
        CountryInfo(
            "AT",
            "AUT",
            "040",
            "Austria",
            "Republic of Austria",
        ),
        CountryInfo(
            "LU",
            "LUX",
            "442",
            "Luxembourg",
            "Grand Duchy of Luxembourg",
        ),
        CountryInfo(
            "GE",
            "GEO",
            "268",
            "Georgia",
            "Georgia",
        ),
        CountryInfo(
            "SK",
            "SVK",
            "703",
            "Slovakia",
            "Slovak Republic",
        ),
        CountryInfo(
            "NO",
            "NOR",
            "578",
            "Norway",
            "Kingdom of Norway",
        ),
        CountryInfo(
            "TH",
            "THA",
            "764",
            "Thailand",
            "Kingdom of Thailand",
        ),
        CountryInfo(
            "IO",
            "IOT",
            "086",
            "British Indian Ocean Territory",
            "British Indian Ocean Territory",
        ),
        CountryInfo(
            "IN",
            "IND",
            "356",
            "India",
            "Republic of India",
        ),
        CountryInfo(
            "MA",
            "MAR",
            "504",
            "Morocco",
            "Kingdom of Morocco",
        ),
        CountryInfo(
            "PM",
            "SPM",
            "666",
            "Saint Pierre and Miquelon",
            "Saint Pierre and Miquelon",
        ),
        CountryInfo(
            "GL",
            "GRL",
            "304",
            "Greenland",
            "Greenland",
        ),
        CountryInfo(
            "NI",
            "NIC",
            "558",
            "Nicaragua",
            "Republic of Nicaragua",
        ),
        CountryInfo(
            "QA",
            "QAT",
            "634",
            "Qatar",
            "State of Qatar",
        ),
        CountryInfo(
            "TW",
            "TWN",
            "158",
            "Taiwan",
            "Republic of China (Taiwan)",
        ),
        CountryInfo(
            "BR",
            "BRA",
            "076",
            "Brazil",
            "Federative Republic of Brazil",
        ),
        CountryInfo(
            "NZ",
            "NZL",
            "554",
            "New Zealand",
            "New Zealand",
        ),
        CountryInfo(
            "SG",
            "SGP",
            "702",
            "Singapore",
            "Republic of Singapore",
        ),
        CountryInfo(
            "SY",
            "SYR",
            "760",
            "Syria",
            "Syrian Arab Republic",
        ),
        CountryInfo(
            "BZ",
            "BLZ",
            "084",
            "Belize",
            "Belize",
        ),
        CountryInfo(
            "FK",
            "FLK",
            "238",
            "Falkland Islands",
            "Falkland Islands",
        ),
        CountryInfo(
            "VE",
            "VEN",
            "862",
            "Venezuela",
            "Bolivarian Republic of Venezuela",
        ),
        CountryInfo(
            "BH",
            "BHR",
            "048",
            "Bahrain",
            "Kingdom of Bahrain",
        ),
        CountryInfo(
            "CC",
            "CCK",
            "166",
            "Cocos (Keeling) Islands",
            "Territory of the Cocos (Keeling) Islands",
        ),
        CountryInfo(
            "MP",
            "MNP",
            "580",
            "Northern Mariana Islands",
            "Commonwealth of the Northern Mariana Islands",
        ),
        CountryInfo(
            "CM",
            "CMR",
            "120",
            "Cameroon",
            "Republic of Cameroon",
        ),
        CountryInfo(
            "CY",
            "CYP",
            "196",
            "Cyprus",
            "Republic of Cyprus",
        ),
        CountryInfo(
            "US",
            "USA",
            "840",
            "United States",
            "United States of America",
        ),
        CountryInfo(
            "AO",
            "AGO",
            "024",
            "Angola",
            "Republic of Angola",
        ),
        CountryInfo(
            "TN",
            "TUN",
            "788",
            "Tunisia",
            "Tunisian Republic",
        ),
        CountryInfo(
            "MC",
            "MCO",
            "492",
            "Monaco",
            "Principality of Monaco",
        ),
        CountryInfo(
            "RW",
            "RWA",
            "646",
            "Rwanda",
            "Republic of Rwanda",
        ),
        CountryInfo(
            "TT",
            "TTO",
            "780",
            "Trinidad and Tobago",
            "Republic of Trinidad and Tobago",
        ),
        CountryInfo(
            "MT",
            "MLT",
            "470",
            "Malta",
            "Republic of Malta",
        ),
        CountryInfo(
            "MX",
            "MEX",
            "484",
            "Mexico",
            "United Mexican States",
        ),
        CountryInfo(
            "YT",
            "MYT",
            "175",
            "Mayotte",
            "Department of Mayotte",
        ),
        CountryInfo(
            "AG",
            "ATG",
            "028",
            "Antigua and Barbuda",
            "Antigua and Barbuda",
        ),
        CountryInfo(
            "TK",
            "TKL",
            "772",
            "Tokelau",
            "Tokelau",
        ),
        CountryInfo(
            "KR",
            "KOR",
            "410",
            "South Korea",
            "Republic of Korea",
        ),
        CountryInfo(
            "NE",
            "NER",
            "562",
            "Niger",
            "Republic of Niger",
        ),
        CountryInfo(
            "AL",
            "ALB",
            "008",
            "Albania",
            "Republic of Albania",
        ),
        CountryInfo(
            "SO",
            "SOM",
            "706",
            "Somalia",
            "Federal Republic of Somalia",
        ),
        CountryInfo(
            "LR",
            "LBR",
            "430",
            "Liberia",
            "Republic of Liberia",
        ),
        CountryInfo(
            "MM",
            "MMR",
            "104",
            "Myanmar",
            "Republic of the Union of Myanmar",
        ),
        CountryInfo(
            "TZ",
            "TZA",
            "834",
            "Tanzania",
            "United Republic of Tanzania",
        ),
        CountryInfo(
            "IQ",
            "IRQ",
            "368",
            "Iraq",
            "Republic of Iraq",
        ),
        CountryInfo(
            "GS",
            "SGS",
            "239",
            "South Georgia",
            "South Georgia and the South Sandwich Islands",
        ),
        CountryInfo(
            "VC",
            "VCT",
            "670",
            "Saint Vincent and the Grenadines",
            "Saint Vincent and the Grenadines",
        ),
        CountryInfo(
            "LY",
            "LBY",
            "434",
            "Libya",
            "State of Libya",
        ),
        CountryInfo(
            "SL",
            "SLE",
            "694",
            "Sierra Leone",
            "Republic of Sierra Leone",
        ),
        CountryInfo(
            "SX",
            "SXM",
            "534",
            "Sint Maarten",
            "Sint Maarten",
        ),
        CountryInfo(
            "RS",
            "SRB",
            "688",
            "Serbia",
            "Republic of Serbia",
        ),
        CountryInfo(
            "HM",
            "HMD",
            "334",
            "Heard Island and McDonald Islands",
            "Heard Island and McDonald Islands",
        ),
        CountryInfo(
            "GH",
            "GHA",
            "288",
            "Ghana",
            "Republic of Ghana",
        ),
        CountryInfo(
            "SS",
            "SSD",
            "728",
            "South Sudan",
            "Republic of South Sudan",
        ),
        CountryInfo(
            "SE",
            "SWE",
            "752",
            "Sweden",
            "Kingdom of Sweden",
        ),
        CountryInfo(
            "GR",
            "GRC",
            "300",
            "Greece",
            "Hellenic Republic",
        ),
        CountryInfo(
            "FO",
            "FRO",
            "234",
            "Faroe Islands",
            "Faroe Islands",
        ),
        CountryInfo(
            "PH",
            "PHL",
            "608",
            "Philippines",
            "Republic of the Philippines",
        ),
        CountryInfo(
            "GW",
            "GNB",
            "624",
            "Guinea-Bissau",
            "Republic of Guinea-Bissau",
        ),
        CountryInfo(
            "SA",
            "SAU",
            "682",
            "Saudi Arabia",
            "Kingdom of Saudi Arabia",
        ),
        CountryInfo(
            "PW",
            "PLW",
            "585",
            "Palau",
            "Republic of Palau",
        ),
        CountryInfo(
            "BG",
            "BGR",
            "100",
            "Bulgaria",
            "Republic of Bulgaria",
        ),
        CountryInfo(
            "NR",
            "NRU",
            "520",
            "Nauru",
            "Republic of Nauru",
        ),
        CountryInfo(
            "KH",
            "KHM",
            "116",
            "Cambodia",
            "Kingdom of Cambodia",
        ),
        CountryInfo(
            "JE",
            "JEY",
            "832",
            "Jersey",
            "Bailiwick of Jersey",
        ),
        CountryInfo(
            "PS",
            "PSE",
            "275",
            "Palestine",
            "State of Palestine",
        ),
        CountryInfo(
            "IT",
            "ITA",
            "380",
            "Italy",
            "Italian Republic",
        ),
        CountryInfo(
            "ML",
            "MLI",
            "466",
            "Mali",
            "Republic of Mali",
        ),
        CountryInfo(
            "IR",
            "IRN",
            "364",
            "Iran",
            "Islamic Republic of Iran",
        ),
        CountryInfo(
            "NU",
            "NIU",
            "570",
            "Niue",
            "Niue",
        ),
        CountryInfo(
            "TJ",
            "TJK",
            "762",
            "Tajikistan",
            "Republic of Tajikistan",
        ),
        CountryInfo(
            "XK",
            "UNK",
            "",
            "Kosovo",
            "Republic of Kosovo",
        ),
        CountryInfo(
            "SH",
            "SHN",
            "654",
            "Saint Helena, Ascension and Tristan da Cunha",
            "Saint Helena, Ascension and Tristan da Cunha",
        ),
        CountryInfo(
            "NF",
            "NFK",
            "574",
            "Norfolk Island",
            "Territory of Norfolk Island",
        ),
        CountryInfo(
            "OM",
            "OMN",
            "512",
            "Oman",
            "Sultanate of Oman",
        ),
        CountryInfo(
            "SV",
            "SLV",
            "222",
            "El Salvador",
            "Republic of El Salvador",
        ),
        CountryInfo(
            "LB",
            "LBN",
            "422",
            "Lebanon",
            "Lebanese Republic",
        ),
        CountryInfo(
            "VA",
            "VAT",
            "336",
            "Vatican City",
            "Vatican City State",
        ),
        CountryInfo(
            "EC",
            "ECU",
            "218",
            "Ecuador",
            "Republic of Ecuador",
        ),
        CountryInfo(
            "GU",
            "GUM",
            "316",
            "Guam",
            "Guam",
        ),
        CountryInfo(
            "HR",
            "HRV",
            "191",
            "Croatia",
            "Republic of Croatia",
        ),
        CountryInfo(
            "SB",
            "SLB",
            "090",
            "Solomon Islands",
            "Solomon Islands",
        ),
        CountryInfo(
            "HN",
            "HND",
            "340",
            "Honduras",
            "Republic of Honduras",
        ),
        CountryInfo(
            "CX",
            "CXR",
            "162",
            "Christmas Island",
            "Territory of Christmas Island",
        ),
        CountryInfo(
            "PR",
            "PRI",
            "630",
            "Puerto Rico",
            "Commonwealth of Puerto Rico",
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
    def _validate(cls, __input_value: str, _: core_schema.ValidationInfo) -> "CountryAlpha2":
        if __input_value not in _index_by_alpha2():
            raise PydanticCustomError("country_alpha2", "Invalid country alpha2 code")
        return cls(__input_value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: Type[T], handler: GetCoreSchemaHandler
    ) -> core_schema.AfterValidatorFunctionSchema:
        return core_schema.general_after_validator_function(
            cls._validate,
            core_schema.str_schema(to_upper=True),
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
    def _validate(cls, __input_value: str, _: core_schema.ValidationInfo) -> "CountryAlpha3":
        if __input_value not in _index_by_alpha3():
            raise PydanticCustomError("country_alpha3", "Invalid country alpha3 code")
        return cls(__input_value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: Type[T], handler: GetCoreSchemaHandler
    ) -> core_schema.AfterValidatorFunctionSchema:
        return core_schema.general_after_validator_function(
            cls._validate,
            core_schema.str_schema(to_upper=True),
            serialization=core_schema.to_string_ser_schema(),
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
    def _validate(cls, __input_value: str, _: core_schema.ValidationInfo) -> "CountryNumericCode":
        if __input_value not in _index_by_numeric_code():
            raise PydanticCustomError("country_numeric_code", "Invalid country numeric code")
        return cls(__input_value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: Type[T], handler: GetCoreSchemaHandler
    ) -> core_schema.AfterValidatorFunctionSchema:
        return core_schema.general_after_validator_function(
            cls._validate,
            core_schema.str_schema(to_upper=True),
            serialization=core_schema.to_string_ser_schema(),
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
    def _validate(cls, __input_value: str, _: core_schema.ValidationInfo) -> "CountryShortName":
        if __input_value not in _index_by_short_name():
            raise PydanticCustomError("country_short_name", "Invalid country short name")
        return cls(__input_value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: Type[T], handler: GetCoreSchemaHandler
    ) -> core_schema.AfterValidatorFunctionSchema:
        return core_schema.general_after_validator_function(
            cls._validate,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
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
    def _validate(cls, __input_value: str, _: core_schema.ValidationInfo) -> "CountryOfficialName":
        if __input_value not in _index_by_official_name():
            raise PydanticCustomError("country_numeric_code", "Invalid country official name")
        return cls(__input_value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: Type[T], handler: GetCoreSchemaHandler
    ) -> core_schema.AfterValidatorFunctionSchema:
        return core_schema.general_after_validator_function(
            cls._validate,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
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
