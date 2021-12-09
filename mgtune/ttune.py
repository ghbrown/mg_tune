
import os
import shutil
from pathlib import Path
import pickle
import numpy as np
import PyNomad as pynomad
from . import function_info
from . import parsing
from . import optinterface


def tune(user_solver_file,A_list,b_list,wfdl=None,max_f_eval=1000,disp_level=2):
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
    max_it : {integer}
        maximum number of function evaluations for optimizer
    disp_level {integer}
        detail level of NOMAD's terminal output, in [0,3] inclusive
    ---Outputs---
    optimal_solver_file : {path}
        path to an optimized version of solver at location user_solver_file 
    """
    #set up path for runtime files
    user_solver_dir = '/'.join(user_solver_file.split('/')[:-1])
    working_dir_name = 'mgtune_working'
    working_dir = user_solver_dir + '/' + working_dir_name
    tagged_solver_file = working_dir + '/tagged_solver.py'

    #internal mgtune files
    running_solver_file = working_dir + '/running_solver.py'
    optimal_solver_file = user_solver_dir + '/optimal_solver.py'
    types_file = working_dir + '/param_types.txt'
    lower_bounds_file = working_dir + '/param_lower_bounds.txt'
    upper_bounds_file = working_dir + '/param_upper_bounds.txt'
    options_file = working_dir + '/options.p' #pickle of parameter options
    A_list_file = working_dir + '/A_list.p' #pickle file of A_list
    b_list_file = working_dir + '/b_list.p' #pickle file of b_list

    mgtune_dir = str(Path(__file__).parent) #will be the directory containing mgtune modules

    #NOMAD files
    params_file = working_dir + '/params.txt' #NOMAD solver options etc.
    obj_file_name = 'obj.py'
    obj_file = working_dir + '/obj.py' #NOMAD's black box objective function
    #obj_file_rel_path = working_dir_name + 'obj.py'

    #create directory in which to keep data/running/working files
    try: 
        os.mkdir(working_dir)
    except:
        pass #no need to create directory if it exists

    #get info about all functions mgtune can configure and their options
    #either from user input, or from mgtune's internal "database"
    if (wfdl is None):
        wfdl = function_info.function_dict_list() #[w]orking [f]unction [d]ictionary [l]ist

    #create tagged file
    options_list = parsing.tag_file(user_solver_file,tagged_solver_file,wfdl)

    #write parameter types (int, real, etc.) to files
    optinterface.write_types_and_bounds(options_list,types_file,
                                        lower_bounds_file,upper_bounds_file)

    #create pickle of: options_list, A_list, and b_list
    pickle.dump(options_list,open(options_file,'wb'))
    pickle.dump(b_list,open(b_list_file,'wb'))
    pickle.dump(A_list,open(A_list_file,'wb'))
    
    #create params file (for NOMAD)
    optinterface.write_params_file(params_file,obj_file,types_file,
                                   lower_bounds_file,upper_bounds_file,
                                   max_f_eval)

    #copy prewritten objective function into working/running directory so NOMAD can find it
    shutil.copy(mgtune_dir+'/obj.py',working_dir)

    #convert params file into a single list of strings, each element sets and option
    nomad_params_list = optinterface.params_file_to_list(params_file)

    #call NOMAD with params
    pynomad.optimizeWithMainStep(nomad_params_list)

    """ for production
    if os.path.exists(tagged_solver_file):
        os.remove(tagged_solver_file)

    shutil.copy(running_solver_file,optimal_solver_file)
    """


    return  optimal_solver_file


    

