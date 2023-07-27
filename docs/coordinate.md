
Coordinate parses Latitude and Longitude.

You can use the `Coordinate` data type for storing coordinates. Coordinates can be defined using one of the following formats:

1. Tuple format: `(Latitude, Longitude)`. For example: `(41.40338, 2.17403)`.
2. `Coordinate` instance format: `Coordinate(latitude=Latitude, longitude=Longitude)`. For example: `Coordinate(latitude=41.40338, longitude=2.17403)`.

The `Latitude` class and `Longitude` class, which are used to represent latitude and longitude, respectively, enforce the following valid ranges for their values:

- `Latitude`: The latitude value should be between -90 and 90, inclusive.
- `Longitude`: The longitude value should be between -180 and 180, inclusive.

```py
from pydantic import BaseModel

from pydantic_extra_types.coordinate import Longitude, Latitude, Coordinate


class Lat(BaseModel):
    lat: Latitude


class Lng(BaseModel):
    lng: Longitude


class Coord(BaseModel):
    coord: Coordinate


lat = Lat(
    lat='90.0',
)

lng = Lng(
    long='180.0'
)

coord = Coord(
    coord=('90.0', '180.0')
)
print(lat.lat)
# > 90.0
print(lng.lng)
# > 180.0
print(coord.coord)
# > 90.0,180.0
```
