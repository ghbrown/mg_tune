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


def tunable():
    """
    Print all tunable functions to terminal
    """
    for cur_dict in function_dict_list():
        print('    ' + cur_dict["function_name"])


#DICTIONARIES DEFINING PARAMETER NAMES AND POSSIBLE VALUES FOR FUNCTIONS
#keywords for values of function dictionaries include:
#    - untunable: cannot/will not be tuned by mgtune because (one of):
#                      - the parameter space is too large
#                      - implementation would be extremely complicated
#                      - parameter does not affect performance
#                 NOTE: untunables may still be set by the user in their function
#    - unbounded_<type>: set of options has infinite size (int or float)

sa_dict = {
    "function_name" : 'pyamg.aggregation.smoothed_aggregation_solver',
    "B" : 'untunable', #False means that parameter is untunable by mgtune
    "BH" : 'untunable',
    "symmetry" : 'untunable',
    "strength" : ['symmetric','classical','evolution','algebraic_distance'],
    #need to accomomodate stuff like strength = ('symmetric',{'theta':0.25})
    "aggregate" : ['standard','lloyd','naive'],
    "smooth" : ['jacobi','richardson','energy'],
    #need to accomomodate stuff like smooth = ('jacobi',{'theta':0.25})
    "presmoother" : ['???'], #actually no idea what the options are
    "postsmoother" : ['???'], #actually no idea what the options are
    "improve_candidates" : 'untunable',
    "max_coarse" : [33,25,20,17,13,9,5,3], #having as actual integer would be disaster
    #perhaps change from these values to range(2,51) if speed allows
    "max_levels" : 'unbounded_int',
    "cycle_type" : ['V','W','F'],
    "coarse_solver" : ['splu','lu','cholesky','pinv','gauss_seidel'],
    "keep" : 'untunable',
    }

"""
TODO: add suppport for nested options
for example, strength options of pyamg.aggregation.smoothed_aggregation_solver
can really take forms like
smooth = ('symmetric',{'theta':0.25})
but this seems like a nightmare to code right now
"""
