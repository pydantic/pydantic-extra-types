
The `ABARoutingNumber` type validates [ABA routing transit numbers].


```py
from pydantic import BaseModel

from pydantic_extra_types.routing_number import ABARoutingNumber


class BankAccount(BaseModel):
    name: str
    routing_number: ABARoutingNumber
    account_number: str


account = BankAccount(
    name="John",
    routing_number="122105155",
    account_number="123456789",
)

print(account.routing_number)
# > 122105155
```

The algorithm used to validate the routing number is described on this [section of the Wikipedia page].


[ABA routing transit numbers]: https://en.wikipedia.org/wiki/ABA_routing_transit_number
[section of the Wikipedia page]: https://en.wikipedia.org/wiki/ABA_routing_transit_number#Check_digit
