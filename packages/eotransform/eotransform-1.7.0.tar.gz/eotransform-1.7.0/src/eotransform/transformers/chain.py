from itertools import chain
from typing import TypeVar, Iterable, Iterator

from eotransform.protocol.transformer import Transformer

ChainT = TypeVar('ChainT')


class Chain(Transformer[Iterable[ChainT], Iterator[ChainT]]):
    """
    Chain multiple iterables together into one iterator, i.e.:

    >>> list(Chain()([[0, 1], [2]]))
    [0, 1, 2]
    """

    def __call__(self, x: Iterable[ChainT]) -> Iterator[ChainT]:
        return chain.from_iterable(x)
