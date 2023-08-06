import numpy as np


class averager:
    """Naive special purpose averager class used in dynasor.

    It assists with keeping track of how many data samples
    have been added to each slot.

    Example
    -------
    av = averager(2)
    av[0] += 10
    av[0] += 2
    av[1] += 3
    av.get_av() ->
    [6, 3]
    """
    def __init__(self, N_slots, initial=np.zeros(1)):
        assert N_slots >= 1
        self._N = N_slots
        self._data = [np.array(initial) for n in range(N_slots)]
        self._samples = np.zeros(N_slots)

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, val):
        self._data[key] = val
        self._samples[key] += 1

    def add(self, array, slot):
        self[slot] += array

    def get_single_av(self, slot):
        f = 1.0 / self._samples[slot]
        return f * self._data[slot]

    def get_av(self):
        return np.array([self.get_single_av(i) for i in range(self._N)])
