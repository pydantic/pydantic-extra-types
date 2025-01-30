"""
Validation for MongoDB ObjectId fields.

Ref: https://github.com/pydantic/pydantic-extra-types/issues/133
"""

from typing import Any

from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema

try:
    from bson import ObjectId
except ModuleNotFoundError as e:  # pragma: no cover
    raise RuntimeError(
        'The `mongo_object_id` module requires "pymongo" to be installed. You can install it with "pip install '
        'pymongo".'
    ) from e


class MongoObjectId(str):
    """MongoObjectId parses and validates MongoDB bson.ObjectId.

    ```py
    from pydantic import BaseModel

    from pydantic_extra_types.mongo_object_id import MongoObjectId


    class MongoDocument(BaseModel):
        id: MongoObjectId


    doc = MongoDocument(id='5f9f2f4b9d3c5a7b4c7e6c1d')
    print(doc)
    # > id='5f9f2f4b9d3c5a7b4c7e6c1d'
    ```

    Raises:
        PydanticCustomError: If the provided value is not a valid MongoDB ObjectId.
    """

    OBJECT_ID_LENGTH = 24

    @classmethod
    def __get_pydantic_core_schema__(cls, _: Any, __: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(min_length=cls.OBJECT_ID_LENGTH, max_length=cls.OBJECT_ID_LENGTH),
            python_schema=core_schema.union_schema(
                [
                    core_schema.is_instance_schema(ObjectId),
                    core_schema.chain_schema(
                        [
                            core_schema.str_schema(min_length=cls.OBJECT_ID_LENGTH, max_length=cls.OBJECT_ID_LENGTH),
                            core_schema.no_info_plain_validator_function(cls.validate),
                        ]
                    ),
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(lambda x: str(x)),
        )

    @classmethod
    def validate(cls, value: str) -> ObjectId:
        """Validate the MongoObjectId str is a valid ObjectId instance."""
        if not ObjectId.is_valid(value):
            raise ValueError(
                f"Invalid ObjectId {value} has to be 24 characters long and in the format '5f9f2f4b9d3c5a7b4c7e6c1d'."
            )

        return ObjectId(value)
