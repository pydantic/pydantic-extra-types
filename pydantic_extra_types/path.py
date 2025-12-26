from __future__ import annotations

import typing
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import pydantic
from pydantic.types import PathType
from pydantic_core import core_schema

ExistingPath = typing.Union[pydantic.FilePath, pydantic.DirectoryPath]


@dataclass
class ResolvedPathType(PathType):
    """A custom PathType that resolves the path to its absolute form.

    Args:
        path_type (typing.Literal['file', 'dir', 'new']): The type of path to resolve. Can be 'file', 'dir' or 'new'.

    Returns:
        Resolved path as a pathlib.Path object.

    Example:
        ```python
        from pydantic import BaseModel
        from pydantic_extra_types.path import ResolvedFilePath, ResolvedDirectoryPath, ResolvedNewPath


        class MyModel(BaseModel):
            file_path: ResolvedFilePath
            dir_path: ResolvedDirectoryPath
            new_path: ResolvedNewPath


        model = MyModel(file_path='~/myfile.txt', dir_path='~/mydir', new_path='~/newfile.txt')
        print(model.file_path)
        # > file_path=PosixPath('/home/user/myfile.txt') dir_path=PosixPath('/home/user/mydir') new_path=PosixPath('/home/user/newfile.txt')"""

    @staticmethod
    def validate_file(path: Path, _: core_schema.ValidationInfo) -> Path:
        return PathType.validate_file(path.expanduser().resolve(), _)

    @staticmethod
    def validate_directory(path: Path, _: core_schema.ValidationInfo) -> Path:
        return PathType.validate_directory(path.expanduser().resolve(), _)

    @staticmethod
    def validate_new(path: Path, _: core_schema.ValidationInfo) -> Path:
        return PathType.validate_new(path.expanduser().resolve(), _)

    def __hash__(self) -> int:
        return hash(type(self.path_type))


ResolvedFilePath = Annotated[Path, ResolvedPathType('file')]
ResolvedDirectoryPath = Annotated[Path, ResolvedPathType('dir')]
ResolvedNewPath = Annotated[Path, ResolvedPathType('new')]
ResolvedExistingPath = typing.Union[ResolvedFilePath, ResolvedDirectoryPath]
