from .basics import OneOf, Boolean, OptionalBoolean, Base


class StatisticalTestFamily(Base):
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
        **kwargs
    ):
        """[summary]

        Args:
            is_discrete (Boolean): dis vs cont
            analysis_type (OneOf): ['compare', 'precision-estimate']
            is_against_benchmark (OptionalBoolean): are we comparing against a benchmark or \
                comparing against two or more groups
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

    def validation(self):
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


class StatisticalTestProperties(Base):
    def __init__(self, **kwargs):
        pass


class StatisticalTestType(Base):
    def __init__(self, **kwargs):

        self.stat_test_family = StatisticalTestFamily(**kwargs)
        self.stat_test_properties = StatisticalTestProperties(**kwargs)
