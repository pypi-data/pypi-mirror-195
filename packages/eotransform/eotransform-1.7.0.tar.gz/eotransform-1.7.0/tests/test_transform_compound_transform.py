from eotransform.transformers.compose import Compose
from trivial_implementations import Add, Mul


def test_composing_transformations():
    assert Compose([Add(1), Mul(2)])(1) == 4
