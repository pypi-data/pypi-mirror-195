from eotransform.sinks.filtered import SinkFiltered

from tests.helpers.doubles import SinkSpy


def test_sink_only_items_where_lambda_returns_true():
    def is_even(x):
        return x % 2 == 0

    sink_wrapped = SinkSpy()
    sink_filtered = SinkFiltered(sink_wrapped, is_even)
    [sink_filtered(i) for i in range(5)]
    assert sink_wrapped.received_values == [0, 2, 4]
