
import numpy as np
import pyamg

#the function must be called solve and take (A,b) as inputs
def solve(A,b):
    ml = pyamg.aggregation.smoothed_aggregation_solver(A, strength=mgtune_tag_0, aggregate=mgtune_tag_1, smooth=mgtune_tag_2, presmoother=mgtune_tag_3, postsmoother=mgtune_tag_4, max_coarse=mgtune_tag_5, max_levels=mgtune_tag_6)
    x = ml.solve(b,tol=1e-10)
    return x
