
import numpy as np
import pyamg

A = pyamg.gallery.poisson((100,100), format='csr')           # matrix
b = np.ones((A.shape[0]))                                    # RHS 
ml = pyamg.aggregation.smoothed_aggregation_solver(A, strength=mgtune_tag_0, aggregate=mgtune_tag_1, smooth=mgtune_tag_2, presmoother=mgtune_tag_3, postsmoother=mgtune_tag_4, max_coarse=mgtune_tag_5, cycle_type=mgtune_tag_6, coarse_solver=mgtune_tag_7)        # AMG solver
ml = pyamg.aggregation.smoothed_aggregation_solver(A, strength=mgtune_tag_8, aggregate=mgtune_tag_9, smooth=mgtune_tag_10, presmoother=mgtune_tag_11, postsmoother=mgtune_tag_12, max_coarse=mgtune_tag_13, cycle_type=mgtune_tag_14, coarse_solver=mgtune_tag_15)        # AMG solver
x = ml.solve(b,tol=1e-10)
