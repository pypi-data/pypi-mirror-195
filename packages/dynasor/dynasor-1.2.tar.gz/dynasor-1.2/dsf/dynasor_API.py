"""
The dynasor API

Note q-points are always given in units of 2 * pi * nm^-1
"""

import os
import sys
import numpy as np

from collections import deque
from functools import partial
from itertools import count, islice
from typing import List, Tuple

import dsf.filon as filon
from ase import Atoms
from dsf.averager import averager
from dsf.binner import fixed_bin_averager
from dsf.handythread import foreach
from dsf.index import section_index
from dsf.reciprocal import reciprocal_isotropic, reciprocal_line
from dsf.trajectory import get_itraj, iwindow
from dsf.logging_tools import logger, set_logging_level

from multiprocessing import cpu_count
from scipy.interpolate import interp1d


# Constants
pi = np.pi
two_pi = 2.0 * pi


# API functions
# -------------------

def compute_correlation_functions_static_qiso(
        trajectory_file, index_file=None, max_frames=100,
        q_max=60.0, q_bins=80, max_q_points=20000,
        n_threads=None, log_level='INFO', calculate_self=False):
    """
    Compute static structure factors with isotropic q-point sampling,
    i.e. a spherical average over q-points will be made.

    Parameters
    -----------
    trajectory_file : str
        Molecular dynamics trajectory file to be analyzed. Supported formats depends on VMDs
        molfile plugin or gmxlib. As a fallback, a lammps-trajectory parser implemented in Python
        is available as well as a .extxyz reader based on ASE
    index_file : str
        Optional index file (think Gromacs INI-style) for specifying atom types. Atoms are indexed
        from 1 up to N (total number of atoms). It is possible to index only a sub set of all atoms,
        and atoms can be indexed in more than one group. If no INDEX_FILE is provided, all atoms
        will be considered identical
    max_frames : int
        Limits the total number of trajectory frames read to max_frames
    q_max : float
        Largest q-value to consider (in units of 2*pi*nm^-1)
    q_bins : int
        Number of "radial" bins to use (between 0 and largest |q|-value) when collecting resulting
        average
    max_q_points : int
        Maximum number of points used to sample q-space. Puts an (approximate) upper limit by
        randomly selecting points
    n_threads : int
        Number of threads to use. The default value is taken from OMP_NUM_THREADS if it is set,
        otherwise it is set to the number of available cpus
    log_level : str
        Verbosity level, available options include DEBUG, INFO, WARNING, ERROR.
        Default is INFO
    calculate_self : bool
        Calculate the self-part, F_s.
    """
    return _compute_correlation_functions(
        trajectory_file, index_file,
        time_window=None, max_frames=max_frames,
        q_sampling='isotropic',
        q_bins=q_bins, max_q_points=max_q_points, q_max=q_max,
        n_threads=n_threads, log_level=log_level, calculate_self=calculate_self)


