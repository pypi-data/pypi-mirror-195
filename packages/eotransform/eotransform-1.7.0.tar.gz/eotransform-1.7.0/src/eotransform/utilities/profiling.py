import logging
import os
import time
from contextlib import contextmanager
from functools import wraps
from typing import Optional

PERFORMANCE_LOG_ENV_VAR = 'CORRELATION_MAP_PERFORMANCE_LOG'
NANOSECONDS_PER_SECOND = 1e9

class PerformanceClock:
    def __init__(self, name: Optional[str] = ""):
        self._measures = []
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @contextmanager
    def measure(self):
        start = time.perf_counter_ns()
        yield
        self._measures.append((time.perf_counter_ns() - start) / NANOSECONDS_PER_SECOND)

    @property
    def total_measures(self):
        return sum(self._measures)

    @property
    def mean_measures(self):
        return self.total_measures / len(self._measures)

    def drop_first(self):
        self._measures = self._measures[1:]
        return self


_LOGGING_FREQUENCIES = dict()


def log(domain: str):
    class _FrequencySetter:
        def __init__(self, domain):
            self._domain = domain

        def every(self, frequency: int):
            _LOGGING_FREQUENCIES[self._domain] = frequency

    return _FrequencySetter(domain)


def clock_performance(domain: str):
    def _clock_performance(func):
        if not os.environ.get(PERFORMANCE_LOG_ENV_VAR, False):
            return func

        clock = PerformanceClock()
        log_n = 0
        freq = None

        @wraps(func)
        def _decorator(*args, **kwargs):
            nonlocal freq
            nonlocal log_n
            nonlocal clock
            if freq is None:
                freq = _LOGGING_FREQUENCIES.get(domain, 0)
            if freq == 0:
                return func(*args, **kwargs)

            with clock.measure():
                response = func(*args, **kwargs)

            log_n += 1
            if log_n % freq == 0:
                logging.info(f"{domain}::{func.__name__}: {clock.mean_measures}")
            return response

        return _decorator

    return _clock_performance
