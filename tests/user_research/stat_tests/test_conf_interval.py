from user_research.stat_tests.conf_interval import CompletionRate, TTest, TaskTimeTest
import pytest
import pandas as pd


@pytest.fixture(scope="session")
def data_CompletionRate():
    """7 out of 10 users completing a task"""
    return pd.DataFrame([1, 1, 1, 1, 1, 1, 1, 0, 0, 0]), (0.645 - 0.25, 0.645 + 0.25)


@pytest.fixture(scope="session")
def data_TTest():
    """
    Fifteen users were asked to find information about a Mutual Fund on a
    Financial Services company website.
    After attempting the task, users answered a single 7-point Likert
    question about how difficult the task was. A
    rating of 1 corresponds to the response “Very Difficult” and a 7 “Very Easy”."""
    return pd.DataFrame([3, 5, 3, 7, 1, 6, 2, 5, 1, 1, 3, 2, 6, 2, 2]), (
        3.27 - 1.1,
        3.27 + 1.1,
    )


@pytest.fixture(scope="session")
def data_TaskTimeTest_geometric():
    data = pd.DataFrame([94, 95, 96, 113, 121, 132, 190, 193, 255, 298])
    return data, (108, 198)


@pytest.fixture(scope="session")
def data_TaskTimeTest_median():
    """Time needs to compelete a task"""
    data = pd.DataFrame(
        [
            167,
            158,
            136,
            124,
            77,
            317,
            85,
            65,
            120,
            136,
            80,
            186,
            110,
            95,
            109,
            330,
            96,
            116,
            76,
            100,
            248,
            57,
            122,
            96,
            173,
            115,
            137,
            76,
            152,
            149,
        ]
    )
    return data, (96, 137)


def test_ComplitionRate(data_CompletionRate):
    input, actual = data_CompletionRate
    method = CompletionRate()
    preds = method.fit(data=input, confident=0.95, col=0)
    assert actual == pytest.approx(preds, abs=1e-2)


def test_TTest(data_TTest):
    input, actual = data_TTest
    method = TTest()
    preds = method.fit(data=input, confident=0.95, col=0)
    assert actual == pytest.approx(preds, abs=1e-1)


def test_TaskTimeTest_geometric(data_TaskTimeTest_geometric):
    input, actual = data_TaskTimeTest_geometric
    method = TaskTimeTest()
    preds = method._geometric_mean(data=input, confident=0.95, col=0)
    assert actual == pytest.approx(preds, abs=1)


def test_TaskTimeTest_median(data_TaskTimeTest_median):
    input, actual = data_TaskTimeTest_median
    method = TaskTimeTest()
    preds = method._median(data=input, confident=0.95, col=0)
    assert actual == pytest.approx(preds, abs=1)
