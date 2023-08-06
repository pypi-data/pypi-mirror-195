import pytest

from eotransform.result import Result
from eotransform.transformers.result import ApplyToOkResult, Unwrap


def test_apply_to_ok_result_transforms_ok_result():
    x = Result.ok(42)
    assert ApplyToOkResult(lambda r: r + 1)(x).unwrap() == 43


def test_apply_to_ok_result_hands_through_error_without_applying_any_transformation():
    def a_transform(_):
        assert False

    x = Result.error(AssertionError("an error occurred"))
    x = ApplyToOkResult(a_transform)(x)
    with pytest.raises(AssertionError):
        x.unwrap()


def test_unwrap_result():
    assert Unwrap()(Result.ok(42)) == 42
    with pytest.raises(AssertionError):
        Unwrap()(Result.error(AssertionError("an error occured")))
