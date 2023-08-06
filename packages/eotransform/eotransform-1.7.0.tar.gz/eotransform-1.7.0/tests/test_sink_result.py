import pytest
from eotransform.result import Result
from eotransform.sinks.result import SinkUnwrapped

from tests.helpers.doubles import SinkSpy


def test_sink_unwrapped_result():
    sink = SinkSpy()
    unwrapped_sink = SinkUnwrapped(sink)
    unwrapped_sink(Result.ok(42))
    assert sink.received_values == [42]
    with pytest.raises(AssertionError):
        unwrapped_sink(Result.error(AssertionError("an error occurred")))


def test_sink_unwrapped_result_ignores_specified_exceptions():
    class SomeTestError(AssertionError):
        ...

    sink = SinkSpy()
    unwrapped_sink = SinkUnwrapped(sink, ignore_exceptions={SomeTestError})
    unwrapped_sink(Result.error(SomeTestError("an error to be ignored")))
    assert sink.received_values == []
