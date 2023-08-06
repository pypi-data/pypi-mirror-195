from typing import Dict, Iterable, Iterator, TypeVar

from eotransform.protocol.transformer import Transformer

InSelectT = TypeVar('InSelectT')
OutSelectT = TypeVar('OutSelectT')


class ApplyToEnumeration(Transformer[Iterable[InSelectT], Iterator[OutSelectT]]):
    """
    Apply a transformations to the element of an enumeration selected by the index
    >>> class Plus(Transformer[int, int]):
    ...     def __init__(self, value):
    ...         self.value = value
    ...
    ...     def __call__(self, x):
    ...         return x + self.value
    ...
    >>> list(ApplyToEnumeration({1: Plus(1), 2: Plus(2)})([0, 1, 2]))
    [0, 2, 4]
    """

    def __init__(self, transforms: Dict[int, Transformer[Iterable[InSelectT], Iterator[OutSelectT]]]):
        """
        :param transforms: Dictionary of transformations applied to the index specified as key
        """
        self._transforms = transforms

    def __call__(self, x: Iterable[InSelectT]) -> Iterator[OutSelectT]:
        for i, elem in enumerate(x):
            if i in self._transforms:
                yield self._transforms[i](elem)
            else:
                yield elem
