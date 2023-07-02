
The `MacAddress` type validates [MAC address](https://en.wikipedia.org/wiki/MAC_address) (such as a network card).

```py
from pydantic import BaseModel

from pydantic_extra_types.mac_address import MacAddress


class Network(BaseModel):
    mac_address: MacAddress


network = Network(
    mac_address='00:00:5e:00:53:01',
)

print(network.mac_address)
# > 00:00:5e:00:53:01
```

The algorithm used to validate the MAC address `IEEE` `802` `MAC-48`, `EUI-48`, `EUI-64`, or a `20-octet`.
