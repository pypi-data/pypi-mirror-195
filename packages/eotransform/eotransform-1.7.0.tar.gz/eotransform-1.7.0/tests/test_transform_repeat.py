from eotransform.transformers.repeat import Repeat


def test_repeat_input_n_times():
    assert list(Repeat(2)(42)) == [42, 42]
