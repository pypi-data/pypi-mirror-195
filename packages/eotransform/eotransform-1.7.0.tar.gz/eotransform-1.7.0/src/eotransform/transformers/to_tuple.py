from typing import Iterable, Tuple, TypeVar

from eotransform.protocol.transformer import Transformer

TupleElemT = TypeVar('TupleElemT')


class ToTuple(Transformer[Iterable[TupleElemT], Tuple[TupleElemT, ...]]):
    """
    Fill element of an iterable stream into a tuple
    >>> ToTuple()([0, 1, 2])
    (0, 1, 2)
    """

    def __call__(self, x: Iterable[TupleElemT]) -> Tuple[TupleElemT, ...]:
        return tuple(x)
