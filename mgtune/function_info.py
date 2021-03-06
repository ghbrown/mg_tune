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
    fdl = [sa_dict,solve_dict] #[f]unction [d]ictionary [l]ist
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
    "improve_candidates" : 'untunable',
    #TODO: this IS very tunable
    #it should really be set to a list of smoothers or something similar
    "max_coarse" : [str(elem) for elem in [2,4,8,16,32,64]],
    "max_levels" : 'untunable', #more effective to tune max_coarse only, as
    #setting max_levels too low results in extremely long solve times
    "keep" : 'untunable',
    }

#TODO: not sure which function takes the coarse_solver option
#"coarse_solver" : ['\'splu\'','\'lu\'','\'cholesky\'','\'pinv\'','\'gauss_seidel\''],

solve_dict = {
    "function_name" : 'ml.solve',
    "x0" : 'untunable',
    "maxiter" : 'untunable',
    "cycle" : ['\'V\'','\'W\'','\'F\''], 
    "accel" : ['None','\'bicgstab\'','\'cgne\'','\'cgnr\'','\'fgmres\'','\'gmres\''], 
    #TODO: cannot currently use all accel options, since some require SPD
    # currently generating SPD warnings: '\'cg\'', 
    }

"""
TODO: add suppport for nested options
for example, strength options of pyamg.aggregation.smoothed_aggregation_solver
can really take forms like
smooth = ('symmetric',{'theta':0.25})
but this seems like a nightmare to code right now
"""
