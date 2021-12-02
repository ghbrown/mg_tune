
import numpy as np
import pyamg

def solver(A,b):
    #ml = pyamg.aggregation.smoothed_aggregation_solver(A)        # AMG solver
    ml = pyamg.aggregation.smoothed_aggregation_solver(A,strength='symmetric',   presmoother=  5, function_name=mgtune_tag_0, aggregate=mgtune_tag_1, smooth=mgtune_tag_2, postsmoother=mgtune_tag_3, max_coarse=mgtune_tag_4, max_levels=mgtune_tag_5, cycle_type=mgtune_tag_6, coarse_solver=mgtune_tag_7)        # AMG solver
    x = ml.solve(b,tol=1e-10)
    return x
