from abc import abstractmethod
from typing import TypeVar, Generic

TransformerT = TypeVar('TransformerT')
TransformerU = TypeVar('TransformerU')


class Transformer(Generic[TransformerT, TransformerU]):
    @abstractmethod
    def __call__(self, x: TransformerT) -> TransformerU:
        ...


PredicatedTransformerKey = TypeVar('PredicatedTransformerKey')
PredicatedTransformerIn = TypeVar('PredicatedTransformerIn')
PredicatedTransformerOut = TypeVar('PredicatedTransformerOut')


class PredicatedTransformer(Generic[PredicatedTransformerKey, PredicatedTransformerIn, PredicatedTransformerOut]):
    @abstractmethod
    def is_applicable(self, k: PredicatedTransformerKey) -> bool:
        ...

    @abstractmethod
    def apply(self, k: PredicatedTransformerKey, x: PredicatedTransformerIn) -> PredicatedTransformerOut:
        ...
