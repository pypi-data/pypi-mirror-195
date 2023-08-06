from typing import Dict, Sequence

from eotransform.protocol.transformer import PredicatedTransformer


def transform_all_dict_elems(d: Dict, pred_trans: PredicatedTransformer):
    return {k: _transform_element_in_collection(d, k, pred_trans) for k in d}


def transform_all_sequence_elems(s: Sequence, pred_trans: PredicatedTransformer):
    if isinstance(s, list):
        return [_transform_element_in_collection(s, i, pred_trans) for i, _ in enumerate(s)]
    elif isinstance(s, tuple):
        return tuple(_transform_element_in_collection(s, i, pred_trans) for i, _ in enumerate(s))


def _transform_element_in_collection(collection, index, pred_trans):
    v = collection[index]
    if pred_trans.is_applicable(index):
        return pred_trans.apply(index, v)
    if isinstance(v, dict):
        return transform_all_dict_elems(v, pred_trans)
    if isinstance(v, (list, tuple)):
        return transform_all_sequence_elems(v, pred_trans)
    return v
