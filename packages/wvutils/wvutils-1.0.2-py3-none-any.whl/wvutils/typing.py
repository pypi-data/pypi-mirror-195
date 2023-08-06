"""Custom type aliases and type variables.

This module contains custom type aliases and type variables used throughout the package.
"""

import collections
import io
from collections.abc import Hashable
from os import PathLike
from typing import Literal, TypeAlias  # TypeVar

__all__ = [
    "AWSRegion",
    "FileObject",
    "FilePath",
    "JSONEncodable",
    "MD5Hashable",
    "Mask",
    "Masks",
    "PickleSerializable",
    "Span",
    "Spans",
]

# Path-like object (likely str or pathlib.Path)
FilePath: TypeAlias = str | PathLike

# File Object
FileObject: TypeAlias = io.TextIOBase | io.BytesIO

# Spans and Masks
Span: TypeAlias = list[int] | tuple[int, int]
Spans: TypeAlias = list[Span] | collections.deque[Span]
Mask: TypeAlias = str
Masks: TypeAlias = list[Mask] | collections.deque[Mask]

# Serialization
JSONEncodable: TypeAlias = str | int | float | bool | list | dict
PickleSerializable: TypeAlias = object
MD5Hashable: TypeAlias = JSONEncodable | tuple | set | Hashable

# AWS
AWSRegion: TypeAlias = Literal[
    "us-east-2",
    "us-east-1",
    "us-west-1",
    "us-west-2",
    "af-south-1",
    "ap-east-1",
    "ap-south-1",
    "ap-northeast-3",
    "ap-northeast-2",
    "ap-southeast-1",
    "ap-southeast-2",
    "ap-northeast-1",
    "ca-central-1",
    "eu-central-1",
    "eu-west-1",
    "eu-west-2",
    "eu-south-1",
    "eu-west-3",
    "eu-north-1",
    "me-south-1",
    "sa-east-1",
    "us-gov-east-1",
    "us-gov-west-1",
]
