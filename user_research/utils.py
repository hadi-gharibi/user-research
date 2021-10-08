from functools import wraps
from typing import Dict, Callable, Set
from .types.algorithms import StatisticalTestType


class AlgorithmRegister(object):
    """Singltone class to register functions based on their AlgProperties"""

    _instance = None
    _plugins: Dict[StatisticalTestType, Set[Callable]] = {}

    def __init__(self, inp=None):
        if inp:
            obj, func = inp
            if not self._plugins.get(obj, None):
                self._plugins[obj] = {func}
            else:
                self._plugins[obj].add(func)

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args):
            value = func(*args)
            return value

        return wrapper
        # return self._plugins[obj]

    def __getitem__(self, key):
        return self._plugins[key]
