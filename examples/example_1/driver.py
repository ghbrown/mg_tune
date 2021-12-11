
from pathlib import Path
import numpy as np
import pyamg
import pyamg.gallery

import mgtune
from mgtune import parsing
from mgtune import function_info


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
tagged_solver_path = cur_dir + '/sa_solver_tagged.py'

#tune solver at location solver_path
mgtune.tune(solver_path,A_list,b_list,n_trials=3,max_f_eval=50,disp_level=3)



