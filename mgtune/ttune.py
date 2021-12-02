
import os
import numpy as np
from . import function_info
from . import parsing


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
    ---Outputs---
    optimal_solver_file : {path}
        path to an optimized version of solver at location user_solver_file 
    """
    #set up path for runtime files
    user_solver_dir = '/'.join(user_solver_file.split('/')[:-1])
    tagged_solver_file = user_solver_dir + '/.tagged_solver.py'
    running_solver_file = user_solver_dir + '/.running_solver.py'
    optimal_solver_file = user_solver_dir + 'optimal_solver.py'

    #get info about all functions mgtune can configure
    wfdl = function_info.function_dict_list() #[w]orking [f]unction [d]ictionary [l]ist

    #create tagged file
    options_list = parsing.tag_file(user_solver_file,tagged_solver_file,wfdl)

    """ for production
    if os.path.exists(tagged_solver_file):
        os.remove(tagged_solver_file)

    shutil.copy(running_solver_file,optimal_solver_file)
    """

    return  optimal_solver_file


    

