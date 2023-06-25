
The `Series` class provides support for working with pandas Series objects.

```py
import pandas as pd
from pydantic import BaseModel

from pydantic_extra_types.pandas_types import Series


class MyData(BaseModel):
    numbers: Series


data = {"numbers": pd.Series([1, 2, 3, 4, 5])}
my_data = MyData(**data)

print(my_data.numbers)
# > 0    1
# > 1    2
# > 2    3
# > 3    4
# > 4    5
# > dtype: int64
```
