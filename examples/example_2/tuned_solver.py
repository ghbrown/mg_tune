
import numpy as np
import pyamg

#the function must be called solve and take (A,b) as inputs
def solve(A,b):
    #max_levels not an effective tuning parameter, since often
    #it just results in a multilevel hierarchy which is far too
    #large on the coarsest level
    #therefore fix it to be large so depth of hierarchy is
    #controlled by max_coarse alone
    ml = pyamg.aggregation.smoothed_aggregation_solver(A,max_levels=1000, strength='algebraic_distance', aggregate='standard', smooth='energy', presmoother='gauss_seidel', postsmoother='sor', max_coarse=4)
    x = ml.solve(b,tol=1e-6, cycle='F', accel=None)
    return x
