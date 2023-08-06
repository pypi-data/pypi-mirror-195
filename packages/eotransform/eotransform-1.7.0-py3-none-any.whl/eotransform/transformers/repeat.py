from itertools import repeat
from typing import TypeVar, Iterator

from eotransform.protocol.transformer import Transformer

RepeatedT = TypeVar('RepeatedT')


class Repeat(Transformer[RepeatedT, Iterator[RepeatedT]]):
    """
    Repeat the input n times and return an iterator which can for instance be used to create a collection, such as list.
    >>> list(Repeat(3)(42))
    [42, 42, 42]
    """

    def __init__(self, n: int):
        """
        :param n: Number of times the input is repeated.
        """
        self._n = n

    def __call__(self, x: RepeatedT) -> Iterator[RepeatedT]:
        return repeat(x, self._n)
