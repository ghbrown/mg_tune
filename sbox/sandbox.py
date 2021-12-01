
import numpy as np
#import pyamg
import mgtune

n = 100
#PROBLEM, PYAMG IS BROKEN INSIDE VENV
#A = pyamg.gallery.poisson((n,n), format='csr')   # matrix
A = np.random.rand(n,n)
b = np.ones((A.shape[0]))                            # right hand side

A_list = [A]    #put tuning/training set in mgtune's expected form
b_list = [b]

solver_file = 'sa_solver.py'   #location of solver function file

#what_will_the_output_look_like = mgtune.tune("sa_solver.py",A_list,b_list)

