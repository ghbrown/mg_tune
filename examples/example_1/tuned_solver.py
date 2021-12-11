
import numpy as np
import pyamg

#the function must be called solve and take (A,b) as inputs
def solve(A,b):
    ml = pyamg.aggregation.smoothed_aggregation_solver(A,symmetry='hermitian',strength=('symmetric',{"theta":0.25}),aggregate='standard',smooth='jacobi',postsmoother=None,improve_candidates=None,max_levels=10,max_coarse=10,diagonal_dominance=False,keep=False, presmoother=('jacobi',{"withrho":False,"omega":0.4537931034482759}))
    x = ml.solve(b,x0=None,tol=1e-6,maxiter=100,cycle='V',accel=None,callback=None,residuals=None, return_residuals=False)
    return x
