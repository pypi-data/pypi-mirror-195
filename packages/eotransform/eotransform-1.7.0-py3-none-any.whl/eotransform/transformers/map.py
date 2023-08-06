from typing import Iterator, Sequence, TypeVar

from eotransform.protocol.transformer import Transformer

MapInT = TypeVar('MapInT')
MapOutT = TypeVar('MapOutT')


class Map(Transformer[Sequence[MapInT], Iterator[MapOutT]]):
    """
    Applying a transformation to a sequence of input data, i.e.:

    >>> class PlusOne(Transformer[int, int]):
    ...     def __call__(self, x):
    ...         return x + 1
    ...
    >>> list(Map(PlusOne())([0, 1, 2]))
    [1, 2, 3]
    """

    def __init__(self, map_transformer: Transformer[MapInT, MapOutT]):
        """
        :param map_transformer: Transformer applied to each element in the sequence
        """
        self._map_transformer = map_transformer

    def __call__(self, x: Sequence[MapInT]) -> Iterator[MapOutT]:
        return map(self._map_transformer, x)
