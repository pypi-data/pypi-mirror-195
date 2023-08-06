import pytest
import numpy as np
from dsf.reciprocal import calc_rho_k, calc_rho_j_k
from dsf.conf import conf


# Setup test arrays and inputs

@pytest.fixture
def xvk():
    Nx = 4
    Nk = 5
    x = np.random.normal(size=(3, Nx))
    v = np.random.normal(size=(3, Nx))
    k = np.random.normal(size=(3, Nk))
    return x, v, k


def test_rho_k(xvk):
    x, v, k = xvk
    conf['backend'] = 'c'
    rho_k_c = calc_rho_k(x, k)

    conf['backend'] = 'numba'
    rho_k_numba = calc_rho_k(x, k)

    assert np.allclose(rho_k_c, rho_k_numba)


def test_rho_j_k(xvk):
    x, v, k = xvk
    conf['backend'] = 'c'
    rho_k_c, rho_j_k_c = calc_rho_j_k(x, v, k)

    conf['backend'] = 'numba'
    rho_k_numba, rho_j_k_numba = calc_rho_j_k(x, v, k)

    assert np.allclose(rho_k_c, rho_k_numba)
    assert np.allclose(rho_j_k_c, rho_j_k_numba)
