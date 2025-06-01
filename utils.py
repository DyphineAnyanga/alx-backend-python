#!/usr/bin/env python3
"""
Utils module
"""

import requests # type: ignore
from typing import Dict


def get_json(url: str) -> Dict:
    """GET JSON content from a URL"""
    response = requests.get(url)
    return response.json()

def memoize(method):
    """Memoization decorator for instance methods"""
    attr_name = f"_memoized_{method.__name__}"

    @property
    def memoized(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)

    return memoized