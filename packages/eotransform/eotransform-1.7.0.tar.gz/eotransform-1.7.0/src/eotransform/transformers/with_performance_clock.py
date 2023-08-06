from typing import TypeVar

from eotransform.protocol.transformer import Transformer
from eotransform.utilities.profiling import PerformanceClock

ClockedT = TypeVar("ClockedT")
ClockedU = TypeVar("ClockedU")


class WithPerformanceClock(Transformer[ClockedT, ClockedU]):
    def __init__(self, wrapped: Transformer, clock: PerformanceClock):
        self._wrapped = wrapped
        self._clock = clock

    def __call__(self, x):
        with self._clock.measure():
            return self._wrapped(x)
