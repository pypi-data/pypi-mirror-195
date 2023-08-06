dynasor
=======

**dynasor** is a simple tool for calculating total and partial dynamical structure factors as well as current correlation functions from molecular dynamics (MD) simulations.
The main input consists of a trajectory output from a MD simulation, i.e., a file containing snapshots of the particle coordinates and optionally velocities that correspond to consecutive, equally spaced points in (simulation) time.

**dynasor** can by itself read and parse standard ``lammpsdump``-style trajectories.
If ``libgmx`` (a library in the gromacs package) is available, **dynasor** can use it to read gromacs ``xtc``-files.
If VMD is available, **dynasor** can use VMD's `molfileplugin` to read other formats (with some limitations) as well.

**dynasor** is controlled via command line options, provided at command invocation.
Output can be written in the form of standard matlab/octave-stype `m`-files and/or python pickle-files.


Documentation
-------------

The full documentation can be found in the `user guide <http://dynasor.materialsmodeling.org/>`_.


Requirements
------------

Python 3.6+, numpy, and a C99-complient C-compiler.
