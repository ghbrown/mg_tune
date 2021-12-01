
import pyamg

#solver to be optimized by mgtune
#its inputs are strictly (A,b), but the internals may be arbitrary
#but be sure to use full names (no import as or abbreviations)
def solver(A,b):
    ml = pyamg.aggregation.smoothed_aggregation_solver(A)  #compute multilevel hierarchy
    x = ml.solve(b,tol=1e-10)                              #solve system using multigrid
    return x