def compute_correlation_functions_dynamic_qiso(
        trajectory_file: str,
        time_window: int,
        dt: float,
        step: int = 1,
        stride: int = 1,
        index_file: str = None,
        max_frames: int = 100,
        q_max: float = 60.0,
        q_bins: int = 80,
        max_q_points: int = 20000,
        n_threads: int = None,
        log_level: str = 'INFO',
        calculate_self: bool = False):
    """
    Compute static structure factors with isotropic q-point sampling,
    i.e., a spherical average over q-points will be made.

    Parameters
    -----------
    trajectory_file
        Molecular dynamics trajectory file to be analyzed. Supported formats depends on VMDs
        molfile plugin or gmxlib. As a fallback, a lammps-trajectory parser implemented in Python
        is available as well as a .extxyz reader based on ASE
    time_window
        The length of the trajectory frame window to use for time correlation calculation.
        It is expressed in number of frames and e.g. determines the smallest frequency resolved
    dt
        Explicitly sets the time difference between two consecutively processed trajectory frames
        to dt (in femtoseconds)
    step
        Only use every (step)th trajectory frame.
        step affects dt and hence the smallest time resolved
        (TODO, check how this works, and interacts with dt)
    stride
        Stride stride number of frames between consecutive trajectory windows.
        This does not affect dt. If e.g. stride > time_window, some frames will be completely unused
    index_file
        Optional index file (think Gromacs INI-style) for specifying atom types. Atoms are indexed
        from 1 up to N (total number of atoms). It is possible to index only a sub set of all atoms,
        and atoms can be indexed in more than one group. If no INDEX_FILE is provided, all atoms
        will be considered identical
    max_frames
        Limits the total number of trajectory frames read to max_frames
    q_max
        Largest q-value to consider (in units of 2*pi*nm^-1)
    q_bins
        Number of "radial" bins to use (between 0 and largest |q|-value) when collecting resulting
        average
    max_q_points
        Maximum number of points used to sample q-space. Puts an (approximate) upper limit by
        randomly selecting points
    n_threads
        Number of threads to use. The default value is taken from OMP_NUM_THREADS if it is set,
        otherwise it is set to the number of available cpus
    log_level
        Verbosity level, available options include DEBUG, INFO, WARNING, ERROR.
        Default is INFO
    calculate_self
        Calculate the self-part, F_s.
    """
    return _compute_correlation_functions(
        trajectory_file, index_file,
        dt=dt, step=step, stride=stride, time_window=time_window, max_frames=max_frames,
        q_sampling='isotropic',
        q_bins=q_bins, max_q_points=max_q_points, q_max=q_max,
        n_threads=n_threads, log_level=log_level, calculate_self=calculate_self)


def compute_correlation_functions_static_qline(
        trajectory_file: str,
        q_direction: Tuple[float, float, float],
        index_file: str = None,
        max_frames: int = 100,
        q_points: int = 100,
        n_threads: int = None,
        log_level: str = 'INFO',
        calculate_self: bool = False):
    """
    Compute static structure factors with sampled a long a line in q-space.

    Parameters
    -----------
    trajectory_file
        Molecular dynamics trajectory file to be analyzed. Supported formats depends on VMDs
        molfile plugin or gmxlib. As a fallback, a lammps-trajectory parser implemented in Python
        is available as well as a .extxyz reader based on ASE
    index_file
        Optional index file (think Gromacs INI-style) for specifying atom types. Atoms are indexed
        from 1 up to N (total number of atoms). It is possible to index only a sub set of all atoms,
        and atoms can be indexed in more than one group. If no INDEX_FILE is provided, all atoms
        will be considered identical
    max_frames
        Limits the total number of trajectory frames read to max_frames
    q_points
        Number of q-points to sample along line
    q_direction
        Direction along which to sample
    n_threads
        Number of threads to use. The default value is taken from OMP_NUM_THREADS if it is set,
        otherwise it is set to the number of available cpus
    log_level
        Verbosity level, available options include DEBUG, INFO, WARNING, ERROR.
        Default is INFO
    calculate_self
        Calculate the self-part, F_s.
    """
    return _compute_correlation_functions(
        trajectory_file, index_file,
        time_window=None, max_frames=max_frames,
        q_sampling='line', q_points=q_points, q_direction=q_direction,
        n_threads=n_threads, log_level=log_level, calculate_self=calculate_self)


