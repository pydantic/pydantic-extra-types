
`Coordinate` parses `Latitude` and `Longitude`

You can use the type `Coordinate` data type for storing coordinates.
Coordinate can be defined by this format `<Latitude>,<Longitude>`: `41.40338, 2.17403`.
The first number in your latitude coordinate is between -90 and 90.
The first number in your longitude coordinate is between -180 and 180.

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
