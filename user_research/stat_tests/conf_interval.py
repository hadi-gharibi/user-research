from ..utils import AlgorithmRegister
from ..types import StatisticalTestType
from . import export_to_all
import pandas as pd
from statsmodels.stats.proportion import proportion_confint
from typing import Tuple, Union
import statsmodels.stats.api as sms
import numpy as np
from scipy import stats
import math
from ..types.basics import AnalysisType


@AlgorithmRegister(
    is_discrete=True,
    analysis_type=AnalysisType.PRECISION_ESTIMATE,
    is_against_benchmark=False,
)
@export_to_all
class CompletionRate:
    @property
    def method_name(self):
        return "Adjusted-Wald Binomial Confidence Interval"

    def fit(
        self,
        data: pd.DataFrame,
        confident: float,
        col: str,
        sucess: Union[int, str] = 1,
    ) -> Tuple[float, float]:
        """Adjusted-Wald Binomial Confidence Interval for binary data.

        Args:
            data (pd.DataFrame): data
            col (str): name of the columns to analyis
            sucess Union[int, str]: What is the value inside the column that equal to sucess.
             Defaults to 1.

        Returns:
            Tuple[float, float]: [description]
        """
        count = len(data[data[col] == sucess])
        nobs = len(data)
        ci_low, ci_upp = proportion_confint(
            count=count,
            nobs=nobs,
            alpha=1 - confident,
            method="wilson",
        )
        return ci_low, ci_upp


@AlgorithmRegister(
    is_discrete=False,
    analysis_type=AnalysisType.PRECISION_ESTIMATE,
    is_against_benchmark=False,
    is_task_time=False,
)
@export_to_all
class TTest:
    @property
    def method_name(self):
        return "Student's t-distribution"

    def fit(self, data: pd.DataFrame, col: str, confident: float):
        ci_low, ci_upp = sms.DescrStatsW(data[col]).tconfint_mean(alpha=1 - confident)
        return ci_low, ci_upp


@AlgorithmRegister(
    is_discrete=False,
    analysis_type=AnalysisType.PRECISION_ESTIMATE,
    is_against_benchmark=False,
    is_task_time=True,
)
@export_to_all
class TaskTimeTest:
    def __init__(self):
        self._method_name = "Need data to decide"

    @property
    def method_name(self):
        return self._method_name

    @method_name.setter
    def method_name(self, value):
        self._method_name = value

    def _median(self, data: pd.DataFrame, col: str, confident: float):
        self.method_name = "Median"
        alpha = (1 - confident) / 2
        n = len(data)
        p = 0.5
        z_crit = stats.norm.ppf(1 - alpha)
        ci_low_ind = math.ceil(n * p - z_crit * np.sqrt(n * p * (1 - p))) - 1
        ci_upp_ind = math.ceil(n * p + z_crit * np.sqrt(n * p * (1 - p))) - 1

        data_sorted = data[col].sort_values(ascending=True)
        ci_low = data_sorted.iloc[ci_low_ind]
        ci_upp = data_sorted.iloc[ci_upp_ind]
        return ci_low, ci_upp

    def _geometric_mean(self, data: pd.DataFrame, col: str, confident: float):
        self.method_name = "Geometric Mean"
        log_data = np.log(data[col]).copy()
        # ttest =
        ci_low, ci_upp = sms.DescrStatsW(log_data).tconfint_mean(alpha=1 - confident)
        return np.exp(ci_low), np.exp(ci_upp)

    def fit(self, data: pd.DataFrame, col: str, confident: float):
        if len(data) < 25:
            return self._geometric_mean(data, col, confident)
        else:
            return self._median(data, col, confident)
