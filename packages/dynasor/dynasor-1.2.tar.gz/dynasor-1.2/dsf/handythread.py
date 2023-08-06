#
# Taken from the SciPy Cookbook, http://www.scipy.org/Cookbook/Multithreading
#


import sys
import threading
from itertools import count


def foreach(f, k, threads=3, return_=False):
    """
    Apply f to each element of k, in parallel.
    """

    if threads > 1:
        iteratorlock = threading.Lock()
        exceptions = []
        if return_:
            d = {}
            i = zip(count(), k.__iter__())
        else:
            i = k.__iter__()

        def runall():
            while True:
                iteratorlock.acquire()
                try:
                    try:
                        if exceptions:
                            return
                        v = i.__next__()
                    finally:
                        iteratorlock.release()
                except StopIteration:
                    return
                try:
                    if return_:
                        n, x = v
                        d[n] = f(x)
                    else:
                        f(v)
                except Exception:
                    e = sys.exc_info()
                    iteratorlock.acquire()
                    try:
                        exceptions.append(e)
                    finally:
                        iteratorlock.release()

        threadlist = [threading.Thread(target=runall) for j in range(threads)]
        for t in threadlist:
            t.start()
        for t in threadlist:
            t.join()
        if exceptions:
            a = exceptions[0]
            raise a
        if return_:
            r = d.items()
            r.sort()
            return [v for (n, v) in r]
    else:
        if return_:
            return [f(v) for v in k]
        else:
            for v in k:
                f(v)
            return


def parallel_map(f, k, threads=3):
    return foreach(f, k, threads=threads, return_=True)
