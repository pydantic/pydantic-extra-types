# Pandas Types

Pydantic types for [pandas](https://pandas.pydata.org/) objects. Supports `Series`, `Index`, and `DataFrame` with optional generic type validation.

## Installation

```bash
pip install "pydantic-extra-types[pandas]"
```

## Series

A validated `pandas.Series`. Use `Series[T]` to validate that every element is of type `T`.

```python
from pydantic import BaseModel
from pydantic_extra_types.pandas_types import Series

class MyModel(BaseModel):
    values: Series[int]

model = MyModel(values=[1, 2, 3])
print(model.values.tolist())  # [1, 2, 3]

# Also accepts an existing pd.Series
import pandas as pd
model = MyModel(values=pd.Series([4, 5, 6]))
print(model.values.tolist())  # [4, 5, 6]
```

Use bare `Series` (no type parameter) to accept elements of any type:

```python
class AnyModel(BaseModel):
    values: Series

model = AnyModel(values=[1, 'two', None])
```

## Index

A validated `pandas.Index`. Use `Index[T]` to validate element types.

```python
from pydantic import BaseModel
from pydantic_extra_types.pandas_types import Index

class MyModel(BaseModel):
    idx: Index[str]

model = MyModel(idx=['a', 'b', 'c'])
print(model.idx.tolist())  # ['a', 'b', 'c']
```

## DataFrame

A validated `pandas.DataFrame`. Pass a `TypedDict` (or any class with `__annotations__`) as the type parameter to validate column names and element types.

```python
from typing import TypedDict
from pydantic import BaseModel
from pydantic_extra_types.pandas_types import DataFrame

class PeopleSchema(TypedDict):
    name: str
    age: int

class MyModel(BaseModel):
    people: DataFrame[PeopleSchema]

model = MyModel(people={'name': ['Alice', 'Bob'], 'age': [30, 25]})
print(model.people)
#    name  age
# 0  Alice   30
# 1    Bob   25
```

Extra columns beyond those defined in the schema are preserved without validation:

```python
import pandas as pd

df = pd.DataFrame({'name': ['Alice'], 'age': [30], 'extra': ['kept']})
model = MyModel(people=df)
print('extra' in model.people.columns)  # True
```

Use bare `DataFrame` (no type parameter) to accept any dict or `pd.DataFrame`:

```python
class AnyModel(BaseModel):
    df: DataFrame

model = AnyModel(df={'x': [1, 2], 'y': [3, 4]})
```
