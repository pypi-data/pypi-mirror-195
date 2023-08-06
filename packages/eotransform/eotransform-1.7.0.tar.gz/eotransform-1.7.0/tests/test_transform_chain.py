from eotransform.transformers.chain import Chain


def test_chain_iterable():
    assert list(Chain()([[0, 1], [2, 3, 4]])) == [0, 1, 2, 3, 4]
