#!/usr/bin/env python3
"""This module provides utility functions for accessing nested mappings."""

"""Utils module with access_nested_map"""

from typing import Mapping, Any, Union


def access_nested_map(nested_map: Mapping, path: Union[str, tuple]) -> Any:
    """Access a nested map with a sequence of keys."""
    for key in path:
        nested_map = nested_map[key]
    return nested_map

