from typing import Any

import pytest
from pydantic import BaseModel, ValidationError
from pydantic_core import PydanticCustomError

from pydantic_extra_types.mac_address import MacAddress


@pytest.mark.parametrize(
    'mac_address, valid',
    [
        # Valid MAC addresses
        ('00:00:5e:00:53:01', True),
        ('02:00:5e:10:00:00:00:01', True),
        ('00:00:00:00:fe:80:00:00:00:00:00:00:02:00:5e:10:00:00:00:01', True),
        ('00-00-5e-00-53-01', True),
        ('02-00-5e-10-00-00-00-01', True),
        ('00-00-00-00-fe-80-00-00-00-00-00-00-02-00-5e-10-00-00-00-01', True),
        ('0000.5e00.5301', True),
        ('0200.5e10.0000.0001', True),
        ('0000.0000.fe80.0000.0000.0000.0200.5e10.0000.0001', True),
        # Invalid MAC addresses
        ('0200.5e10.0000.001', False),
        ('00-00-5e-00-53-0', False),
        ('00:00:5e:00:53:1', False),
        ('02:00:5e:10:00:00:00:1', False),
        ('00:00:00:00:fe:80:00:00:00:00:00:00:02:00:5e:10:00:00:00:1', False),
        ('0200.5e10.0000.001', False),  # Invalid length
        ('00-00-5e-00-53-0', False),  # Missing character
        ('00:00:5e:00:53:1', False),  # Missing leading zero
        ('00:00:5g:00:53:01', False),  # Invalid hex digit 'g'
        ('00-00-5e-00-53-01:', False),  # Extra separator at the end
        ('00-00-5e-00-53-01-', False),  # Extra separator at the end
        ('00.00.5e.00.53.01.', False),  # Extra separator at the end
        ('00:00:5e:00:53:', False),  # Incomplete MAC address
    ],
)
def test_format_for_mac_address(mac_address: str, valid: bool):
    if valid:
        assert MacAddress(mac_address) == mac_address
    else:
        with pytest.raises(PydanticCustomError, match='format'):
            MacAddress(mac_address)


@pytest.mark.parametrize(
    'mac_address, valid',
    [
        # Valid MAC addresses
        ('00:00:5e:00:53:01', True),
        ('02:00:5e:10:00:00:00:01', True),
        ('00:00:00:00:fe:80:00:00:00:00:00:00:02:00:5e:10:00:00:00:01', True),
        ('00-00-5e-00-53-01', True),
        ('02-00-5e-10-00-00-00-01', True),
        ('00-00-00-00-fe-80-00-00-00-00-00-00-02-00-5e-10-00-00-00-01', True),
        ('0000.5e00.5301', True),
        ('0200.5e10.0000.0001', True),
        ('0000.0000.fe80.0000.0000.0000.0200.5e10.0000.0001', True),
        # Invalid MAC addresses
        ('0', False),
        ('00:00:00', False),
        ('00-00-5e-00-53-01-01', False),
        ('0000.0000.fe80.0000.0000.0000.0200.5e10.0000.0001.0000.0001', False),
    ],
)
def test_length_for_mac_address(mac_address: str, valid: bool):
    if valid:
        assert MacAddress(mac_address) == mac_address
    else:
        with pytest.raises(PydanticCustomError, match='Length'):
            MacAddress(mac_address)


@pytest.mark.parametrize(
    'mac_address, valid',
    [
        # Valid MAC addresses
        ('00:00:5e:00:53:01', True),
        (b'00:00:5e:00:53:01', True),
        (MacAddress('00:00:5e:00:53:01'), True),
        # Invalid MAC addresses
        (0, False),
        (['00:00:00'], False),
    ],
)
def test_type_for_mac_address(mac_address: Any, valid: bool):
    if valid:
        MacAddress(mac_address)
    else:
        with pytest.raises(
            PydanticCustomError, match='value is not a valid Mac Address: value must be a string or bytes'
        ):
            MacAddress(mac_address)


def test_model_validation():
    class Model(BaseModel):
        mac_address: MacAddress

    assert Model(mac_address='00:00:5e:00:53:01').mac_address == '00:00:5e:00:53:01'
    with pytest.raises(ValidationError) as exc_info:
        Model(mac_address='1234')

    assert exc_info.value.errors() == [
        {
            'ctx': {'mac_address': '1234', 'required_length': 14},
            'input': '1234',
            'loc': ('mac_address',),
            'msg': 'Length for a 1234 mac address must be 14',
            'type': 'mac_address_len',
        }
    ]
