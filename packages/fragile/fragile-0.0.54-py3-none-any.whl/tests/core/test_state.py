from typing import Any, Dict

from judo.data_types import dtype
import pytest

from fragile.core.state import State


param_dict_list = {
    "list_param_int": {"shape": None, "dtype": int},
    "list_param_list": {"shape": None, "dtype": list},
    "list_param_dict": {"shape": None, "dtype": dict},
    "list_param_set": {"shape": None, "dtype": set},
}

param_dict_vector = {
    "vec_float_16": {"dtype": dtype.float16},
    "vec_float_32": {"dtype": dtype.float32},
    "vec_bool": {"dtype": dtype.bool},
    "vec_int_shape": {"shape": tuple(), "dtype": dtype.int64},
}

param_dict_tensor = {
    "tensor_float_20_17": {"shape": (20, 17), "dtype": dtype.float16},
    "tensor_float_1": {"shape": (1,), "dtype": dtype.float32},
    "tensor_int_1_17_5": {"shape": (1, 17, 5), "dtype": dtype.int64},
}


param_dict_mix = {
    "observs": {"shape": (20, 17), "dtype": dtype.float16},
    "rewards": {"dtype": dtype.float32},
    "oobs": {"dtype": dtype.bool},
    "actions": {"shape": (1, 17), "dtype": dtype.int64},
    "list_param": {"shape": None, "dtype": int},
}

param_dict_examples = [param_dict_list, param_dict_vector, param_dict_tensor, param_dict_mix]
param_dict_ids = ["list_param_dict", "vector_param_dict", "tensor_param_dict", "mix_param_dict"]


@pytest.fixture(params=param_dict_examples, ids=param_dict_ids)
def param_dict(request) -> Dict[str, Any]:
    return request.param


@pytest.fixture()
def n_walkers() -> int:
    return 7


class TestState:
    def test_init(self, param_dict, n_walkers):
        state = State(n_walkers=n_walkers, param_dict=param_dict)
        for name in param_dict.keys():
            assert name in state.names
