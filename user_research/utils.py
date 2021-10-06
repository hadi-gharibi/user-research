from functools import wraps
from typing import Dict, Callable
from .types.algs import AlgProperties


class Register(object):
    _instance = None
    _plugins: Dict[AlgProperties, Callable] = {}

    def __init__(self, inp=None):
        if inp:
            obj, func = inp

            self._plugins[obj] = func

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

    def __getitem__(self, key):
        return self._plugins[key]
