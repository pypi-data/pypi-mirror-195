from typing import TypeVar

from eotransform.protocol.sink import Sink
from eotransform.utilities.profiling import PerformanceClock

ClockedSinkT = TypeVar("ClockedSinkT")


class WithPerformanceClock(Sink[ClockedSinkT]):
    def __init__(self, wrapped: Sink, clock: PerformanceClock):
        self._wrapped = wrapped
        self._clock = clock

    def __call__(self, x: ClockedSinkT) -> None:
        with self._clock.measure():
            return self._wrapped(x)
