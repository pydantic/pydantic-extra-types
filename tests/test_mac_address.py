from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

from pydantic_extra_types.mac_address import MacAddress


class Network(BaseModel):
    mac_address: MacAddress


@pytest.mark.parametrize(
    'mac_address, result, valid',
    [
        # Valid MAC addresses
        ('00:00:5e:00:53:01', '00:00:5e:00:53:01', True),
        ('02:00:5e:10:00:00:00:01', '02:00:5e:10:00:00:00:01', True),
        (
            '00:00:00:00:fe:80:00:00:00:00:00:00:02:00:5e:10:00:00:00:01',
            '00:00:00:00:fe:80:00:00:00:00:00:00:02:00:5e:10:00:00:00:01',
            True,
        ),
        ('00-00-5e-00-53-01', '00:00:5e:00:53:01', True),
        ('02-00-5e-10-00-00-00-01', '02:00:5e:10:00:00:00:01', True),
        (
            '00-00-00-00-fe-80-00-00-00-00-00-00-02-00-5e-10-00-00-00-01',
            '00:00:00:00:fe:80:00:00:00:00:00:00:02:00:5e:10:00:00:00:01',
            True,
        ),
        ('0000.5e00.5301', '00:00:5e:00:53:01', True),
        ('0200.5e10.0000.0001', '02:00:5e:10:00:00:00:01', True),
        (
            '0000.0000.fe80.0000.0000.0000.0200.5e10.0000.0001',
            '00:00:00:00:fe:80:00:00:00:00:00:00:02:00:5e:10:00:00:00:01',
            True,
        ),
        # Invalid MAC addresses
        ('0200.5e10.0000.001', None, False),
        ('00-00-5e-00-53-0', None, False),
        ('00:00:5e:00:53:1', None, False),
        ('02:00:5e:10:00:00:00:1', None, False),
        ('00:00:00:00:fe:80:00:00:00:00:00:00:02:00:5e:10:00:00:00:1', None, False),
        ('0200.5e10.0000.001', None, False),  # Invalid length
        ('00-00-5e-00-53-0', None, False),  # Missing character
        ('00:00:5e:00:53:1', None, False),  # Missing leading zero
        ('00:00:5g:00:53:01', None, False),  # Invalid hex digit 'g'
        ('00.00.5e.0.3.01.0.0.5e.0.53.01', None, False),
        ('00-00-5e-00-53-01:', None, False),  # Extra separator at the end
        ('00000.5e000.5301', None, False),
        ('000.5e0.530001', None, False),
        ('0000.5e#0./301', None, False),
        (b'12.!4.5!.7/.#G.AB......', None, False),
        ('12.!4.5!.7/.#G.AB', None, False),
        ('00-00-5e-00-53-01-', None, False),  # Extra separator at the end
        ('00.00.5e.00.53.01.', None, False),  # Extra separator at the end
        ('00:00:5e:00:53:', None, False),  # Incomplete MAC address
        (float(12345678910111213), None, False),
    ],
)
def test_format_for_mac_address(mac_address: Any, result: str, valid: bool):
    if valid:
        assert Network(mac_address=MacAddress(mac_address)).mac_address == result
    else:
        with pytest.raises(ValidationError, match='format'):
            Network(mac_address=MacAddress(mac_address))


@pytest.mark.parametrize(
    'mac_address, result, valid',
    [
        # Valid MAC addresses
        ('00:00:5e:00:53:01', '00:00:5e:00:53:01', True),
        ('02:00:5e:10:00:00:00:01', '02:00:5e:10:00:00:00:01', True),
        (
            '00:00:00:00:fe:80:00:00:00:00:00:00:02:00:5e:10:00:00:00:01',
            '00:00:00:00:fe:80:00:00:00:00:00:00:02:00:5e:10:00:00:00:01',
            True,
        ),
        ('00-00-5e-00-53-01', '00:00:5e:00:53:01', True),
        ('02-00-5e-10-00-00-00-01', '02:00:5e:10:00:00:00:01', True),
        (
            '00-00-00-00-fe-80-00-00-00-00-00-00-02-00-5e-10-00-00-00-01',
            '00:00:00:00:fe:80:00:00:00:00:00:00:02:00:5e:10:00:00:00:01',
            True,
        ),
        ('0000.5e00.5301', '00:00:5e:00:53:01', True),
        ('0200.5e10.0000.0001', '02:00:5e:10:00:00:00:01', True),
        (
            '0000.0000.fe80.0000.0000.0000.0200.5e10.0000.0001',
            '00:00:00:00:fe:80:00:00:00:00:00:00:02:00:5e:10:00:00:00:01',
            True,
        ),
        # Invalid MAC addresses
        ('0', None, False),
        ('00:00:00', None, False),
        ('00-00-5e-00-53-01-01', None, False),
        ('0000.0000.fe80.0000.0000.0000.0200.5e10.0000.0001.0000.0001', None, False),
    ],
)
def test_length_for_mac_address(mac_address: str, result: str, valid: bool):
    if valid:
        assert Network(mac_address=MacAddress(mac_address)).mac_address == result
    else:
        with pytest.raises(ValueError, match='Length'):
            Network(mac_address=MacAddress(mac_address))


@pytest.mark.parametrize(
    'mac_address, valid',
    [
        # Valid MAC addresses
        ('00:00:5e:00:53:01', True),
        (MacAddress('00:00:5e:00:53:01'), True),
        # Invalid MAC addresses
        (0, False),
        (['00:00:00'], False),
    ],
)
def test_type_for_mac_address(mac_address: Any, valid: bool):
    if valid:
        Network(mac_address=MacAddress(mac_address))
    else:
        with pytest.raises(ValidationError, match='MAC address must be 14'):
            Network(mac_address=MacAddress(mac_address))


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
            'msg': 'Length for a 1234 MAC address must be 14',
            'type': 'mac_address_len',
        }
    ]
