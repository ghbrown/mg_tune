
import numpy as np
import pyamg
"""
from pyamg import smoothed_aggregation_solver
from pyamg.gallery import poisson
from scipy.sparse.linalg import cg
"""
A = pyamg.gallery.poisson((100,100), format='csr')           # matrix
b = np.ones((A.shape[0]))                      # RHS
ml = pyamg.aggregation.smoothed_aggregation_solver(A)            # AMG solver
x = ml.solve(b,tol=1e-10)
#M = ml.aspreconditioner(cycle='V')             # preconditioner
#x,info = cg(A, b, tol=1e-8, maxiter=30, M=M)   # solve with CG