def compute_correlation_functions_dynamic_qline(
        trajectory_file: str,
        q_direction: Tuple[float, float, float],
        time_window: int,
        dt: float,
        step: int = 1,
        stride: int = 1,
        index_file: str = None,
        max_frames: int = 100,
        q_points: int = 100,
        n_threads: int = None,
        log_level: str = 'INFO',
        calculate_self: bool = False):
    """
    Compute static structure factors with sampled a long a line in q-space.

    Parameters
    -----------
    trajectory_file
        Molecular dynamics trajectory file to be analyzed. Supported formats depends on VMDs
        molfile plugin or gmxlib. As a fallback, a lammps-trajectory parser implemented in Python
        is available as well as a .extxyz reader based on ASE
    index_file
        Optional index file (think Gromacs INI-style) for specifying atom types. Atoms are indexed
        from 1 up to N (total number of atoms). It is possible to index only a sub set of all atoms,
        and atoms can be indexed in more than one group. If no INDEX_FILE is provided, all atoms
        will be considered identical
    dt
        Explicitly sets the time difference between two consecutively processed trajectory frames
        to dt (in femtoseconds)
    time_window
        The length of the trajectory frame window to use for time correlation calculation.
        It is expressed in number of frames and e.g. determines the smallest frequency resolved
    step
        Only use every (step)th trajectory frame.
        step affects dt and hence the smallest time resolved
    stride
        Stride stride number of frames between consecutive trajectory windows.
        This does not affect dt. If e.g. stride > time_window, some frames will be completely unused
    max_frames
        Limits the total number of trajectory frames read to max_frames
    q_points
        Number of q-points to sample along line
    q_direction
        Direction along which to sample
    n_threads
        Number of threads to use. The default value is taken from OMP_NUM_THREADS if it is set,
        otherwise it is set to the number of available cpus
    log_level
        Verbosity level, available options include DEBUG, INFO, WARNING, ERROR.
        Default is INFO
    calculate_self
        Calculate the self-part, F_s.
    """
    return _compute_correlation_functions(
        trajectory_file, index_file,
        dt=dt, step=step, stride=stride, time_window=time_window, max_frames=max_frames,
        q_sampling='line', q_points=q_points, q_direction=q_direction,
        n_threads=n_threads, log_level=log_level, calculate_self=calculate_self)


# helper functions doing the heavy lifting
# ----------------------------------


