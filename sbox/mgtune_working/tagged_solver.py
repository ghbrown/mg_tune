
import numpy as np
import pyamg

#the function must be called solve and take (A,b) as inputs
def solve(A,b):
    #ml = pyamg.aggregation.smoothed_aggregation_solver(A)        # AMG solver
    ml = pyamg.aggregation.smoothed_aggregation_solver(A,strength='symmetric',   presmoother=  5, aggregate=mgtune_tag_0, smooth=mgtune_tag_1, postsmoother=mgtune_tag_2, max_coarse=mgtune_tag_3, max_levels=mgtune_tag_4, cycle_type=mgtune_tag_5, coarse_solver=mgtune_tag_6)        # AMG solver
    x = ml.solve(b,tol=1e-10)
    return x
