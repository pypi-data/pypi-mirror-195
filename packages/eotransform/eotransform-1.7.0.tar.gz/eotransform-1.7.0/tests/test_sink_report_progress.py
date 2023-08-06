import pytest

from eotransform.sinks.sink_to_progress_report import Reporter, SinkToProgressReport


class ReporterSpy(Reporter):
    def __init__(self):
        self.num_update_calls_received = 0

    def update(self, n=1) -> None:
        self.num_update_calls_received += 1


@pytest.fixture
def reporter():
    return ReporterSpy()


def test_report_iteration(reporter):
    sink = SinkToProgressReport(reporter)
    sink(42)
    assert reporter.num_update_calls_received == 1
    sink(42)
    assert reporter.num_update_calls_received == 2
