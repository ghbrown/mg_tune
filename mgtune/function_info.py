import copy
import numpy as np

def function_dict_list():
    """
    Return list of dictionaries which contain info/parameters
    for functions that mgtune "knows about"
    ---Inputs---
    NONE
    ---Outputs---
    function_ei : {list}
       discrete values of max_coarse, with values as specified above 
    """
    fdl = [sa_dict] #[f]unction [d]ictionary [l]ist
    return copy.deepcopy(fdl)


#DICTIONARIES DEFINING PARAMETER NAMES AND POSSIBLE VALUES FOR FUNCTIONS
#keywords for values of function dictionaries include:
#    - unbounded: set of options has infinite size
#    - preprocess: set of options should be decided based on problem
sa_dict = {
    "function_name" : 'pyamg.aggregation.smoothed_aggregation_solver',
    "strength" : ['symmetric','classical','evolution','algebraic_distance'],
    #need to accomomodate stuff like strength = ('symmetric',{'theta':0.25})
    "aggregate" : ['standard','lloyd','naive'],
    "smooth" : ['jacobi','richardson','energy'],
    #need to accomomodate stuff like smooth = ('jacobi',{'theta':0.25})
    "presmoother" : ['???'], #actually no idea what the options are
    "postsmoother" : ['???'], #actually no idea what the options are
    "max_coarse" : [33,25,20,17,10,9,5,4,2], #having as actual integer would be disaster
    #perhaps change from these values to range(2,51) if things are fast allows
    "max_levels" : 'unbounded_integer',
    "cycle_type" : ['V','W','F'],
    "coarse_solver" : ['splu','lu','cholesky','pinv','gauss_seidel'],
    #arguments to function name which are not tuned because:
    #parameter space is too large, implementation would be very
    #complicated, or they do not affect performance
    #NOTE: these may still be set by the user in their function
    "not_tuned" : ['B','BH','symmetry','improve_candidates','keep']
    }
