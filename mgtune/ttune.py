
import os
import shutil
from pathlib import Path
import pickle
import numpy as np
import PyNomad as pynomad
from . import function_info
from . import parsing
from . import optinterface


def tune(user_solver_file,A_list,b_list,wfdl=None,optimal_solver_file=None,
         n_trials=1,max_f_eval=1000,disp_level=2):
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
    optimal_solver_file : {string or path}
        location to save source code of optimal solver configuration
    n_trial : {integer}
        number of times to evaluate each iterate in objective function (since
            timing can have errors)
    max_f_eval : {integer}
        maximum number of function evaluations for optimizer
    disp_level {integer}
        detail level of NOMAD's terminal output, in [0,3] inclusive
    ---Outputs---
    optimal_solver_file : {path}
        path to an optimized version of solver at location user_solver_file 
    """
    #set up path for user side files
    user_solver_dir = '/'.join(user_solver_file.split('/')[:-1])
    if (optimal_solver_file is None):
        optimal_solver_file = user_solver_dir + '/optimal_solver.py'

    #names of internal mgtune files
    working_dir_name = 'mgtune_working'
    working_dir = user_solver_dir + '/' + working_dir_name
    tagged_solver_file = working_dir + '/tagged_solver.py'
    running_solver_file = working_dir + '/running_solver.py'
    types_file = working_dir + '/param_types.txt'
    lower_bounds_file = working_dir + '/param_lower_bounds.txt'
    upper_bounds_file = working_dir + '/param_upper_bounds.txt'
    options_file = working_dir + '/options.p' #pickle of parameter options
    n_trials_file = working_dir + '/n_trials.p' #pickle of n_trials
    A_list_file = working_dir + '/A_list.p' #pickle file of A_list
    b_list_file = working_dir + '/b_list.p' #pickle file of b_list

    mgtune_dir = str(Path(__file__).parent) #will be the directory containing mgtune modules

    #NOMAD files
    params_file = working_dir + '/params.txt' #NOMAD solver options etc.
    obj_file_name = 'obj.py'
    obj_file = working_dir + '/' + obj_file_name #NOMAD's black box objective function

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
    t_list,lb_list,ub_list = optinterface.get_types_and_bounds(options_list)
    types_list = t_list #rename for clarity (above line was too long)
    lower_bounds_list = lb_list 
    upper_bounds_list = ub_list

    #create pickle of: (options,types,lower_bounds,upper_bounds)_list, n_trials
    pickle.dump(options_list,open(options_file,'wb'))
    pickle.dump(types_list,open(types_file,'wb'))
    pickle.dump(lower_bounds_list,open(lower_bounds_file,'wb'))
    pickle.dump(upper_bounds_list,open(upper_bounds_file,'wb'))
    pickle.dump(n_trials,open(n_trials_file,'wb'))

    #create picke of: A_list, b_list
    pickle.dump(b_list,open(b_list_file,'wb'))
    pickle.dump(A_list,open(A_list_file,'wb'))
    
    #copy prewritten objective function into working/running directory so NOMAD can find it
    print(mgtune_dir+'obj.py')
    shutil.copy(mgtune_dir+'/obj.py',working_dir)

    #create human readable params file (for NOMAD)
    optinterface.write_params_file(params_file,types_file,
                                   lower_bounds_file,upper_bounds_file,
                                   obj_file,max_f_eval)

    #convert readable params file into a list of strings, each element sets an option
    nomad_params_list = optinterface.params_file_to_list(params_file)

    #call NOMAD with params
    pynomad.optimizeWithMainStep(nomad_params_list)

    #copy source code of optimal solver to user side
    shutil.copy(running_solver_file,optimal_solver_file)

    #delete temporary working/running directory
    if (os.path.exists(working_dir)):
        shutil.rmtree(working_dir)

    return  optimal_solver_file


    

