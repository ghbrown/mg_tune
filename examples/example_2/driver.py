
from pathlib import Path
import numpy as np
import pyamg
import pyamg.gallery

import mgtune

"""
Tune (nearly) all parameters of PyAMG's smoothed aggregation
and multilevel solver for Poisson problem
NOTES: this takes about 20 minutes to run and does not typically
       produce a faster solver, primarily because the default
       PyAMG solver is well optimized for Laplace like problems
       and the current optimization approach is suspceptible to
       noise
"""

#printout of tunable functions
mgtune.tunable()

n = 1000 #matrix dimension
A = pyamg.gallery.poisson((n,),format='csr')  #matrix
b = np.ones((A.shape[0]))                     #right hand side

#put systems in mgtune's expected form
A_list = [A]
b_list = [b]

#build relative path from full path (only since running make from different directory)
#relative paths work if you run python adjacent to driver script
cur_dir = str(Path(__file__).parent)
solver_path = cur_dir + '/sa_solver.py'
tuned_solver_path = cur_dir + '/tuned_solver.py'

#tune solver
mgtune.tune(solver_path,A_list,b_list,tuned_solver_path,
            n_trials=40,max_f_eval=500,disp_level=3)

#compare slow and tuned solvers on training set
solver_list = [solver_path,tuned_solver_path]
mgtune.compare(solver_list,A_list,b_list,n_trials=100)



