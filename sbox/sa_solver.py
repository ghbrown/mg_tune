
import numpy as np
import pyamg

A = pyamg.gallery.poisson((100,100), format='csr')           # matrix
b = np.ones((A.shape[0]))                                    # RHS 
ml = pyamg.aggregation.smoothed_aggregation_solver(A)        # AMG solver
ml = pyamg.aggregation.smoothed_aggregation_solver(A)        # AMG solver
x = ml.solve(b,tol=1e-10)
