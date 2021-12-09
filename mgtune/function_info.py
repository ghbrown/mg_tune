import copy
import numpy as np

def function_dict_list():
    """
    Return list of dictionaries which contain info/parameters
    for functions that mgtune "knows about"
    ---Inputs---
    NONE
    ---Outputs---
    fdl : {list}
        function dictionary list, a list of dictionaries, each of which defines the free parameters of a function and its possible values
    """
    fdl = [sa_dict] #[f]unction [d]ictionary [l]ist
    return copy.deepcopy(fdl)


def tunable():
    """
    Print all tunable functions to terminal
    """
    print('\nmgtune can optimize all or some of the optional arguments of:')
    for cur_dict in function_dict_list():
        print('    ' + cur_dict["function_name"])
    print('by default. \n\nHowever, if you would like it to optimize over custom parameters')
    print('use the optional argument of mgtune.tune(A_list,b_list,wfdl=None)\n')


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
    "strength" : ['\'symmetric\'','\'classical\'','\'evolution\'','\'algebraic_distance\''],
    #need to accomomodate stuff like strength = ('symmetric',{'theta':0.25})
    "aggregate" : ['\'standard\'','\'lloyd\'','\'naive\''],
    "smooth" : ['\'jacobi\'','\'richardson\'','\'energy\''],
    #need to accomomodate stuff like smooth = ('jacobi',{'theta':0.25})
    "presmoother" : ['\'jacobi\'','\'gauss_seidel\'','\'richardson\'','\'sor\''],
    "postsmoother" : ['\'jacobi\'','\'gauss_seidel\'','\'richardson\'','\'sor\''],
    #not exactly sure what options are for above two arguments
    "improve_candidates" : 'untunable',
    "max_coarse" : [str(elem) for elem in [33,25,20,17,13,9,5,3]],
    #having as actual integer could be disaster at high end
    #perhaps change from these values to range(2,51) if speed allows
    "max_levels" : [str(elem) for elem in range(16)], #number of levels, realistically not above 15
    #"cycle_type" : ['\'V\'','\'W\'','\'F\''], 
    #"coarse_solver" : ['\'splu\'','\'lu\'','\'cholesky\'','\'pinv\'','\'gauss_seidel\''],
    #TODO: above two commented out because they are not optional arguments
    "keep" : 'untunable',
    }

"""
TODO: add suppport for nested options
for example, strength options of pyamg.aggregation.smoothed_aggregation_solver
can really take forms like
smooth = ('symmetric',{'theta':0.25})
but this seems like a nightmare to code right now
"""
