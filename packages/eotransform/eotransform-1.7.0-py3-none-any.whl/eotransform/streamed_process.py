from concurrent.futures import ThreadPoolExecutor
from queue import Queue, Empty, Full
from threading import Event
from typing import TypeVar, Iterable, Iterator

from eotransform.protocol.sink import Sink
from eotransform.protocol.transformer import Transformer

StreamedInT = TypeVar('StreamedInT')
StreamedOutT = TypeVar('StreamedOutT')
ReturnPipeT = TypeVar('ReturnPipeT')
InSource = Iterable[StreamedInT]
ProcessTransformer = Transformer[StreamedInT, StreamedOutT]
OutSink = Sink[StreamedOutT]


class ReturnPipeIterator(Iterator[ReturnPipeT]):
    def __init__(self, pipe: Queue, timeout: float):
        self._pipe = pipe
        self._timeout = timeout

    def __next__(self) -> ReturnPipeT:
        while True:
            elem = self._pipe.get(timeout=self._timeout)
            self._pipe.task_done()
            if elem is StopIteration:
                raise elem
            return elem


class ReturnPipeStream(Iterable[ReturnPipeT]):
    def __init__(self, pipe: Queue, timeout: float):
        self._pipe = pipe
        self._timeout = timeout

    def __iter__(self) -> Iterator[ReturnPipeT]:
        return ReturnPipeIterator(self._pipe, self._timeout)


def _producer(source: InSource, pipe: Queue, cancel_event: Event) -> None:
    for elem in source:
        if cancel_event.is_set():
            return
        else:
            pipe.put(elem)

    if not cancel_event.is_set():
        pipe.put(StopIteration)


def _consumer(sink: OutSink, pipe: Queue) -> None:
    for elem in ReturnPipeStream(pipe, 9999):
        sink(elem)


def streamed_process(source: InSource, process: ProcessTransformer, dst_sink: OutSink,
                     executor: ThreadPoolExecutor, loading_timeout: float = 120, storing_timeout: float = 120) -> None:
    """
    Interleaves the data loading from source with the data processing, and finally putting it into the sink. This can be
    used to hide IO processed i.e.:
    thread_0: IN->IN->IN
    thread_1:   ->PR->PR->PR
    thread_2:       ->SK->SK->SK

    :param source: Input data fed to the process transformation
    :param process: Transformation changing the input data to the output data
    :param dst_sink: Sink receiving the output data
    :param executor: Thread pool executor used to spawn async threads for IO hiding
    :param loading_timeout: Timeout for the loading process in seconds (default: 120)
    :param storing_timeout: Timout for the storing process in seconds (default: 120)
    """

    source_pipe = Queue(maxsize=1)
    sink_pipe = Queue(maxsize=1)

    cancel_production_event = Event()
    producer = executor.submit(_producer, source, source_pipe, cancel_production_event)
    consumer = executor.submit(_consumer, dst_sink, sink_pipe)

    try:
        for x in ReturnPipeStream(source_pipe, loading_timeout):
            sink_pipe.put(process(x), timeout=storing_timeout)
    except Empty:
        ...
    finally:
        cancel_production_event.set()
        try:
            sink_pipe.put(StopIteration, timeout=storing_timeout)
        except Full:
            ...
        finally:
            for _ in range(source_pipe.unfinished_tasks):
                source_pipe.get_nowait()
                source_pipe.task_done()

            producer.result(timeout=loading_timeout)
            consumer.result(timeout=storing_timeout)
            _unsafe_pipe_clear(source_pipe)
            source_pipe.join()
            sink_pipe.join()


def _unsafe_pipe_clear(pipe: Queue):
    pipe.queue.clear()
    for _ in range(pipe.unfinished_tasks):
        pipe.task_done()
