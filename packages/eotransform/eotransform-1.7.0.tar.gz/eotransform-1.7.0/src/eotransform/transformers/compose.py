from typing import Iterable, TypeVar

from eotransform.protocol.transformer import Transformer

ComposedT = TypeVar('ComposedT')
ComposedU = TypeVar('ComposedU')


class Compose(Transformer[ComposedT, ComposedU]):
    """
    Composing a sequence of transformations together

    >>> class PlusOne(Transformer[int, int]):
    ...     def __call__(self, x):
    ...         return x + 1
    ...
    >>> Compose([PlusOne(), PlusOne()])(0)
    2
    """

    def __init__(self, transformations: Iterable[Transformer]):
        """
        :param transformations: Multiple transformations applied to the input data
        """
        self._transformations = transformations

    def __call__(self, x: ComposedT) -> ComposedU:
        for t in self._transformations:
            x = t(x)
        return x
