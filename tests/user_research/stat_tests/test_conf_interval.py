from user_research.stat_tests.conf_interval import CompletionRate, TTest, TaskTimeTest
import pytest


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
