from abc import abstractmethod
from typing import TypeVar, Generic

SinkT = TypeVar('SinkT')


class Sink(Generic[SinkT]):
    """
    Basic protocol to consume data
    """

    @abstractmethod
    def __call__(self, x: SinkT) -> None:
        ...
