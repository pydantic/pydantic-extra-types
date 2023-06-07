
The `PhoneNumber` type validates phone numbers.

This class depends on the [phonenumbers] package, which is a Python port of Google's [libphonenumber].

```py
from pydantic import BaseModel

from pydantic_extra_types.phone_numbers import PhoneNumber


class User(BaseModel):
    name: str
    phone_number: PhoneNumber


user = User(name='John', phone_number='+447911123456')
print(user.phone_number)  # (1)!
#> tel:+44-7911-123456
```

1. The phone format used is described on the [RFC3966].


[phonenumbers]: https://pypi.org/project/phonenumbers/
[libphonenumber]: https://github.com/google/libphonenumber/
[RFC3966]: https://tools.ietf.org/html/rfc3966
