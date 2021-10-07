from functools import wraps
from .basics import OneOf, Boolean, OptionalBoolean
from varname import argname


class AlgorithmProperties:
    is_discrete = Boolean()
    analysis_type = OneOf("compare", "precision-estimate")
    is_against_benchmark = OptionalBoolean()
    is_task_time = OptionalBoolean()
    groups = OneOf("same-group", "diffrent-groups", None)
    number_of_groups = OneOf("two", "three-or-more", None)

    def __init__(
        self,
        *,
        is_discrete: Boolean,
        analysis_type: OneOf,
        is_against_benchmark: OptionalBoolean = None,
        is_task_time: OptionalBoolean = None,
        groups: OneOf = None,
        number_of_groups: OneOf = None,
    ):
        """[summary]

        Args:
            is_discrete (Boolean): dis vs cont
            analysis_type (OneOf): ['compare', 'precision-estimate']
            is_against_benchmark (OptionalBoolean): against benchmark of comparing two or more gps
            is_task_time (OptionalBoolean): task or not task
            groups (OneOf): ['same-group', 'diffrent-groups', None]
            number_of_groups (OneOf): ['two', 'three-or-more', None]
        """

        self.is_discrete = is_discrete
        self.analysis_type = analysis_type
        self.is_against_benchmark = is_against_benchmark
        self.is_task_time = is_task_time
        self.groups = groups
        self.number_of_groups = number_of_groups
        self.validation()

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

    def validation(
        self,
    ):
        if self.analysis_type == "precision-estimate":
            self.mutually_exclusive(self.analysis_type, self.groups)
            self.mutually_exclusive(self.number_of_groups)
        if self.analysis_type == "compare":
            self.mutually_exclusive(self.analysis_type, self.is_against_benchmark)
            self.mutually_exclusive(self.analysis_type, self.is_task_time)
        if self.groups == "same-group":
            assert self.analysis_type == "compare"
        if self.is_discrete:
            self.mutually_exclusive(self.is_task_time, self.is_discrete)

    def __hash__(self):
        return hash(repr(self))

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args):
            value = func(*args)
            return value

        return self, wrapper

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"({', '.join([f'{k[1:]}={v!r}' for k, v in self.__dict__.items()])})"
        )

    def __eq__(self, other):
        return hash(repr(self)) == hash(repr(other))
