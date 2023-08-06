from typing import TypeVar, Callable

from eotransform.protocol.transformer import Transformer, TransformerT, TransformerU

ApplyT = TypeVar('ApplyT')
ApplyU = TypeVar('ApplyU')


class Apply(Transformer[ApplyT, ApplyU]):
    """
    Applies an arbitrary function to the input which takes the input as argument and returns a transformed output

    >>> Apply(lambda x: f"The answer is: {x}")(42)
    'The answer is: 42'
    """

    def __init__(self, fn: Callable[[ApplyT], ApplyU]):
        self._fn = fn

    def __call__(self, x: TransformerT) -> TransformerU:
        return self._fn(x)
