from eotransform.transformers.map import Map
from trivial_implementations import Add


def test_map_transform_to_sequence():
    mapper = Map(Add(1))
    assert list(mapper([0, 1, 2])) == [1, 2, 3]
