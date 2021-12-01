
import numpy as np
import pyamg    #PROBLEM, PYAMG IS BROKEN INSIDE VENV
import mgtune

n = 100
A = np.random.rand(n,n)
#A = pyamg.gallery.poisson((n,n), format='csr')   # matrix
b = np.ones((A.shape[0]))                        # right hand side

A_list = [A]    #put tuning/training set in mgtune's expected form
b_list = [b]

solver_file = 'sa_solver.py'   #location of solver function file

#mgtune.tune("sa_solver.py",A_list,b_list)

