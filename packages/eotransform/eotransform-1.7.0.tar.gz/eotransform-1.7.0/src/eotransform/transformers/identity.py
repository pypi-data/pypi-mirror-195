from typing import TypeVar

from eotransform.protocol.transformer import Transformer

IdentityT = TypeVar('IdentityT')


class Identity(Transformer[IdentityT, IdentityT]):
    """
    The identity transformation
    >>> Identity()(42)
    42
    """

    def __call__(self, x: IdentityT) -> IdentityT:
        return x
