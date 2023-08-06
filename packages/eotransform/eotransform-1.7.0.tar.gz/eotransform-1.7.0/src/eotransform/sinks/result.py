from typing import TypeVar

from eotransform.protocol.sink import Sink, SinkT
from eotransform.result import Result

ErrT = TypeVar("ErrT")


class SinkUnwrapped(Sink[Result[SinkT, ErrT]]):
    """
    Unwrap a result object before passing it onto the wrapped sink. Also allows for automatically ignoring exceptions.
    >>> class RecordingSink(Sink[int]):
    ...     def __init__(self):
    ...          self.record = []
    ...     def __call__(self, x: int) -> None:
    ...          self.record.append(x)
    >>> sink = RecordingSink()
    >>> SinkUnwrapped(sink)(Result.ok(42))
    >>> sink.record
    [42]
    >>> SinkUnwrapped(sink, ignore_exceptions={RuntimeError})(Result.error(RuntimeError("An error to be ignored")))
    >>> sink.record
    [42]
    """
    def __init__(self, wrapped_sink: Sink[SinkT], ignore_exceptions=None):
        """
        @param wrapped_sink: sink to which the unwrapped object is passed
        @param ignore_exceptions: set of exception types to be ignored
        """
        self._wrapped_sink = wrapped_sink
        self._ignore_exceptions = ignore_exceptions or set()

    def __call__(self, x: Result[SinkT, ErrT]) -> None:
        x = x.ignore(self._ignore_exceptions)
        if not x.is_ignored():
            self._wrapped_sink(x.unwrap())
