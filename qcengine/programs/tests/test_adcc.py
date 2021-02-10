"""Tests for adcc functionality"""
import pytest
import numpy as np
import qcengine as qcng
import qcelemental as qcel

from qcengine.testing import using
from qcelemental.testing import compare_values


@pytest.fixture
def h2o():
    return qcel.models.Molecule.from_data(
        """
      O  0.0  0.000  -0.129
      H  0.0 -1.494  1.027
      H  0.0  1.494  1.027
      """
    )


@using("adcc")
def test_run(h2o):
    inp = qcel.models.AtomicInput(
        molecule=h2o, driver="properties", model={"method": "adc2", "basis": "sto-3g"}, keywords={"n_singlets": 3}
    )
    ret = qcng.compute(inp, "adcc", raise_error=True, local_options={"ncores": 1}, return_dict=True)

    ref_excitations = np.array([0.0693704245883876, 0.09773854881340478, 0.21481589246935925])
    ref_hf_energy = -74.45975898670224
    ref_mp2_energy = -74.67111187456267
    assert ret["success"] is True

    ret_qcvars = ret["extras"]["qcvars"]

    assert ret_qcvars["EXCITATION KIND"] == "SINGLET"
    assert compare_values(ref_excitations, ret["return_result"])
    assert compare_values(ref_hf_energy, ret_qcvars["HF TOTAL ENERGY"])
    assert compare_values(ref_mp2_energy, ret_qcvars["MP2 TOTAL ENERGY"])
