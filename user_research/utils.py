from functools import wraps
from typing import Dict, Callable, Set
from .types.algorithms import StatisticalTestType
from copy import deepcopy


class AlgorithmRegister(object):
    """Singltone class to register functions based on their AlgProperties"""

    _instance = None
    _plugins: Dict[StatisticalTestType, Set[Callable]] = {}
    _buffer = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)

        if kwargs:
            cls._buffer = StatisticalTestType(*args, **kwargs)

        return cls._instance

    def __call__(self, func):
        # obj = deepcopy(self.__class__._buffer)
        obj = self.__class__._buffer
        if obj:
            if self._plugins.get(obj, None) is None:

                self._plugins[obj] = {func}
            else:
                self._plugins[obj].add(func)
        self.__class__._buffer = None

        @wraps(func)
        def wrapper(*args):
            value = func(*args)
            return value

        return wrapper
        # return self._plugins[obj]

    def __getitem__(self, key):
        return self._plugins[key]
