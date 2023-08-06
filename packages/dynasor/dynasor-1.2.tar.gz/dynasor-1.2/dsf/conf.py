import warnings


class conf(dict):

    def __setitem__(self, key, value):

        if key == 'backend':
            if value == 'numba':
                warnings.warn('Running with experimental numba backend')

        super().__setitem__(key, value)


conf = conf(backend='c')
