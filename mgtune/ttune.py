
import numpy as np
from . import function_info


def tune(user_solver_file,A_list,b_list):
    """
    tunes the solver defined in user_solver_file for the problem(s)
    defined by (A_list, b_list)
    ---Inputs---
    user_solver_file : {string or path}
        user defined solver of the form
        --------
        user_solver(A,b):
            amg_function(....,any_argument_that_should_stay_fixed=val)
            return x
        --------
        NOTE: any AMG function (that mg_tune knows about) whose optional
              argumentare left unspecified will consider those parameters
              as tunable
    A_list : {list}
        list of matrices whose solution is desired
    b_list : {list}
        corresponding list of right hand sides for linear systems
    """

    """ CURRENTLY UNUSED
    #set arguments that are dynamic with problem 
    wfdl = function_info.function_dict_list() #[w]orking [f]unction [d]ictionary [l]ist
    for i_f, function_dict in enumerate(wfdl):
        for (key,value) in function_dict.items():
            if (isinstance(value,str) and ('preprocess' in value)):
                function_key = key + '_set' #name of method to set value of key
                wfdl[i_f][key]=function_dict[function_key](A_list,b_list)
    """

    """
    things to be done:
        - determine which functions the user is using and where
        - determine which parameters are free from parsing user kernel file
        - 
    """
    
                
    #get text of user solver
    #loop over all function
    #    loop over all
    #read user function to see which functions mg_tune knows about

