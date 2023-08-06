from eotransform.transformers.identity import Identity


def test_transform_identity_does_nothing():
    assert Identity()(42) == 42
