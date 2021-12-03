
from pathlib import Path
import numpy as np
import pyamg    #PROBLEM, PYAMG IS BROKEN INSIDE VENV

import mgtune
from mgtune import parsing
from mgtune import function_info


"""
fdl = mgtune.function_info.function_dict_list()
mgtune.parsing.tag_file(solver_path,tagged_solver_path,fdl)
"""
mgtune.tunable()


n = 100
A = np.random.rand(n,n)
#A = pyamg.gallery.poisson((n,n), format='csr')   # matrix
b = np.ones((A.shape[0]))                        # right hand side

A_list = [A]    #put tuning/training set in mgtune's expected form
b_list = [b]


#build relative path from full path (only since running make from different directory)
cur_dir = str(Path(__file__).parent)
solver_path = cur_dir + '/sa_solver.py'
tagged_solver_path = cur_dir + '/sa_solver_tagged.py'


mgtune.tune(solver_path,A_list,b_list)