def _compute_correlation_functions(
        trajectory_file: str,
        index_file: str = None,
        time_window: int = None,
        max_frames: int = 100,
        step: int = 1,
        stride: int = 1,
        dt: int = 1,
        q_sampling: str = 'isotropic',
        q_points: int = 100,
        q_direction: Tuple[float, float, float] = None,
        q_bins: int = 80,
        max_q_points: int = 20000,
        q_max: int = 60,
        n_threads: int = None,
        log_level: str = 'INFO',
        calculate_self: bool = False):
    """
    Compute dynamical structure factors

    Parameters
    -----------
    time_window (None means only static)
    """

    # sanity check input args
    assert max_frames > 0
    assert step > 0
    assert stride > 0
    assert dt > 0

    assert q_points > 0
    assert q_bins > 0
    assert max_q_points > 0
    assert q_max > 0

    # set log level
    set_logging_level(log_level)

    # decide how many threads to use
    if n_threads is not None:
        num_threads = n_threads
    elif 'OMP_NUM_THREADS' in os.environ:
        num_threads = int(os.environ['OMP_NUM_THREADS'])
    else:
        num_threads = cpu_count()
    if num_threads < 1:
        logger.error('Number of threads must be > 0')
        sys.exit(1)

    # Affects rho_j_k
    os.environ['OMP_NUM_THREADS'] = str(num_threads)

    # Read the two first frames to set up references values
    # box size, number of different particles, time step length, etc
    try:
        f0, f1 = islice(get_itraj(trajectory_file, step=step), 2)
    except ValueError:
        logger.error('Failed to read two consecutive frames to determine '
                     'delta t. Is the trajectory long enough?')
        sys.exit(1)

    # time between frames
    # delta_t = f1['time'] - f0['time']
    # logger.warning('-- Found {} between frames fs.'.format(delta_t))
    delta_t = dt
    logger.warning('-- Explicitly setting delta time to {} fs.'.format(dt))

    # time window (None means only static)
    if time_window is not None:
        assert time_window >= 1
        N_tc = time_window + (time_window + 1) % 2
    else:
        N_tc = 1

    if N_tc > 1:
        dw = two_pi / (time_window * delta_t)
        logger.info('-- delta_t found to be {} [fs], time window {} [fs]'
                    .format(delta_t, delta_t * (time_window - 1)))
        logger.info('-- delta_omega, max_omega = {}, {} [fs^-1]'.format(dw, dw * time_window))

    # Do we get any velocities from the trajectory reader?
    if 'v' in f0:
        calculate_current = True
    else:
        calculate_current = False

    # Should the particle self correlations be calculated?
    if calculate_self:
        logger.info('-- Calculating self-part of correlations')
    else:
        logger.info('-- Not calculating self-part of correlations')

    index = section_index(index_file, f0['N'])

    # box
    # TODO....
    # * Assert box is not changed during consecutive frames
    a, b, c = reference_box = f0['box']
    a1, b1, c1 = f1['box']
    assert np.allclose(a, a1)
    assert np.allclose(b, b1)
    assert np.allclose(c, c1)

    reference_volume = abs(np.dot(np.cross(a, b), c))
    particle_types = index.get_section_names()
    particle_counts = list(deque(map(len, index.get_section_indices())))
    particle_densities = [n / reference_volume for n in particle_counts]

    logger.info('Trajectory file: %s' % trajectory_file)
    logger.info('-- With a total of %i particles, %i types.' % (f0['N'], len(particle_types)))
    for i, t in enumerate(particle_types):
        logger.info('-- %d. %d %s' % (i + 1, particle_counts[i], t))
    logger.info('Simulation box is\n%s' % str(reference_box))

    # reciprocal space, q-points to sample
    # TODO: Log some info on q-points being sampled
    if q_sampling == 'line':
        rec = reciprocal_line(points=q_points, k_direction=q_direction)
    elif q_sampling == 'isotropic':
        rec = reciprocal_isotropic(reference_box, max_points=max_q_points, max_k=q_max)
    else:
        raise ValueError('Q-sampling must be either line or istotropic')

    # function to use to "calculate rho(k)"
    f2 = rec.get_frame_process_function()

    # function to split particles into different index groups (types)
    f1 = index.get_section_split_function()  # Prerequisite for f2

    # apply this to each frame considered
    element_processor = lambda frame: f2(f1(frame))   # noqa

    # The trajectory window iterator
    itraj_window = iwindow(get_itraj(trajectory_file, step=step, max_frames=max_frames),
                           width=N_tc, stride=stride, element_processor=element_processor)

    Ntypes = len(particle_types)
    m = count(0)
    pair_list = [(m.__next__(), i, j) for i in range(Ntypes) for j in range(i, Ntypes)]
    pair_types = [particle_types[i] + '-' + particle_types[j]
                  for _, i, j in pair_list]

    z = np.zeros(len(rec.q_distance))
    F_k_t_avs = [averager(N_tc, z) for _ in pair_list]
    if calculate_current:
        Cl_k_t_avs = [averager(N_tc, z) for _ in pair_list]
        Ct_k_t_avs = [averager(N_tc, z) for _ in pair_list]
    if calculate_self:
        F_s_k_t_avs = [averager(N_tc, z) for _ in particle_types]

    def calc_corr(window, time_i):
        # Calculate correlations between two frames in the window
        f0 = window[0]
        fi = window[time_i]
        for m, i, j in pair_list:
            F_k_t_avs[m][time_i] += np.real(f0['rho_ks'][i]
                                            * fi['rho_ks'][j].conjugate())

        if calculate_current:
            for m, i, j in pair_list:
                Cl_k_t_avs[m][time_i] += np.real(f0['jz_ks'][i]
                                                 * fi['jz_ks'][j].conjugate())
                Ct_k_t_avs[m][time_i] += 0.5 * \
                    np.real(np.sum(f0['jper_ks'][i]
                                   * fi['jper_ks'][j].conjugate(), axis=0))

        if calculate_self:
            for i, F_s in enumerate(
                rec.process_specific_xs(
                    [(xi - x0) for xi, x0 in zip(fi['xs'], f0['xs'])])):
                F_s_k_t_avs[i][time_i] += np.real(F_s)

    # This is the "main loop"
    for window in itraj_window:
        logger.debug("processing window step %i to %i" % (window[0]['index'],
                                                          window[-1]['index']))
        # Have num_threads threads concurrently process the window
        foreach(partial(calc_corr, window), range(len(window)), threads=num_threads)

    # Extract correlation (all k-point) averages
    # and calculate average per 'radial' bin
    k_bins = fixed_bin_averager(rec.max_k, q_bins, rec.k_distance)
    k_bin_averager = partial(k_bins.bin, axis=1)

    F_k_t = list(map(k_bin_averager, [F.get_av() for F in F_k_t_avs]))

    if calculate_current:
        Cl_k_t = list(map(k_bin_averager, [C.get_av() for C in Cl_k_t_avs]))
        Ct_k_t = list(map(k_bin_averager, [C.get_av() for C in Ct_k_t_avs]))

    if calculate_self:
        F_s_k_t = list(map(k_bin_averager, [C.get_av() for C in F_s_k_t_avs]))
        for i, N in enumerate(particle_counts):
            F_s_k_t[i] *= (1.0 / np.sqrt(N))

    t = delta_t * np.arange(N_tc, dtype=float)
    k = k_bins.x.copy()
    k_bin_count = k_bins.bin_count.copy()

    output = []
    output += [(k, 'k', 'k-values (technically, bin centers) [nm^1]'),
               (t, 't', 'time values [fs]'),
               (k_bin_count, 'k_bin_count', 'Number of k-points per bin')]
    output += [(F_k_t[m], 'F_k_t_%i_%i' % (i, j),
                'Partial intermediate scattering function [time, k] ({})'
                .format(pair_types[m]))
               for m, i, j in pair_list]

    if calculate_current:
        output += [(Cl_k_t[m], 'Cl_k_t_%i_%i' % (i, j),
                    'Longitudinal current correlation [time, k] ({})'
                    .format(pair_types[m])) for m, i, j in pair_list]
        output += [(Ct_k_t[m], 'Ct_k_t_%i_%i' % (i, j),
                    'Transversal current correlation [time, k] ({})'
                    .format(pair_types[m]))
                   for m, i, j in pair_list]

    if calculate_self:
        output += [(F_s_k_t[i], 'F_s_k_t_%i' % i,
                    'Self part of intermediate scattring function [time, k]')
                   for i in range(index.N_sections())]

    if len(k) > 1:
        # Create an odd number of linearly spaced k-points, ranging from
        # the "distance" of the smallest non-empty bin and up.
        k_ = k_bins.x_linspace
        k_ = k_[k_ >= k[1]]
        k_ = k_[k_ <= k[-1]]
        if not len(k_) % 2:
            k_ = k_[:-1]

        dr = two_pi / k[-1]
        r = np.arange(5 * dr, pi / k[1], dr)

        def F_to_G(F, pair_index):
            _, i, j = pair_list[pair_index]
            f = 1 / (r * 2 * pi ** 2 * particle_densities[j])
            kF_ = k_ * interp1d(k, F - 1)(k_)
            return f * filon.sin_integral(kF_, k_[1] - k_[0], r,
                                          k_[0], axis=1) + 1
        G_r_t = [F_to_G(F, i) for i, F in enumerate(F_k_t)]

        output += [(r, 'r', 'r-values for calculated G(r,t) [nm]')]
        output += [(G_r_t[m], 'G_r_t_%i_%i' % (i, j),
                    'Calculated partial van Hove function [time, r] ({})'
                    .format(pair_types[m]))
                   for m, i, j in pair_list]

    if len(t) > 2:
        w, S_k_w = zip(*[filon.fourier_cos(F, delta_t) for F in F_k_t])
        w = w[0]
        output += [(w, 'w', 'omega [fs^-1]')]
        output += [(S_k_w[m], 'S_k_w_%i_%i' % (i, j),
                    'Partial dynamical structure factor [omega, k] ({})'
                    .format(pair_types[m]))
                   for m, i, j in pair_list]

        if calculate_current:
            _, Cl_k_w = zip(*[filon.fourier_cos(C, delta_t) for C in Cl_k_t])
            _, Ct_k_w = zip(*[filon.fourier_cos(C, delta_t) for C in Ct_k_t])
            output += [(Cl_k_w[m], 'Cl_k_w_%i_%i' % (i, j),
                        'Longitudinal partial current correlation'
                        ' [omega, k] ({})'.format(pair_types[m]))
                       for m, i, j in pair_list]
            output += [(Ct_k_w[m], 'Ct_k_w_%i_%i' % (i, j),
                        'Transversal partial current correlation'
                        ' [omega, k] ({})'.format(pair_types[m]))
                       for m, i, j in pair_list]

        if calculate_self:
            _, S_s_k_w = zip(*[filon.fourier_cos(F, delta_t) for F in F_s_k_t])
            output += [(S_s_k_w[i], 'S_s_k_w_%i' % i,
                        'Self part of partial dynamical structure factor'
                        ' [omega, k]')
                       for i, _ in enumerate(particle_types)]

    # finalize results
    return output


