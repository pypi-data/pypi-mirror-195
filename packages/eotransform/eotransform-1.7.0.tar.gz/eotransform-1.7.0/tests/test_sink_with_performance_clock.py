import time

from pytest import approx

from eotransform.protocol.sink import Sink
from eotransform.sinks.with_performance_clock import WithPerformanceClock
from eotransform.utilities.profiling import PerformanceClock


class ASinkThatTakes(Sink):
    def __init__(self, seconds):
        self._seconds = seconds

    def __call__(self, x):
        time.sleep(self._seconds)
        return x


def test_clock_runtime_performance_of_sink(slow_factor):
    clock = PerformanceClock()
    transform = WithPerformanceClock(ASinkThatTakes(seconds=0.1 * slow_factor), clock)
    transform(0)
    assert clock.total_measures == approx(0.1 * slow_factor, abs=0.01 * slow_factor)
