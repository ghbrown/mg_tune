
from pathlib import Path
import numpy as np
#import pyamg    #PROBLEM, PYAMG IS BROKEN INSIDE VENV
import mgtune
from mgtune import parsing
from mgtune import function_info

cur_dir = str(Path(__file__).parent)
solver_path = cur_dir + '/sa_solver.py'
marked_path = cur_dir + '/sa_solver_marked.py'

fdl = mgtune.function_info.function_dict_list()
mgtune.parsing.mark_functions(solver_path,marked_path,fdl)

n = 100
A = np.random.rand(n,n)
#A = pyamg.gallery.poisson((n,n), format='csr')   # matrix
b = np.ones((A.shape[0]))                        # right hand side

A_list = [A]    #put tuning/training set in mgtune's expected form
b_list = [b]

solver_file = 'sa_solver.py'   #location of solver function file

#mgtune.tune("sa_solver.py",A_list,b_list)

