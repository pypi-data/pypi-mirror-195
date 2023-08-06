from abc import ABC
from typing import TypeVar

from eotransform.protocol.transformer import Transformer
from eotransform.result import Result

T = TypeVar('T')
E = TypeVar('E')


class ResultTransformation(Transformer[Result[T, E], Result[T, E]], ABC):
    ...


class ApplyToOkResult(ResultTransformation):
    def __init__(self, transformation):
        self._transformation = transformation

    def __call__(self, x: Result[T, E]) -> Result[T, E]:
        if x.is_error():
            return x
        return Result.ok(self._transformation(x.unwrap()))


class Unwrap(ResultTransformation):
    def __call__(self, x: Result[T, E]) -> T:
        return x.unwrap()
