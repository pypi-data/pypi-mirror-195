from eotransform.apply import Apply


def test_transform_using_supplied_function():
    assert Apply(lambda x: x * 2)(2) == 4
