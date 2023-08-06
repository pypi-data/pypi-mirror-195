import numpy as np
import os
import pytest
from dsf.dynasor_API import compute_correlation_functions_static_qiso, \
    compute_correlation_functions_dynamic_qiso, \
    compute_correlation_functions_static_qline, compute_correlation_functions_dynamic_qline
from dsf.conf import conf


@pytest.fixture
def traj_fname_xyz():
    this_dir = os.path.dirname(__file__)
    traj_fname = os.path.join(this_dir, 'trajectory_reader/trajectory_files/dump.xyz')
    return traj_fname


def test_API_static_qiso(traj_fname_xyz):
    print(traj_fname_xyz)
    res = compute_correlation_functions_static_qiso(traj_fname_xyz)
    assert len(res) == 8


def test_API_dynamic_qiso(traj_fname_xyz):
    res = compute_correlation_functions_dynamic_qiso(traj_fname_xyz, time_window=3, dt=1.0)
    assert len(res) == 12


def test_API_static_qline(traj_fname_xyz):
    q_dir = [1, 0, 0]
    res = compute_correlation_functions_static_qline(traj_fname_xyz, q_direction=q_dir)
    assert len(res) == 8


def test_API_dynamic_qline(traj_fname_xyz):
    q_dir = [1, 0, 0]
    res = compute_correlation_functions_dynamic_qline(
        traj_fname_xyz, q_direction=q_dir, time_window=3, dt=1.0)
    assert len(res) == 12


def test_API_dynamic_qline_backends_and_selfpart(traj_fname_xyz):
    q_dir = [1, 0, 0]

    conf['backend'] = 'c'
    res1 = compute_correlation_functions_dynamic_qline(
        traj_fname_xyz, q_direction=q_dir, time_window=3, dt=1.0, calculate_self=True)
    assert len(res1) == 14

    conf['backend'] = 'numba'
    res2 = compute_correlation_functions_dynamic_qline(
        traj_fname_xyz, q_direction=q_dir, time_window=3, dt=1.0, calculate_self=True)
    assert len(res2) == 14

    data_dict1 = dict()
    for (val, key, info) in res1:
        data_dict1[key] = val
    data_dict2 = dict()
    for (val, key, info) in res2:
        data_dict2[key] = val

    # compare all
    for key in data_dict1.keys():
        v1 = data_dict1[key]
        v2 = data_dict2[key]
        assert np.allclose(v1, v2)


def test_API_sed(traj_fname_xyz):
    pass  # compute_spectral_energy_density
