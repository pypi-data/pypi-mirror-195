from abc import abstractmethod
from typing import Any, Optional

try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol

from eotransform.protocol.sink import Sink


class Reporter(Protocol):
    @abstractmethod
    def update(self, n: Optional[int] = 1) -> None:
        ...


class SinkToProgressReport(Sink[Any]):
    def __init__(self, reporter: Reporter):
        self._reporter = reporter

    def __call__(self, x: Any) -> None:
        self._reporter.update()
