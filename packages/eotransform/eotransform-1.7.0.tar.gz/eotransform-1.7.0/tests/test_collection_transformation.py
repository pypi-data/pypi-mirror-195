from eotransform.collection_transformation import transform_all_dict_elems
from eotransform.protocol.transformer import PredicatedTransformer, PredicatedTransformerKey, PredicatedTransformerIn, \
    PredicatedTransformerOut


class PredicatedTransformerStub(PredicatedTransformer):

    def is_applicable(self, k: PredicatedTransformerKey) -> bool:
        return k == "transformable"

    def apply(self, k: PredicatedTransformerKey, x: PredicatedTransformerIn) -> PredicatedTransformerOut:
        return 42


def test_transform_nested_collection():
    collection = dict(nested=dict(transformable="What is the answer?", list=["stable", "stable"]),
                      list=["stable", "stable"], tuple=("stable", dict(transformable="What is the answer?")),
                      transformable="The value is not important")
    assert transform_all_dict_elems(collection, PredicatedTransformerStub()) == \
           dict(nested=dict(transformable=42, list=["stable", "stable"]),
                list=["stable", "stable"], tuple=("stable", dict(transformable=42)),
                transformable=42)
