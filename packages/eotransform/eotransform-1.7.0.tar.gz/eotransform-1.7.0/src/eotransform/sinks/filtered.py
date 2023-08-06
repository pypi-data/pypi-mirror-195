from typing import Callable

from eotransform.protocol.sink import Sink, SinkT


class SinkFiltered(Sink[SinkT]):
    """
    Allows to filter items for passing them to the wrapped sink.
    >>> class RecordingSink(Sink[int]):
    ...     def __init__(self):
    ...          self.record = []
    ...     def __call__(self, x: int) -> None:
    ...          self.record.append(x)
    >>> wrapped_sink = RecordingSink()
    >>> filtered_sink = SinkFiltered(wrapped_sink, lambda x: x % 2 == 1)
    >>> for i in range(4):
    ...     filtered_sink(i)
    >>> wrapped_sink.record
    [1, 3]
    """
    def __init__(self, wrapped_sink: Sink[SinkT], predicate: Callable[[SinkT], bool]):
        """
        :param wrapped_sink: the sink the filtered items are passed to
        :param predicate: callable which determines if an item is passed to the wrapped sink
        """
        self._wrapped_sink = wrapped_sink
        self._predicate = predicate

    def __call__(self, x: SinkT) -> None:
        if self._predicate(x):
            self._wrapped_sink(x)