def compute_spectral_energy_density(
        trajectory_file: str,
        ideal: Atoms,
        prim: Atoms,
        q_points: List[np.ndarray],
        max_frames: int = 100,
        dt: int = 1,
        log_level: int = -1):
    """
    Compute Spectral energy density (SED) for specific q-points.

    Note that this implementation reads the full trajectory (upto max_frames),
    and can thus consume alot of memory.

    TODO: REF to SED paper

    Parameters
    ----------
    trajectory_file
        Molecular dynamics trajectory file to be analyzed. Supported formats depends on VMDs
        molfile plugin or gmxlib. As a fallback, a lammps-trajectory parser implemented in Python
        is available as well as a .extxyz reader based on ASE
    ideal
        ideal atoms object
    prim
        compatible primitive cell. Must be aligned correctly
    q_points
        list of q points in cart coord (2pi must be included)
    max_frames
        Limits the total number of trajectory frames read to max_frames
    dt
        Explicitly sets the time difference between two consecutively processed trajectory frames
        to dt (in femtoseconds)
    log_level
        Verbosity level, available options are DEBUG, INFO, QUIET. Default is INFO
    """

    # read full traj
    traj = []

    # colllect all velocities
    velocities = []
    for atom in traj:
        velocities.append(atom.get_velocities())
    velocities = np.array(velocities)
    velocities = velocities.transpose(1, 2, 0).copy()
    velocities = np.fft.fft(velocities, axis=2)

    masses = prim.get_masses()
    indices, offsets = _index_offset(ideal, prim)

    pos = np.dot(q_points, np.dot(offsets, prim.cell).T)
    exppos = np.exp(1.0j * pos)
    density = np.zeros((len(q_points), velocities.shape[2]))
    for alpha in range(3):
        for b in range(len(masses)):
            tmp = np.zeros(density.shape, dtype=np.complex)
            for i in range(len(indices)):
                index = indices[i]
                if index != b:
                    continue
                tmp += np.outer(exppos[:, i], velocities[i, alpha])

            density += masses[b] * np.abs(tmp)**2

    return density


def _index_offset(atoms, prim, atol=1e-3, rtol=0.0):
    index, offset = [], []
    for pos in atoms.positions:
        spos = np.linalg.solve(prim.cell.T, pos)
        for i, spos2 in enumerate(prim.get_scaled_positions()):
            off = spos - spos2
            off_round = np.round(off)
            if not np.allclose(off, off_round, atol=atol, rtol=rtol):
                continue
            index.append(i)
            off = off_round.astype(int)
            assert np.allclose(off, off_round)
            offset.append(off)
            break
        else:
            raise ValueError('prim not compatible with atoms')

    index, offset = np.array(index), np.array(offset)
    return index, offset
