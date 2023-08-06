from eotransform.transformers.apply_to_enumeration import ApplyToEnumeration
from trivial_implementations import Add, ReplaceWithString


def test_also_works_with_tuples():
    assert tuple(ApplyToEnumeration({
        0: ReplaceWithString("the answer:"),
        1: Add(40)})((1, 2, 3))) == ("the answer:", 42, 3)
