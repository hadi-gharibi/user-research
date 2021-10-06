from abc import ABC, abstractmethod


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
