
import os
import numpy as np
import PyNomad as pynomad
from . import function_info
from . import parsing
from . import optinterface


def tune(user_solver_file,A_list,b_list,wfdl=None):
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
    wfdl : {list}
        working function dictionary list, a list of dictionaries, each of which
        defines the free parameters of a function and its possible values
        (this allows a user who knows what they are doing to set up a custom
            run with a limited or expanded set of possible parameters)
    ---Outputs---
    optimal_solver_file : {path}
        path to an optimized version of solver at location user_solver_file 
    """
    #set up path for runtime files
    user_solver_dir = '/'.join(user_solver_file.split('/')[:-1])
    working_dir = user_solver_dir + '/mgtune_working'
    tagged_solver_file = working_dir + '/tagged_solver.py'
    running_solver_file = working_dir + '/running_solver.py'
    optimal_solver_file = user_solver_dir + '/optimal_solver.py'
    types_file = working_dir + '/param_types.txt'
    lower_bounds_file = working_dir + '/param_lower_bounds.txt'
    upper_bounds_file = working_dir + '/param_upper_bounds.txt'

    #get info about all functions mgtune can configure and their options
    #either from user input, or from mgtune's internal "database"
    if (wfdl is None):
        wfdl = function_info.function_dict_list() #[w]orking [f]unction [d]ictionary [l]ist

    #create tagged file
    options_list = parsing.tag_file(user_solver_file,tagged_solver_file,wfdl)
    optinterface.write_types_and_bounds(options_list,types_file,
                                        lower_bounds_file,upper_bounds_file)

    #create pickle of A_list and b_list

    #creat pickle of options_list
    
    #create params file (for NOMAD)

    #process params file into a single list of strings
    with open('youll have to fix this') as f:
        lines = f.readlines()

    #retain only lines with things on them
    params = [line.strip() for line in lines if not line.isspace()] 

    #call NOMAD on params file (as string)
    pynomad.optimizeWithMainStep(params)

    """ for production
    if os.path.exists(tagged_solver_file):
        os.remove(tagged_solver_file)

    shutil.copy(running_solver_file,optimal_solver_file)
    """


    return  optimal_solver_file


    

