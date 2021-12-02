
import numpy as np
import pyamg

def solver(A,b):
    #ml = pyamg.aggregation.smoothed_aggregation_solver(A)        # AMG solver
    ml = pyamg.aggregation.smoothed_aggregation_solver(A,strength='symmetric',   presmoother=  5)        # AMG solver
    x = ml.solve(b,tol=1e-10)
    return x
