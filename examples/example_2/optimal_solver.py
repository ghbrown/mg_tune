
import numpy as np
import pyamg

#the function must be called solve and take (A,b) as inputs
def solve(A,b):
    ml = pyamg.aggregation.smoothed_aggregation_solver(A, strength='classical', aggregate='lloyd', smooth='richardson', presmoother='gauss_seidel', postsmoother='sor', max_coarse=3, max_levels=3)
    x = ml.solve(b,tol=1e-10)
    return x
