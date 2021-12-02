
import numpy as np
import pyamg

A = pyamg.gallery.poisson((100,100), format='csr')           # matrix
b = np.ones((A.shape[0]))                                    # RHS 
ml =         # AMG solver
x = ml.solve(b,tol=1e-10)
