from eotransform.transformers.to_tuple import ToTuple


def test_fill_iterable_into_tuple():
    assert ToTuple()([0, 1]) == (0, 1)
