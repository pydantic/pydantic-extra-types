import os
import pathlib

import pytest
from pydantic import BaseModel

from pydantic_extra_types.path import (
    ExistingPath,
    ResolvedDirectoryPath,
    ResolvedExistingPath,
    ResolvedFilePath,
    ResolvedNewPath,
)


class File(BaseModel):
    file: ResolvedFilePath


class Directory(BaseModel):
    directory: ResolvedDirectoryPath


class NewPath(BaseModel):
    new_path: ResolvedNewPath


class Existing(BaseModel):
    existing: ExistingPath


class ResolvedExisting(BaseModel):
    resolved_existing: ResolvedExistingPath


@pytest.fixture
def absolute_file_path(tmp_path: pathlib.Path) -> pathlib.Path:
    directory = tmp_path / 'test-relative'
    directory.mkdir()
    file_path = directory / 'test-relative.txt'
    file_path.touch()
    return file_path


@pytest.fixture
def relative_file_path(absolute_file_path: pathlib.Path) -> pathlib.Path:
    cwd = pathlib.Path.cwd()
    if os.name == 'nt' and absolute_file_path.anchor != cwd.anchor:
        # on windows, cant create relative path when paths are on different drives
        return absolute_file_path
    return pathlib.Path(os.path.relpath(absolute_file_path, os.getcwd()))


@pytest.fixture
def absolute_directory_path(tmp_path: pathlib.Path) -> pathlib.Path:
    directory = tmp_path / 'test-relative'
    directory.mkdir()
    return directory


@pytest.fixture
def relative_directory_path(absolute_directory_path: pathlib.Path) -> pathlib.Path:
    cwd = pathlib.Path.cwd()
    if os.name == 'nt' and absolute_directory_path.anchor != cwd.anchor:
        # on windows, cant create relative path when paths are on different drives
        return absolute_directory_path
    return pathlib.Path(os.path.relpath(absolute_directory_path, os.getcwd()))


@pytest.fixture
def absolute_new_path(tmp_path: pathlib.Path) -> pathlib.Path:
    return tmp_path / 'test-relative'


@pytest.fixture
def relative_new_path(absolute_new_path: pathlib.Path) -> pathlib.Path:
    cwd = pathlib.Path.cwd()
    if os.name == 'nt' and absolute_new_path.anchor != cwd.anchor:
        # on windows, cant create relative path when paths are on different drives
        return absolute_new_path
    return pathlib.Path(os.path.relpath(absolute_new_path, os.getcwd()))


def test_relative_file(absolute_file_path: pathlib.Path, relative_file_path: pathlib.Path):
    file = File(file=relative_file_path)
    assert file.file == absolute_file_path


def test_absolute_file(absolute_file_path: pathlib.Path):
    file = File(file=absolute_file_path)
    assert file.file == absolute_file_path


def test_relative_directory(absolute_directory_path: pathlib.Path, relative_directory_path: pathlib.Path):
    directory = Directory(directory=relative_directory_path)
    assert directory.directory == absolute_directory_path


def test_absolute_directory(absolute_directory_path: pathlib.Path):
    directory = Directory(directory=absolute_directory_path)
    assert directory.directory == absolute_directory_path


def test_relative_new_path(absolute_new_path: pathlib.Path, relative_new_path: pathlib.Path):
    new_path = NewPath(new_path=relative_new_path)
    assert new_path.new_path == absolute_new_path


def test_absolute_new_path(absolute_new_path: pathlib.Path):
    new_path = NewPath(new_path=absolute_new_path)
    assert new_path.new_path == absolute_new_path


@pytest.mark.parametrize(
    ('pass_fixture', 'expect_fixture'),
    (
        ('relative_file_path', 'relative_file_path'),
        ('absolute_file_path', 'absolute_file_path'),
        ('relative_directory_path', 'relative_directory_path'),
        ('absolute_directory_path', 'absolute_directory_path'),
    ),
)
def test_existing_path(request: pytest.FixtureRequest, pass_fixture: str, expect_fixture: str):
    existing = Existing(existing=request.getfixturevalue(pass_fixture))
    assert existing.existing == request.getfixturevalue(expect_fixture)


@pytest.mark.parametrize(
    ('pass_fixture', 'expect_fixture'),
    (
        ('relative_file_path', 'absolute_file_path'),
        ('absolute_file_path', 'absolute_file_path'),
        ('relative_directory_path', 'absolute_directory_path'),
        ('absolute_directory_path', 'absolute_directory_path'),
    ),
)
def test_resolved_existing_path(request: pytest.FixtureRequest, pass_fixture: str, expect_fixture: str):
    resolved_existing = ResolvedExisting(resolved_existing=request.getfixturevalue(pass_fixture))
    assert resolved_existing.resolved_existing == request.getfixturevalue(expect_fixture)
