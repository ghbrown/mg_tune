
import numpy as np
import pyamg
import mgtune

A = pyamg.gallery.poisson((100,100), format='csr')   # matrix
b = np.ones((A.shape[0]))                            # right hand side

A_list = [A]    #put tuning/training set in mgtune's expected form
b_list = [b]

solver_file = "sa_solver.py"   #location of solver function file

what_will_the_output_look_like = mgtune.tune("sa_solver.py",A_list,b_list)

