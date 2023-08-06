import logging
import os
import time

import pytest
from pytest import approx

from eotransform.utilities.profiling import PerformanceClock, PERFORMANCE_LOG_ENV_VAR, clock_performance, log


@pytest.fixture
def clock():
    return PerformanceClock()


@pytest.fixture
def set_logging_active():
    try:
        os.environ[PERFORMANCE_LOG_ENV_VAR] = "1"
        yield
    finally:
        del os.environ[PERFORMANCE_LOG_ENV_VAR]


def test_measure_scope(clock, slow_factor):
    with clock.measure():
        time.sleep(0.01 * slow_factor)

    assert clock.mean_measures == approx(0.01 * slow_factor, abs=0.009 * slow_factor)


def test_measure_multiple_scopes_and_provide_mean(clock, slow_factor):
    with clock.measure():
        time.sleep(0.01 * slow_factor)
    with clock.measure():
        time.sleep(0.03 * slow_factor)

    assert clock.mean_measures == approx(0.02 * slow_factor, abs=0.005 * slow_factor)


def test_drop_first(clock, slow_factor):
    with clock.measure():
        time.sleep(0.05 * slow_factor)

    with clock.measure():
        time.sleep(0.01 * slow_factor)

    assert clock.drop_first().mean_measures == approx(0.01 * slow_factor, abs=0.005 * slow_factor)


def test_total_measures(clock, slow_factor):
    for _ in range(5):
        with clock.measure():
            time.sleep(0.01 * slow_factor)

    assert clock.total_measures == approx(0.05 * slow_factor, abs=0.01 * slow_factor)


def test_clock_can_have_a_name():
    assert PerformanceClock("a name").name == "a name"


def test_performance_clock_decorators(caplog, set_logging_active):
    @clock_performance("process")
    def some_process():
        time.sleep(0.01)

    @clock_performance("io")
    def some_io():
        time.sleep(0.03)

    log("process").every(10)
    log("io").every(1)

    with caplog.at_level(logging.INFO):
        for _ in range(10):
            some_process()
            some_io()
        assert sum("some_io" in r.msg for r in caplog.records) == 10
        assert sum("some_process" in r.msg for r in caplog.records) == 1


def test_performance_clock_on_class_methods(caplog, set_logging_active):
    class SomeClass:
        @clock_performance("process")
        def some_method(self):
            time.sleep(0.01)

    log("process").every(1)

    with caplog.at_level(logging.INFO):
        obj = SomeClass()
        obj.some_method()
        assert sum("some_method" in r.msg for r in caplog.records) == 1


def test_ignore_performance_logging_if_environment_variable_is_not_set(caplog):
    @clock_performance("process")
    def some_process():
        time.sleep(0.01)

    log("process").every(1)

    with caplog.at_level(logging.INFO):
        some_process()

    assert len(caplog.records) == 0
