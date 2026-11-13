"""The `pydantic_extra_types.numpy` module provides data types for
[numpy](https://numpy.org/) arrays and scalars.

This module depends on the [numpy](https://pypi.org/project/numpy/) package.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import partial
from typing import Any

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import PydanticCustomError, core_schema

try:
    import numpy as np  # type: ignore[import-untyped]
except ModuleNotFoundError as e:
    raise RuntimeError(
        '`NumpyArray` and `NumpyScalar` require "numpy" to be installed. '
        'You can install it with "pip install numpy"'
    ) from e


class NumpyArray:
    """A wrapper type that validates an object is a `numpy.ndarray`.

    You can optionally require a specific dtype and/or shape.

    ## Examples

    ### Basic usage:

    ```python
    import numpy as np
    from pydantic import BaseModel
    from pydantic_extra_types.numpy import NumpyArray


    class Model(BaseModel):
        arr: NumpyArray


    m = Model(arr=np.array([1, 2, 3]))
    print(m.arr)
    ```

    ### With dtype restriction:

    ```python
    import numpy as np
    from pydantic import BaseModel
    from pydantic_extra_types.numpy import NumpyArray


    class Model(BaseModel):
        arr: NumpyArray[dtype=np.float64]


    m = Model(arr=np.array([1.0, 2.0, 3.0], dtype=np.float64))
    print(m.arr)
    ```

    ### With shape restriction:

    ```python
    import numpy as np
    from pydantic import BaseModel
    from pydantic_extra_types.numpy import NumpyArray


    class Model(BaseModel):
        arr: NumpyArray[shape=(3, 2)]


    m = Model(arr=np.array([[1, 2], [3, 4], [5, 6]]))
    print(m.arr.shape)  # (3, 2)
    ```

    ### With dtype and shape restriction:

    ```python
    import numpy as np
    from pydantic import BaseModel
    from pydantic_extra_types.numpy import NumpyArray


    class Model(BaseModel):
        arr: NumpyArray[dtype=np.float32, shape=(2, 3)]


    m = Model(arr=np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], dtype=np.float32))
    print(m.arr.shape)  # (2, 3)
    print(m.arr.dtype)  # float32
    ```
    """

    dtype: type | str | None = None
    """Optional dtype that the array must have."""

    shape: tuple[int, ...] | None = None
    """Optional shape that the array must have. Use -1 for any size in a dimension."""

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.with_info_after_validator_function(
            cls._validate,
            core_schema.any_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> dict[str, Any]:
        json_schema = handler(schema)
        json_schema.update({"type": "array", "title": "NumpyArray"})
        return json_schema

    @classmethod
    def _validate(cls, value: Any, _: core_schema.ValidationInfo) -> "np.ndarray":
        if not isinstance(value, np.ndarray):
            raise PydanticCustomError(
                "value_error",
                "value is not a valid numpy ndarray",
            )

        if cls.dtype is not None:
            expected_dtype = np.dtype(cls.dtype)
            if value.dtype != expected_dtype:
                raise PydanticCustomError(
                    "value_error",
                    f"array dtype {value.dtype} does not match expected dtype {expected_dtype}",
                )

        if cls.shape is not None:
            if value.ndim != len(cls.shape):
                raise PydanticCustomError(
                    "value_error",
                    f"array has {value.ndim} dimensions but expected {len(cls.shape)}",
                )
            for i, (actual, expected) in enumerate(zip(value.shape, cls.shape)):
                if expected != -1 and actual != expected:
                    raise PydanticCustomError(
                        "value_error",
                        f"dimension {i} has size {actual} but expected {expected}",
                    )

        return value


class NumpyScalar:
    """A wrapper type that validates an object is a numpy scalar.

    ## Examples

    ```python
    import numpy as np
    from pydantic import BaseModel
    from pydantic_extra_types.numpy import NumpyScalar


    class Model(BaseModel):
        val: NumpyScalar


    m = Model(val=np.int64(42))
    print(m.val)  # 42
    ```

    ### With specific dtype:

    ```python
    import numpy as np
    from pydantic import BaseModel
    from pydantic_extra_types.numpy import NumpyScalar


    class Model(BaseModel):
        val: NumpyScalar[dtype=np.float64]


    m = Model(val=np.float64(3.14))
    print(m.val)  # 3.14
    ```
    """

    dtype: type | str | None = None
    """Optional dtype that the scalar must have."""

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.with_info_after_validator_function(
            cls._validate,
            core_schema.any_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> dict[str, Any]:
        json_schema = handler(schema)
        json_schema.update({"type": "number", "title": "NumpyScalar"})
        return json_schema

    @classmethod
    def _validate(cls, value: Any, _: core_schema.ValidationInfo) -> np.generic:
        if not isinstance(value, np.generic):
            raise PydanticCustomError(
                "value_error",
                "value is not a numpy scalar",
            )

        if cls.dtype is not None:
            expected_dtype = np.dtype(cls.dtype)
            if value.dtype != expected_dtype:
                raise PydanticCustomError(
                    "value_error",
                    f"scalar dtype {value.dtype} does not match expected dtype {expected_dtype}",
                )

        return value


def _validate_ndarray(
    required_dtype: np.dtype | None,
    required_shape: tuple[int, ...] | None,
    value: Any,
) -> np.ndarray:
    """Validate that *value* is a ``np.ndarray`` and (optionally) that it
    matches *required_dtype* and/or *required_shape*."""
    if not isinstance(value, np.ndarray):
        raise PydanticCustomError(
            "value_error",
            "value is not a valid numpy ndarray",
        )

    if required_dtype is not None:
        expected_dtype = np.dtype(required_dtype)
        if value.dtype != expected_dtype:
            raise PydanticCustomError(
                "value_error",
                f"array dtype {value.dtype} does not match expected dtype {expected_dtype}",
            )

    if required_shape is not None:
        if value.ndim != len(required_shape):
            raise PydanticCustomError(
                "value_error",
                f"array has {value.ndim} dimensions but expected {len(required_shape)}",
            )
        for i, (actual, expected) in enumerate(zip(value.shape, required_shape)):
            if expected != -1 and actual != expected:
                raise PydanticCustomError(
                    "value_error",
                    f"dimension {i} has size {actual} but expected {expected}",
                )

    return value


def _validate_scalar(
    required_dtype: np.dtype | None,
    value: Any,
) -> np.generic:
    """Validate that *value* is a numpy scalar."""
    if not isinstance(value, np.generic):
        raise PydanticCustomError(
            "value_error",
            "value is not a numpy scalar",
        )

    if required_dtype is not None:
        expected_dtype = np.dtype(required_dtype)
        if value.dtype != expected_dtype:
            raise PydanticCustomError(
                "value_error",
                f"scalar dtype {value.dtype} does not match expected dtype {required_dtype}",
            )

    return value


@dataclass(frozen=True)
class NumpyArrayValidator:
    """An annotation to validate `np.ndarray` objects with dtype and shape constraints.

    Example:
        ```python
        from typing import Annotated
        import numpy as np
        from pydantic import BaseModel
        from pydantic_extra_types.numpy import NumpyArrayValidator

        Matrix3x3 = Annotated[np.ndarray, NumpyArrayValidator(dtype=np.float64, shape=(3, 3))]

        class Model(BaseModel):
            matrix: Matrix3x3

        m = Model(matrix=np.eye(3, dtype=np.float64))
        print(m.matrix)
        ```
    """

    dtype: type | str | None = None
    """Optional dtype that the array must have."""

    shape: tuple[int, ...] | None = None
    """Optional shape that the array must have. Use -1 for any size in a dimension."""

    def __get_pydantic_core_schema__(self, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        required_dtype = np.dtype(self.dtype) if self.dtype is not None else None
        required_shape = self.shape
        return core_schema.with_info_after_validator_function(
            partial(_validate_ndarray, required_dtype, required_shape),
            core_schema.any_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> dict[str, Any]:
        json_schema = handler(schema)
        json_schema.update({"type": "array", "title": "NumpyArray"})
        return json_schema

    def __hash__(self) -> int:
        return super().__hash__()


def _validate_ndarray(
    required_dtype: np.dtype | None,
    required_shape: tuple[int, ...] | None,
    value: Any,
    _info: core_schema.ValidationInfo | None = None,
) -> np.ndarray:
    """Validate that *value* is a ``np.ndarray`` and (optionally) that it
    matches *required_dtype* and/or *required_shape*."""
    if not isinstance(value, np.ndarray):
        raise PydanticCustomError(
            "value_error",
            "value is not a valid numpy ndarray",
        )

    if required_dtype is not None:
        expected_dtype = np.dtype(required_dtype)
        if value.dtype != expected_dtype:
            raise PydanticCustomError(
                "value_error",
                f"array dtype {value.dtype} does not match expected dtype {expected_dtype}",
            )

    if required_shape is not None:
        if value.ndim != len(required_shape):
            raise PydanticCustomError(
                "value_error",
                f"array has {value.ndim} dimensions but expected {len(required_shape)}",
            )
        for i, (actual, expected) in enumerate(zip(value.shape, required_shape)):
            if expected != -1 and actual != expected:
                raise PydanticCustomError(
                    "value_error",
                    f"dimension {i} has size {actual} but expected {expected}",
                )

    return value