from abc import ABC, abstractmethod
from functools import wraps
from varname import argname


class Validator(ABC):
    def __set_name__(self, owner, name):
        self.private_name = "_" + name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.private_name, value)

    @abstractmethod
    def validate(self, value):
        pass


class OneOf(Validator):
    def __init__(self, *options):
        self.options = set(options)

    def validate(self, value):
        if value not in self.options:
            raise ValueError(f"Expected {value!r} to be one of {self.options!r}")


class Boolean(Validator):
    def validate(self, value):
        if type(value) != bool:
            raise ValueError(f"Expected {value!r} to be True or False")


class OptionalBoolean(Validator):
    def validate(self, value):
        if (type(value) != bool) and (value is not None):
            raise ValueError(f"Expected {value!r} to be True or False")


class Base:
    def __hash__(self):
        return hash(repr(self))

    def __call__(self, funcs):
        @wraps(funcs)
        def wrapper(*args):
            value = funcs(*args)
            return value

        return self, wrapper

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"""({', '.join([f'{k}={v!r}' if not k.startswith('_')
            else f'{k[1:]}={v!r}' for k, v in self.__dict__.items()])})"""
        )

    def __eq__(self, other):
        return hash(repr(self)) == hash(repr(other))

    @staticmethod
    def mutually_exclusive(x, y):
        x_name, y_name = argname("x", "y")
        is_x = 1 if x else 0
        is_y = 1 if y else 0
        if sum([is_x, is_y]) != 1:
            raise ValueError(
                f"You can only have '{x_name}' = {x!r} or '{y_name}' = {y!r}. "
                f"They are mutually exclusive."
            )
