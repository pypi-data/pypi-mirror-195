from dsf.trajectory_reader.abstract_trajectory_reader \
    import abstract_trajectory_reader
from itertools import count
from ase.io.extxyz import iread_xyz


class extxyz_trajectory_reader(abstract_trajectory_reader):
    """Read extend xyz trajectory file, typicall produced by GPUMD

    This is a naive (and comparatively slow) implementation which relies on ASE xyz reader
    """

    @classmethod
    def available(cls):
        return True

    def __init__(self, filename, x_factor=0.1, t_factor=1.0):

        self._fobj = open(filename, 'r')
        indices = slice(0, None, 1)
        self._generator_xyz = iread_xyz(self._fobj, indices=indices)

        self._open = True
        self.x_factor = x_factor
        self.t_factor = t_factor
        self.v_factor = x_factor / t_factor
        self._index = count(1)

    def _get_next(self):
        try:
            atoms = next(self._generator_xyz)
        except Exception:
            self._fobj.close()
            self._open = False
            raise StopIteration

        self._natoms = len(atoms)
        self._box = atoms.cell[:]
        self._time = atoms.info['Time']
        self._x = atoms.positions.T
        if 'vel' in atoms.arrays:
            self._v = atoms.arrays['vel'].T
        else:
            self._v = None

    def __iter__(self):
        return self

    def close(self):
        if not self._fobj.closed:
            self._fobj.close()

    def __next__(self):
        if not self._open:
            raise StopIteration

        self._get_next()

        res = dict(
            index=next(self._index),
            N=int(self._natoms),
            box=self.x_factor * self._box.copy('F'),
            time=self.t_factor * self._time,
            x=self.x_factor * self._x,)

        if self._v is not None:
            res['v'] = self.v_factor * self._v

        return res
