import numpy as np
import numba


@numba.njit(fastmath=True, nogil=True)
def kernel(x, k):
    tmp = 0.0j
    Nx = x.shape[0]
    for xi in range(Nx):
        alpha = x[xi, 0]*k[0] + x[xi, 1]*k[1] + x[xi, 2]*k[2]
        tmp += np.exp(1j * alpha)
    return tmp


@numba.njit(fastmath=True, nogil=True, parallel=True)
def rho_k(x: np.ndarray, Nx: int, k: np.ndarray, Nk: int, rho: np.ndarray):
    """Calculates the fourier transformed density

    Parameters
    ----------
    x
        the positions as a np.float64 array with shape (3, Nx)
    Nx
        the number of particles
    k
        the k points as a np.float64 array with shape (3, Nk)
    Nk
        the number of k-points
    rho
        density as a np.complex128 array of length Nk
    """

    # dynasor uses 3xN array which makes my brain hurt
    x = x.T
    k = k.T

    for ki in numba.prange(Nk):
        rho[ki] = kernel(x, k[ki])

    rho /= Nx**0.5


@numba.njit(fastmath=True, parallel=True, nogil=True)
def rho_j_k(x: np.ndarray, v: np.ndarray, Nx: int,
            k: np.ndarray, Nk: int,
            rho: np.ndarray, j_k: np.ndarray):
    """Calculates the fourier transformed density and current?

    Parameters
    ----------
    x
        the positions as a np.float64 array with shape (3, Nx)
    v
        the velocities as a np.float64 array with shape (3, Nx)
    Nx
        the number of particles
    k
        the k points as a np.float64 array with shape (3, Nk)
    Nk
        the number of k-points
    rho
        density as a np.complex128 array of length Nk
    j_k
        current as a np.complex128 array with shape (3, Nk)
    """

    x = x.T
    v = v.T
    k = k.T
    j_k = j_k.T

    factor = Nx**-0.5

    for ki in numba.prange(Nk):
        rho_ki_0 = 0
        rho_ki_1 = 0
        j_ki = np.zeros(6)
        for xi in range(Nx):
            alpha = 0
            for i in range(3):
                alpha += x[xi, i] * k[ki, i]
            ca = np.cos(alpha)
            sa = np.sin(alpha)
            rho_ki_0 += ca
            rho_ki_1 += sa
            j_ki[0] += ca * v[xi][0]
            j_ki[1] += sa * v[xi][0]
            j_ki[2] += ca * v[xi][1]
            j_ki[3] += sa * v[xi][1]
            j_ki[4] += ca * v[xi][2]
            j_ki[5] += sa * v[xi][2]
        rho[ki] = factor * (rho_ki_0 + 1j * rho_ki_1)
        for i in range(3):
            j_k[ki, i] = factor * (j_ki[2*i] + 1j * j_ki[1 + 2*i])
